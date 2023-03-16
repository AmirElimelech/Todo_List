from django.urls import path
from .views.API_views import task_list_api, task_detail_api
from .views.login_views import CustomLoginView, CustomLogoutView, SignUp
from .views.task_views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete
from django.contrib.auth import views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('reset_password/',views.PasswordResetView.as_view(template_name = "../templates/base/reset_password.html") , name = "reset_password"),
    path('reset_password_sent/',views.PasswordResetDoneView.as_view(template_name = "../templates/base/reset_password_sent.html") , name = "password_reset_done"),
    path('reset/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(template_name = "../templates/base/reset.html") , name = "password_reset_confirm"),
    path('reset_password_complete/',views.PasswordResetCompleteView.as_view(template_name = "../templates/base/reset_password_complete.html") , name = "password_reset_complete"),

    
   

    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),


    path('api/', task_list_api, name='task-list-api'),
    path('api/<int:pk>/', task_detail_api, name='task-detail-api'),



]