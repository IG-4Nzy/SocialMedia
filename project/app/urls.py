from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import send_message


urlpatterns=[
    path("",views.base,name="base"),
    path("home",views.home,name="home"),
    path("changepass",views.changepass,name="changepass"),
    path("chat",views.chat,name="chat"),
    path("post",views.post,name="post"),
    path("profile",views.profile,name="profile"),
    path("settings",views.settings,name="settings"),
    path("signin/",views.signin,name="signin"),
    path("signup",views.signup,name="signup"),
    path("userlist",views.userlist,name="userlist"),
    path('sign', views.sign,name='sign'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.log, name='log'),
    path('send_message/<int:receiver_id>/', send_message, name='send_message'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)