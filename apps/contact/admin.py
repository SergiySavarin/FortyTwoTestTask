from django.contrib import admin
from .models import Owner
from south.models import MigrationHistory

# Register your models here.
admin.site.register(Owner)

admin.site.register(MigrationHistory)
