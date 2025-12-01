from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.db.models import Case, When, Value, CharField, F
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.contrib.auth.models import User
from .models import Tasks


# Create your views here.
#go to login page
def logIn(request):
    return render(request, 'login.html')

#check login
def loggingin(request):
    if request.method == 'POST':
        username= request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['storeId'] = request.user.id
            return redirect("taskList")
        else:
            return render(request, 'login.html', {'message': 'invalid email or password'})
        return render(request, 'login.html', {'message': 'something went wrong'})

def signup(request):
    return render(request, 'signup.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not password or not email or not name or not confirm_password:
            return render(request, 'signup.html', {'message': 'All the fields are required'})
        if User.objects.filter(email=email).exists():
            return render(required, 'signup.html', {'message': 'email already registered'})
        if password != confirm_password:
            return render(request, 'signup.html', {'message': 'new password and confirm password does not match'})
        User.objects.create_user(username=email, email=email, password=password)
        return render(request, 'login.html', {'message': 'Registered successfully. Please login now.'})
    return render(request, 'signup.html', {'message': 'something went wrong, please try again'})

#go to the tasks form page to create or edit
def taskForm(request):
    return render(request, 'taskForm.html')

#create tasks
def createTask(request):
    try:
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            due_date = request.POST.get('due_date')
            is_complete = request.POST.get('complete')
            priority = request.POST.get('dropdown')
            is_completed= 1 if request.POST.get("complete") == "1" else 0
            task_id = request.POST.get("id")
            if task_id:
                Tasks.objects.filter(id=task_id).update(title = title, description =description, due_date=due_date,is_completed=is_completed, version=F('version')+1)
                data = Tasks.objects.get(id=task_id)
            else:
                data = Tasks.objects.create(title = title, description =description, due_date=due_date,is_completed=0, owner_id = request.session.get('storeId'))
            return render(request, 'taskForm.html', {'data': data, 'message':'hello'})
        return render(request, 'taskForm.html', {'message': 'something whent wrong.'})
    except Exception as e:
        return render(request, 'taskForm.html', {'message': e})

#edit page
def taskEdit(request, id):
    try:
        data = Tasks.objects.filter(id=id).first()
        return render(request, 'taskForm.html', {'data': data})
    except Exception as e:
        return render(request, 'tasks.html', {'message': e})


def task_list(request):
    try:
        today = now().date()
        if request.user.is_superuser: 
            task = Tasks.objects.filter(owner_id=request.session.get('storeId')).annotate(
                status=Case(When(due_date__lt=today, then=Value("Overdue")), default=Value("In Progress"), output_field=CharField())
            ).order_by('-created_at')
        else:
            task = Tasks.objects.filter(owner_id=request.user.id, is_completed = 0, is_deleted = False).annotate(
                status=Case(When(due_date__lt=today, then=Value("Overdue")), default=Value("In Progress"), output_field=CharField())
            ).order_by('-created_at')
        paginator = Paginator(task, 10) 

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "tasks.html", {"fetchData": page_obj})
    except Exception as e:
        return render(request, 'tasks.html', {"message":e})

#delete task
def deleteTask(request):
    try:
        page = request.POST.get('page')
        delete = request.POST.get('delete')
        task_id = request.POST.get('task_id')
        submit = request.POST.get('submit')
        if submit == "OK":
            if delete:
                Tasks.objects.filter(id=task_id).update(is_deleted = True)
            else:
                Tasks.objects.filter(id=task_id).update(is_deleted = False)
        return redirect('taskList')
    except Exception as e:
        return render(request, 'tasks.html', {"message":e})

#view all users
def userList(request):
    try:
        if not request.user.is_superuser: 
            return render(request, 'login.html', {'message':'something whent wrong'})
        user = User.objects.all()
        paginator = Paginator(user, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "userList.html", {"fetchData": page_obj})
    except Exception as e:
        return render(request, 'userList.html', {"message":e})

#get user tasks by admin
def viewUserTasks(request, id):
    try:
        if not request.user.is_superuser:
            return render(request, 'login.html', {'message', 'Something whent wrong, please login again'})
        return redirect('taskList')
    except Exception as e:
        return render(request, 'userList.html', {'message': e})
        request.session['storageId'] = id

#logout
def logout(request):
    try:
        logout(request)
        return render(request, 'login.html', {'message': 'logout successfully'})
    except Exception as e:
        return render(request, 'login.html')