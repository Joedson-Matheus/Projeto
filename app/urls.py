from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('page_accontLogin/', views.page_accontLogin, name='page_accontLogin'),
    path('page_accontCreate/', views.page_accontCreate, name='page_accontCreate'),
    path('home/', views.page_home, name='page_home'),
    path('filme/<int:id>', views.page_move, name='page_move'),
    path('planos/', views.page_planos, name='page_planos'),
    path('perfil/', views.page_profileUser, name='page_profileUser'),
    path('ver-perfil/', views.page_viewProfileUser, name='page_viewProfileUser'),
    path('login-acao/', views.run_accontLogin, name='run_accontLogin'),
    path('create-acao/', views.run_CreateAccont, name='run_CreateAccont'),
    
     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
