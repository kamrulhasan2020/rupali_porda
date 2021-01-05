from django.contrib.auth import views as auth_views
from django.urls import path
from .views import SignUpView

app_name = 'user'
urlpatterns = [
    path('signup/', SignUpView.as_view(template_name='user/signup.html'), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
]
