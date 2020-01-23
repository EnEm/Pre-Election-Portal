from django.contrib import admin
from . import models


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'position')
    list_filter = ('position',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('asked_to', 'question')
    list_filter = ('approved', 'asked_to', 'answered',)
    search_fields = ('question', 'asked_to', 'answer',)
    actions = ('approve_questions',)

    def approve_questions(self, request, queryset):
        queryset.update(approved=True)


class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'no_of_votes', 'total_residents')


admin.site.register(models.Junta)
admin.site.register(models.Candidate, CandidateAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Hostel, HostelAdmin)
