from django import forms

from online_ide.models import *


class SubsmissionForm(forms.ModelForm):
    class Meta:
        model = Submissions
        fields = ['code', 'language', 'user_input']
