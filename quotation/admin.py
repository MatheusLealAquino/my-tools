from django.contrib import admin
from django.utils.html import format_html

from quotation.models import Demand, City, State

class DemandAdmin(admin.ModelAdmin):
  list_display = ('description', 'street_name', 'number_address', 'city', 'cep', 'email', 'cellphone', 'is_ended')

  def is_ended(self, obj):
    if obj.status:
      return format_html('<img src="/static/admin/img/baseline-check_circle_outline.svg" alt="True">')
    else:
      return format_html('<img src="/static/admin/img/baseline-highlight_off.svg" alt="False">')

  is_ended.short_description = 'Status'

admin.site.register(Demand, DemandAdmin)
admin.site.register(City)
admin.site.register(State)
