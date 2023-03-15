from django.urls import path
from .views.API_views import task_list_api, task_detail_api
from .views.login_views import CustomLoginView, CustomLogoutView, SignUp
from .views.task_views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),


    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),


    path('api/', task_list_api, name='task-list-api'),
    path('api/<int:pk>/', task_detail_api, name='task-detail-api'),
]