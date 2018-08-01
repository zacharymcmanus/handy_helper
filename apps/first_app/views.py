from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "first_app/login.html")

def register(request):
    if request.method == 'POST':
        errors = User.objects.user_val(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='registration_errors')
            return redirect('/')
        else: 
            password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=password_hash)
            user = User.objects.get(email=request.POST['email'])
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['email'] = user.email
            request.session['id'] = user.id
            print ("==========successfully registered========")
            return redirect('/dashboard')    

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if not len(user):
        errors = User.objects.login_val(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='login_errors')
        return redirect('/')
    if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
        user_login = User.objects.get(email=request.POST['email'])
        request.session['first_name'] = user_login.first_name
        request.session['last_name'] = user_login.last_name
        request.session['email'] = user_login.email
        request.session['id'] = user_login.id
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect("/")

def dashboard(request):    
    if 'id' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=request.session['id'])
        user_jobs = Job.objects.filter(join=user)
        all_jobs = Job.objects.all()
        context = {
            'user': user,
            'user_jobs': user_jobs,
            'all_jobs': all_jobs,
        }
        return render(request, 'first_app/dashboard.html', context)

def show_add_job(request):
    return render(request, 'first_app/add_job.html')

def add_job(request):
    if request.method == 'POST':
        errors = Job.objects.job_val(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='add_job_errors')
            return redirect('/show_add_job')
        else:
            job = Job.objects.create(
                job_name=request.POST['job_name'],
                job_description=request.POST['job_description'],
                job_location=request.POST['job_location'],
                creator=User.objects.get(id=request.session['id']),
                )
            job.save()
            job.join.add(User.objects.get(id=request.session['id']))
            return redirect("/dashboard")        

def show_edit_job(request, id):
    if "id" not in request.session:
        return redirect("/")
    else:
        context = {
            'job': Job.objects.get(id=id)
        }
    return render(request, 'first_app/edit_job.html', context)

def edit_job(request, id):
    if request.method == 'POST':
        errors = Job.objects.job_val(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='edit_job_errors')
            return redirect('/dashboard')
        else:
            job = Job.objects.get(id=id)
            job.job_name=request.POST['job_name']
            job.job_description=request.POST['job_description']
            job.job_location=request.POST['job_location']
            job.save()
            return redirect("/dashboard") 
    
def complete_job(request, id):
    job_to_delete = Job.objects.filter(id=id)
    job_to_delete.delete()
    return redirect('/dashboard')

def view_job(request, id):
    job = Job.objects.get(id=id)
    context = {
        'job': job,
    }
    return render(request, "first_app/view_job.html", context)

def join_job(request, id):
    this_user = User.objects.get(id=request.session["id"])
    this_job = Job.objects.get(id=id)
    this_job.join.add(this_user)
    print('==============successfully joined job==============')
    return redirect('/dashboard')

def cancel_job(request, id):
    this_user = User.objects.get(id=request.session['id'])
    this_job = Job.objects.get(id=id)
    this_job.join.remove(this_user)
    print('==============successful cancel==============')
    return redirect('/dashboard')



        







