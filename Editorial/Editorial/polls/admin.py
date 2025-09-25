from django.contrib import admin
from .models import Poll, PollFile

class PollFileInline(admin.TabularInline):
    model = PollFile
    extra = 0
    readonly_fields = ()

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id','title','author','created_at')
    inlines = [PollFileInline]

@admin.register(PollFile)
class PollFileAdmin(admin.ModelAdmin):
    list_display = ('id','poll','file','uploaded_at')
