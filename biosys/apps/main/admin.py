from __future__ import absolute_import, unicode_literals, print_function, division

from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from reversion.admin import VersionAdmin

from main import forms
from main.models import *

logger = logging.getLogger(__name__)


@admin.register(Project)
class ProjectAdmin(VersionAdmin, OSMGeoAdmin):
    fields = ('name', 'code', 'datum', 'timezone', 'custodians', 'attributes',
              'description', 'site_data_package', 'geometry')
    filter_horizontal = ('custodians',)  # TODO: why it's not working?
    list_display = ('name', 'id', 'code')
    readonly_fields = ['id']
    search_fields = ['name', 'code']
    form = forms.ProjectForm


@admin.register(Site)
class SiteAdmin(VersionAdmin, OSMGeoAdmin):
    fields = ('project', 'code', 'name', 'geometry', 'description', 'attributes')
    list_display = ['code', 'project', 'name']
    list_filter = ['project']
    form = forms.SiteForm
    default_lon = 125.0
    default_lat = -18.0
    default_zoom = 6

    class Media:
        css = {'all': ('css/site_admin.css',)}


@admin.register(Dataset)
class DatasetAdmin(VersionAdmin):
    list_display = ['name', 'project', 'type', 'description']
    list_filter = ['project']
    form = forms.DataSetForm


@admin.register(Record)
class RecordAdmin(VersionAdmin, OSMGeoAdmin):
    list_display = ['dataset', 'data']
    list_filter = ['dataset']
    readonly_fields = ['data']
