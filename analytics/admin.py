from django.contrib import admin

from analytics.models import Feedback, RoomBooking


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'rating', 'text')


class RoomBookingAdmin(admin.ModelAdmin):
    list_display = (
        'room',
        'renter',
        'check_in_date',
        'check_out_date',
        'created_at'
    )
    readonly_fields = (
        'room',
        'renter',
        'check_in_date',
        'check_out_date',
        'created_at'
    )


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(RoomBooking, RoomBookingAdmin)

