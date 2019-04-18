from django.contrib import admin

from analytics.models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'rating', 'text')


admin.site.register(Feedback, FeedbackAdmin)
