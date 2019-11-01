from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views as user_views

urlpatterns = [
    path('', views.ProfileListView, name='home'),
    path('search/', views.ProfileSearchView, name='profile_search'),
    path('register/', user_views.register, name='register'),
    path('profile/<int:pk>/', user_views.ProfileDetailView, name='profile_view'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('contact/<int:pk>/', views.contact, name='profile_contact'),
]
