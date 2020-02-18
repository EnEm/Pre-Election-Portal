from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from . import models


class JuntaAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'image_tag']
    readonly_fields = ['image_tag']


class CandidateAdmin(SummernoteModelAdmin):
    list_display = ('user', 'position')
    list_filter = ('position',)
    summernote_fields = ('bio', 'key_points')


class QuestionAdmin(SummernoteModelAdmin):
    list_display = ('asked_to', 'question')
    list_filter = ('approved', 'asked_to', 'answered',)
    search_fields = ('question', 'asked_to', 'answer',)
    actions = ('approve_questions',)
    summernote_fields = ('answer',)


class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'no_of_votes', 'total_residents')


class CommentAdmin(SummernoteModelAdmin):
    list_display = ('comment', 'question', 'comment_by')
    actions = ('approve_comments',)


admin.site.register(models.User)
admin.site.register(models.Junta, JuntaAdmin)
admin.site.register(models.Candidate, CandidateAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Hostel, HostelAdmin)
admin.site.register(models.Comment, CommentAdmin)
