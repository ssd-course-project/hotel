from django.contrib import admin
from .models import Room, ExtraPictures, ExtraService


class ExtraPicturesInline(admin.TabularInline):
    model = ExtraPictures
    extra = 0


class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_status', 'check_in_date', 'check_out_date', 'price')

    inlines = [ExtraPicturesInline]


class ExtraServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(Room, RoomAdmin)
admin.site.register(ExtraService, ExtraServiceAdmin)
