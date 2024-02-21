from django.contrib import admin
from.models import Tutoria

# Register your models here.

class TutoriasAdmin(admin.ModelAdmin):
    """Define admin model for Tutorias objects"""

    fieldsets = (

    )
    list_display = ('tema', 'alumno', 'tutor', 'descripcion', 'fecha')
    search_fields = ('tema', 'alumno', 'tutor', 'fecha')

admin.site.register(Tutoria, TutoriasAdmin)