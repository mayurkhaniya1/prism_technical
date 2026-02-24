#drf permissions class import 
from rest_framework import permissions
from .models import Membership

#organization permissions
class IsOrganizationOwnerOrManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        membership = Membership.objects.filter(user=request.user, organization=obj).first()
        return membership and membership.role in ['OWNER', 'MANAGER']
        # create organization 

# only owner create organizations permiision 
class IsOrganizationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        membership = Membership.objects.filter(user=request.user, organization=obj).first()
        return membership and membership.role == 'OWNER'

# org member permisions 
class IsOrganizationMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return Membership.objects.filter(user=request.user, organization=obj).exists()

# project permissions
class IsProjectOrganizationMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return Membership.objects.filter(user=request.user, organization=obj.organization).exists()

# permision given owner and manager
class IsProjectOrganizationOwnerOrManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        membership = Membership.objects.filter(user=request.user, organization=obj.organization).first()
        return membership and membership.role in ['OWNER', 'MANAGER']

# project owner permission
class IsProjectOrganizationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        membership = Membership.objects.filter(user=request.user, organization=obj.organization).first()
        return membership and membership.role == 'OWNER'

# permision task or isue permision
class IsIssueOrganizationMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return Membership.objects.filter(user=request.user, organization=obj.project.organization).exists()

# permision for priority 
class CanChangeIssuePriority(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        membership = Membership.objects.filter(user=request.user, organization=obj.project.organization).first()
        return membership and membership.role in ['OWNER', 'MANAGER']

# permision for task or isuse 
class CanMarkIssueDone(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if obj.assignee == request.user:
            return True
        membership = Membership.objects.filter(user=request.user, organization=obj.project.organization).first()
        return membership and membership.role in ['OWNER', 'MANAGER']

# permision delete isuse
class CanDeleteIssue(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if obj.created_by == request.user:
            return True
        membership = Membership.objects.filter(user=request.user, organization=obj.project.organization).first()
        return membership and membership.role in ['OWNER', 'MANAGER']