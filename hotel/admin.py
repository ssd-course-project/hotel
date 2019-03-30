from django.contrib import admin
from .models import Room, ExtraPictures, AdditionalService


class ExtraPicturesInline(admin.TabularInline):
    model = ExtraPictures
    extra = 0




class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_status', 'check_in_date', 'check_out_date', 'price')

    inlines = [ExtraPicturesInline]


admin.site.register(Room, RoomAdmin)


class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(AdditionalService, AdditionalServiceAdmin)


