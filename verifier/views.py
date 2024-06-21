from rest_framework.response import Response
from django.shortcuts import render, redirect
# Create your views here.
from django.views.generic import ListView
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from verifier.models import TaskObject, VerificationTaskResult
from verifier.serializers import TaskSerializer
from .utils import assign_task_to_verifier
from .forms import CustomLoginForm, SignUpForm
from django.contrib.auth import authenticate, login


##### Create Task
class TaskCreateView(CreateAPIView):
    serializer_class = TaskSerializer
    queryset = TaskObject.objects.all()

    def perform_create(self, serializer):
        # Save the task object
        serializer.save()

        # Call the task assignment function
        assign_task_to_verifier()
        

        return super().perform_create(serializer)

class TaskListView(ListView):
    model = TaskObject
    template_name = 'task_page.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # Assuming a field 'assigned_to' in TaskObject model
        return VerificationTaskResult.objects.filter(tagged_by=self.request.user, completed=False, task__state=TaskObject.PENDING).select_related('task')


#### Post Task Result
@api_view(['POST'])
def post_task_result(request, pk):
    task = TaskObject.objects.get(id=pk)
    print("user",request.user.id)
    data = request.data
    task_result = VerificationTaskResult.objects.filter(task=task, tagged_by=request.user).first()
    task_result.tag = data['tag']
    task_result.completed = True
    task_result.save()
    task.state = TaskObject.COMPLETED
    task.save()
    return Response(status=200, data={"message": "Task Completed"})


##### Fetch result of a Task
@api_view(['GET'])
def get_task_result(request, pk):
    task = TaskObject.objects.get(id=pk)
    if task.state == TaskObject.COMPLETED:
        task_result = VerificationTaskResult.objects.get(task=task, completed=True)
        return Response(status=200, data={"tag": task_result.tag})

    else:
        ## return error 400
        return Response(status=400, data={"message": "Task Not Completed"})


def task_form_view(request):
    # This view renders the HTML template with the task creation form
    return render(request, 'create_task.html')



###### fetch active assigned task


def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/tasks/')  # Redirect to /tasks/ after successful login
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after successful registration
            return redirect('/tasks/')  # Redirect to /tasks/ after registration
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})
