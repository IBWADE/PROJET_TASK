from django.contrib import admin
from django.urls import path
from maintenance import views

urlpatterns = [
    path('home',views.dashboard,name="home"),
    path('users',views.Users,name="users"),
    path('users_bis',views.Users_bis,name="users_bis"),
    path('user_profil',views.user_profil,name="user_profil"),
    path('tasks',views.tasks_gestion,name="tasks"),
    path('delete_user/<int:id>',views.delete_user,name="delete_user"),
    path('manage_tasks',views.manage_task,name="manage"),
    path('edit_task/<int:id>',views.edit_task,name="edit_task"),
    path('delete_task/<int:id>',views.delete_task,name="delete_task"),
    path('news',views.news,name="news"),
    path('delete_post/<int:id>',views.delete_post,name="delete_post"),
    path('detail_post/<int:id>',views.detail_post,name="detail_post"),
    path('like_post',views.like_post,name="like_post"),
    path('edit_post/<int:id>',views.edit_post,name="edit_post"),
    path('update_mypassword/<int:id>',views.update_password,name="update_password"),
    path('users/<int:id>',views.single_user,name="single_user"),
    path('users_bis/<int:id>',views.single_user_bis,name="single_user_bis"),
    path('search/<int:id>',views.search,name="search"),
   
]
