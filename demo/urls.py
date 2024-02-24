from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from demo import views

urlpatterns = [
    path('', views.login, name="login"),
    path('app/', views.app, name="app"),
    path('generate/', views.generate, name="generate"),
    path('generate_inpaint/', views.generate_inpaint, name="generate_inpaint"),
    path('replace_inpaint/', views.replace_inpaint, name="replace_inpaint"),
    path('cdn/celebbrowser', views.celeb_browser, name='celeb_browser'),
    path('cdn/brushtool', views.brush_tool, name='brush_tool')] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
