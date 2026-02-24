from django.contrib import admin
# admin site register models to handle admin operations 
from .models import Organization, Membership, Project, Issue

# Register models admin site
admin.site.register(Organization)
admin.site.register(Membership)
admin.site.register(Project)
admin.site.register(Issue)

