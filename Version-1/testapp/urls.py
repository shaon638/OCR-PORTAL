from django.urls import path
from testapp import views

urlpatterns = [
    path('', views.homePage, name = "home"),
    path('about/', views.aboutPage, name = "about"),
    path('contact/', views.contactPage, name = "contact"),
    path('signup/', views.register, name = "reg"),
    path("check_user/",views.checkUser, name = "check_user"),
    path("login_user/", views.login_user, name = "login_user"),
    path("user_dashboard/",views.user_dashboard, name = "user_dashboard"),
    path("user_logout/", views.user_logout, name = "user_logout"),
    path("edit_profile/", views.edit_Profile, name = "edit_profile"),
    path("change_password/", views.changePassword, name = "change_password"),
    path("add_form/", views.add_form_view, name = "add_form_view"),
    path("myform/", views.my_forms, name = "myform"),


]