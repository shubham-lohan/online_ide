from django.http import HttpResponse
from .models import *
from django.shortcuts import redirect, render
from .forms import SubsmissionForm
import subprocess
import uuid


def index(request):
    context = {}
    form = SubsmissionForm(request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    print(form)
    code = (form['code']).data
    language = form['language'].data
    filename = str(uuid.uuid4())+"."+language
    with open('code_files/'+filename, 'w') as file:
        file.write(code)
    if language == 'py':
        result = subprocess.run(['python', "code_files/"+filename], capture_output=True)
        if result.returncode == 1 or result.returncode != 0:
            context['output'] = result.stderr.decode()
        else:
            context['output'] = result.stdout.decode()
    if language == 'cpp':
        result = subprocess.run(['g++', "code_files/"+filename], capture_output=True)
        if result.returncode == 1 or result.returncode != 0:
            # compile time error:1
            # run time error!=0
            context['output'] = result.stderr.decode()
        else:
            result = subprocess.run(["a.exe"], capture_output=True)
            context['output'] = result.stdout.decode()
    return render(request, "index.html", context)
