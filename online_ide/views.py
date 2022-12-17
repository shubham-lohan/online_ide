from django.http import HttpResponse
from .models import *
from django.shortcuts import redirect, render
from .forms import SubsmissionForm
import subprocess
import uuid
from django.contrib.auth.decorators import login_required
from .models import Submissions


def index(request):
    if request.user.is_authenticated:
        return redirect(home)
    return render(request, "index.html")


@login_required
def home(request):
    context = {}
    context['form'] = SubsmissionForm()
    context['user'] = request.user
    if request.method == 'POST':
        form = SubsmissionForm(request.POST or None)
        context['form'] = form
        code = (form['code']).data
        language = form['language'].data
        filename = str(uuid.uuid4())+"."+language
        with open(filename, 'w') as file:
            file.write(code)
        input_filename = str(uuid.uuid4())+".in"
        with open(input_filename, 'w') as file:
            file.write(form['user_input'].data)
        if language == 'py':
            result = subprocess.run(['python', filename], capture_output=True, stdin=open(input_filename))
            if result.returncode == 1 or result.returncode != 0:
                context['output'] = result.stderr.decode()
            else:
                context['output'] = result.stdout.decode()
        if language == 'cpp':
            result = subprocess.run(['g++', filename, '-o', filename[:-4]], capture_output=True)
            if result.returncode == 1 or result.returncode != 0:
                # compile time error:1
                # run time error!=0
                context['output'] = result.stderr.decode()
            else:
                result = subprocess.run(["./"+filename[:-4]], capture_output=True, stdin=open(input_filename))
                context['output'] = result.stdout.decode()
            subprocess.run(['rm', filename[:-4]])
        subprocess.run(['rm', filename, input_filename])
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.user_output = result.stdout.decode()
            instance.name = form['name'].data
            instance.save()
        return render(request, "home.html", context)
    return render(request, "home.html", context)


@login_required
def show_submissions(request, submission_id):
    submission = Submissions.objects.get(id=submission_id)
    print(submission.user, request.user)
    if submission.user != request.user and (submission.user != request.user and request.user not in submission.share_with.all()):
        return HttpResponse("<h1>Invalid Access</h1>")
    # submission.code = submission.code.encode('utf-8')
    # # print(submission.code.encode('utf-8'))
    if request.method == 'POST':
        print(request.POST)
        people = request.POST['share_with']
        user = User.objects.filter(email=people).first()
        print("user", user)
        if user:
            submission.share_with.add(user)
            submission.save()
    users = User.objects.all()
    print(users)
    return render(request, "show_submissions.html", {'submission': submission,
                                                     'share_with': submission.share_with.all(),
                                                     'users': users
                                                     })


@login_required
def my_submissions(request):
    submissions = Submissions.objects.filter(user=request.user).order_by('-submission_time')
    context = {'submissions': submissions}
    return render(request, "my_submissions.html", context)
