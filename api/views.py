from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
from .models import Organization, Membership, Project, Issue
from .serializers import (
    OrganizationSerializer, MembershipSerializer, ProjectSerializer, IssueSerializer,
    UserRegistrationSerializer, UserSerializer
)
from .permissions import (
    IsOrganizationOwnerOrManager, IsOrganizationOwner, IsOrganizationMember,
    IsProjectOrganizationMember, IsProjectOrganizationOwnerOrManager, IsProjectOrganizationOwner,
    IsIssueOrganizationMember, CanChangeIssuePriority, CanMarkIssueDone, CanDeleteIssue
)
from api import serializers

# create user register view 

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []

# create org viewset 
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        org = serializer.save(created_by=self.request.user)
        # Create membership as OWNER
        Membership.objects.create(user=self.request.user, organization=org, role='OWNER')

    def get_queryset(self):
        return Organization.objects.filter(memberships__user=self.request.user)

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOrganizationOwner()]
        return [IsAuthenticated(), IsOrganizationMember()]

#create membership viewset
class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Membership.objects.filter(organization_id=self.kwargs['organization_pk'])

    # def perform_create(self, serializer):
    #     org = Organization.objects.get(pk=self.kwargs['organization_pk'])
    #     serializer.save(organization=org)

    def perform_create(self, serializer):
        org = Organization.objects.get(pk=self.kwargs['organization_pk'])
        serializer.save(organization=org)

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsOrganizationOwnerOrManager()]
        elif self.action in ['update', 'partial_update']:
            # For promoting to OWNER, check if current user is OWNER
            return [IsAuthenticated(), IsOrganizationOwner()]
        elif self.action in ['destroy']:
            # Cannot remove last OWNER, etc. But for simplicity, allow OWNER or MANAGER
            return [IsAuthenticated(), IsOrganizationOwnerOrManager()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'role' in request.data and request.data['role'] == 'OWNER':
            # Only OWNER can promote to OWNER
            membership = Membership.objects.filter(user=request.user, organization=instance.organization, role='OWNER').first()
            if not membership:
                return Response({"error": "Only OWNER can promote to OWNER."}, status=status.HTTP_403_FORBIDDEN)
        if instance.role == 'OWNER' and request.data.get('role') != 'OWNER':
            # Check if this is the last OWNER
            owner_count = Membership.objects.filter(organization=instance.organization, role='OWNER').count()
            if owner_count <= 1:
                return Response({"error": "Cannot remove the last OWNER from the organization."}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.role == 'OWNER':
            owner_count = Membership.objects.filter(organization=instance.organization, role='OWNER').count()
            if owner_count <= 1:
                return Response({"error": "Cannot remove the last OWNER from the organization."}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

# create project viewset
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(organization__memberships__user=self.request.user)

    def perform_create(self, serializer):
        org = Organization.objects.get(pk=self.kwargs['organization_pk'])
        serializer.save(organization=org, created_by=self.request.user)

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsOrganizationOwnerOrManager()]
        elif self.action in ['destroy']:
            return [IsAuthenticated(), IsProjectOrganizationOwner()]
        return [IsAuthenticated(), IsProjectOrganizationMember()]

# create issue or task viewset
class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['project', 'status', 'priority', 'assignee']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        return Issue.objects.filter(project__organization__memberships__user=self.request.user)

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        if not Membership.objects.filter(user=self.request.user, organization=project.organization).exists():
            raise serializers.ValidationError("You are not a member of this organization.")
        serializer.save(project=project, created_by=self.request.user)

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated()]  # Check in perform_create
        elif self.action in ['update', 'partial_update']:
            # For priority, special permission
            if 'priority' in self.request.data:
                return [IsAuthenticated(), CanChangeIssuePriority()]
            elif 'status' in self.request.data and self.request.data['status'] == 'DONE':
                return [IsAuthenticated(), CanMarkIssueDone()]
            return [IsAuthenticated(), IsIssueOrganizationMember()]
        elif self.action in ['destroy']:
            return [IsAuthenticated(), CanDeleteIssue()]
        return [IsAuthenticated(), IsIssueOrganizationMember()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'assignee' in request.data:
            assignee = User.objects.get(pk=request.data['assignee'])
            if not Membership.objects.filter(user=assignee, organization=instance.project.organization).exists():
                return Response({"error": "Assignee must be a member of the organization."}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)
