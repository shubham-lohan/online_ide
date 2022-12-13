from django.db import models


# class User(models.Model):
#     full_name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.full_name


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
    code = models.TextField(max_length=20000)
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICE)
    submissions_time = models.DateField(auto_now=True)
    status = models.CharField(max_length=1, choices=ACCEPTANCE_STATUS)
    user_input = models.CharField(max_length=1000, null=True, blank=True)
    user_output = models.CharField(max_length=1000, null=True, blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.language}\n{self.code}'
