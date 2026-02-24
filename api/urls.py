from django.urls import path, include
# import default router for DRF
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView, OrganizationViewSet, MembershipViewSet, ProjectViewSet, IssueViewSet
)

# call default router org DRF
router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)

# Nested routers for memberships, projects, issues
organizations_router = DefaultRouter()
organizations_router.register(r'memberships', MembershipViewSet, basename='organization-memberships')

# call default router for projects and issues
projects_router = DefaultRouter()
projects_router.register(r'issues', IssueViewSet, basename='project-issues')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('organizations/<int:organization_pk>/', include([
        path('', include(organizations_router.urls)),
        path('projects/', ProjectViewSet.as_view({'get': 'list', 'post': 'create'}), name='organization-projects'),
        path('projects/<int:pk>/', ProjectViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='organization-project-detail'),
        path('projects/<int:project_pk>/issues/', IssueViewSet.as_view({'get': 'list', 'post': 'create'}), name='project-issues'),
        path('projects/<int:project_pk>/issues/<int:pk>/', IssueViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='project-issue-detail'),
    ])),
]