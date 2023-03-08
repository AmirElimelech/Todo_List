
from django import forms
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView, FormView,
                                       UpdateView)
from django.views.generic.list import ListView
from rest_framework import generics ,status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer

@api_view(['GET','POST'])  #list of methods that are allowed are GET and POST .. if delete is not 
                           # mentioned above ---> means that once delete is choosen it will show 
                           # error 
@csrf_exempt
def task_list_api(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = status.HTTP_201_CREATED )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST )
    elif request.method == "GET":
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)

# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# @csrf_exempt
# def task_detail_api(request, pk):
#     try:
#         task = Task.objects.get(id=pk)
#         data = JSONParser().parse(request)
#     except Task.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = TaskSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == "PUT":
#         serializer = TaskSerializer(task, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == "DELETE":
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET','POST'])  #list of methods that are allowed are GET and POST .. if delete is not 
#                            # mentioned above ---> means that once delete is choosen it will show 
#                            # error 
# @csrf_exempt
# def task_list_api(request):
#     if request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = TaskSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status = status.HTTP_201_CREATED )
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST )
#     elif request.method == "GET":
#         tasks = Task.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return JsonResponse(serializer.data, safe=False)

# # @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# # @csrf_exempt
# # def task_detail_api(request, pk):
# #     try:
# #         task = Task.objects.get(id=pk)
# #         data = JSONParser().parse(request)
# #     except Task.DoesNotExist:
# #         return Response(status=status.HTTP_404_NOT_FOUND)

# #     if request.method == "GET":
# #         serializer = TaskSerializer(task)
# #         return Response(serializer.data)
# #     elif request.method == "POST":
# #         serializer = TaskSerializer(data=data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #     elif request.method == "PUT":
# #         serializer = TaskSerializer(task, data=data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #     elif request.method == "DELETE":
# #         task.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)
    

# class TaskDetailApi(APIView):

#     def get_object(self, pk):
#         try:
#             return Task.objects.get(pk=pk)
#         except Task.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)

#     def post(self, request, pk):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         task = self.get_object(pk)
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

            

# # class TaskListAPI(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
# #     queryset = Task.objects.all()
# #     serializer_class = TaskSerializer

# #     def get(self, request, *args , **kwargs):
# #         return self.list(request, *args , **kwargs)

# #     def post(self, request, *args , **kwargs):
# #         return self.create(request, *args , **kwargs)

# # class TaskDetailAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
# #     queryset = Task.objects.all()
# #     serializer_class = TaskSerializer

# #     def get(self, request, pk):
# #         return self.retrieve(request, pk)

# #     def put(self, request, pk):
# #         return self.update(request, pk)

# #     def delete(self, request, pk):
# #         return self.destroy(request, pk)





@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@csrf_exempt
def task_detail_api(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = TaskSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

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

    