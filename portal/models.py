from django.db import models
from django.contrib.auth.models import User
from . import choices


class Junta(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField()
    role = models.CharField(max_length=32, choices=choices.ROLES_CHOICES, default=choices.VOTER)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class Candidate(models.Model):
    user = models.ForeignKey(Junta, on_delete=models.CASCADE, related_name='candidate')
    bio = models.TextField()
    position = models.CharField(max_length=64, choices=choices.POSITION_CHOICES, default=choices.VP)
    videos = models.FileField()
    agenda = models.FileField()
    key_points = models.TextField()

    def __str__(self):
        return '{} {}'.format(self.user.user.first_name, self.user.user.last_name)


class Question(models.Model):
    asked_by = models.ForeignKey(Junta, on_delete=models.CASCADE, related_name='questions_submitted')
    asked_to = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='question_asked')
    question = models.CharField(max_length=1024)
    approved = models.BooleanField(default=False)
    answer = models.TextField()
    answered = models.BooleanField(default=False)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    class Meta:
        ordering = ['upvotes']

    def __str__(self):
        return '{}'.format(self.question)


class Hostel(models.Model):
    name = models.CharField(max_length=64)
    total_residents = models.IntegerField(default=0)
    no_of_votes = models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.name)

