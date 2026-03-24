from django.shortcuts import render

# Create your views here.
from .models import Project, Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.db.models import Case, When, Value, IntegerField

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'dashboard/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('dashboard')

    return render(request, 'dashboard/signup.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):

    total_projects = Project.objects.filter(user=request.user).count()
    total_tasks = Task.objects.filter(user=request.user).count()

    completed_tasks = Task.objects.filter(
        user=request.user,
        status='Completed'
    ).count()

    pending_tasks = Task.objects.filter(
        user=request.user,
        status='Pending'
    ).count()

    inprogress_tasks = Task.objects.filter(
        user=request.user,
        status='In Progress'
    ).count()

    tasks = Task.objects.filter(user=request.user)

    context = {
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'inprogress_tasks': inprogress_tasks,
        'tasks': tasks,
    }

    return render(request, 'dashboard/dashboard.html', context)
@login_required
def projects_view(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'dashboard/projects.html', {'projects': projects})

@login_required
def tasks_view(request):

    tasks = Task.objects.filter(user=request.user)

    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')

    # Filtering
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    # ✅ STATUS ORDER
    tasks = tasks.annotate(
        status_order=Case(
            When(status='Pending', then=0),
            When(status='In Progress', then=1),
            When(status='Completed', then=2),
            output_field=IntegerField(),
        )
    )

    # ✅ PRIORITY ORDER
    tasks = tasks.annotate(
        priority_order=Case(
            When(priority='High', then=0),
            When(priority='Medium', then=1),
            When(priority='Low', then=2),
            output_field=IntegerField(),
        )
    )

    # ✅ FINAL SORTING
    tasks = tasks.order_by('status_order', 'priority_order')

    return render(request, 'dashboard/tasks.html', {'tasks': tasks})
@login_required
def update_status(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)

    if request.method == "POST":
        new_status = request.POST.get("status")
        task.status = new_status
        task.save()

    return redirect('tasks')



@login_required
def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    tasks = Task.objects.filter(project=project, user=request.user)

    completed = tasks.filter(status="Completed").count()
    pending = tasks.filter(status="Pending").count()
    inprogress = tasks.filter(status="In Progress").count()

    context = {
        "project": project,
        "tasks": tasks,
        "completed": completed,
        "pending": pending,
        "inprogress": inprogress,
    }

    return render(request, "dashboard/project_detail.html", context)