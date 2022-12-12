from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=100)


class Submissions(models.Model):
    ACCEPTANCE_STATUS = [
        ("S", "Success"),
        ("E", "Error"),
        ("P", "Pending")
    ]
    code = models.CharField(max_length=2000)
    language = models.CharField(max_length=100)
    submissions_time = models.DateField(auto_now=True)
    status = models.CharField(max_length=1, choices=ACCEPTANCE_STATUS)
    user_input = models.CharField(max_length=1000, null=True, blank=True)
    user_output = models.CharField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
