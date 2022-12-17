from django.db import models
from django.contrib.auth.models import User


class Submissions(models.Model):
    ACCEPTANCE_STATUS = [
        ("S", "Success"),
        ("E", "Error"),
        ("P", "Pending")
    ]
    LANGUAGE_CHOICE = [
        ('py', 'python'),
        ('cpp', 'cpp')
    ]
    name = models.CharField(max_length=100, default="temp")
    code = models.TextField(max_length=20000)
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICE)
    submission_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=ACCEPTANCE_STATUS)
    user_input = models.CharField(max_length=1000, null=True, blank=True)
    user_output = models.CharField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, related_name='owned_submission', on_delete=models.CASCADE, null=False)
    share_with = models.ManyToManyField(User, related_name='shared_submissions')

    def __str__(self):
        return f'{self.language}\n{self.code}'
