from django.contrib import admin
from .models import Responsible, Room, EnviromentalParameters, Profession, MeasurementInstrument, ParameterSet


admin.site.register(Responsible)
admin.site.register(EnviromentalParameters)
admin.site.register(Profession)
admin.site.register(ParameterSet)


@admin.register(MeasurementInstrument)
class MeasurementInstrumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'serial_number', 'calibration_date', 'calibration_interval')
    
   
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'list_responsibles')

    def list_responsibles(self, obj):
        return ", ".join([responsible.last_name for responsible in obj.responsible_persons.all()])
    list_responsibles.short_description = 'Ответственные'



