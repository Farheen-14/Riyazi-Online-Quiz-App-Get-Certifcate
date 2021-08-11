from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('home/',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('payment/',views.payment,name='payment'),
    path('instruction/',views.instruction,name='instruction'),
    path('quiz/',views.quiz,name='quiz'),
    path('question/',views.question,name='question'),
    path('congrats/',views.congrats,name='congrats'),
    path('footer1/',views.footer1,name='footer1'),
    path('pdf/',views.certificate,name='certificate')

] 

# for media file saved
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
