from django import forms

from online_ide.models import *


class SubsmissionForm(forms.ModelForm):
    class Meta:
        model = Submissions
        fields = ['name', 'language', 'code',  'user_input']
