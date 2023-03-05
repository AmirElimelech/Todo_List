
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , DeleteView , UpdateView ,FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView , LogoutView 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.conf import settings
from .serializers import TaskSerializer
from . models import Task
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse ,HttpResponse
from rest_framework import generics

@csrf_exempt
def task_list_api(request):
    if request.method == "POST":
        pass
    elif request.method == "GET":
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)
    
@csrf_exempt
def task_detail_api(request, pk):
    if request.method == "POST":
        pass 
    elif request.method == "GET":
        task = Task.objects.get(id=pk)
        serializer = TaskSerializer(task)
        return JsonResponse(serializer.data ,safe=False)
    


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        self.request.session['username'] = self.request.user.username
        return reverse_lazy('tasks')


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''


class SignUp(FormView):
    template_name = "base/signup.html"
    form_class = CustomUserCreationForm # we have just inherited from this builtin Form
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            # send confirmation email
            subject = 'Welcome to My To Do List!'
            message = 'Thank you for signing up!'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


    def get_form(self, form_class= None):
        form = super().get_form(form_class)
        del form.fields['password2']
        return form




class CustomLogoutView(LogoutView):
    def get_default_redirect_url(self):
        return reverse_lazy ('login')


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        context['completed'] = context['tasks'].filter(complete=True)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        context['username'] = self.request.session.get('username', 0)

        view_count = self.request.session.get('view_count',0)+1
        self.request.session['view_count'] = view_count
        self.request.session.modified = True
        context['view_count'] = view_count
        return context



class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form): # instead of choosing the user who created the task
                                # this auto changes it to the logged user without having to 
                                # take care of changing it by your self everytime . 
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task 
    context_object_name = 'task'
    success_url = reverse_lazy ('tasks')

    