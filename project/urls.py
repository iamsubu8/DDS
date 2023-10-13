
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Login,name='login'),
    path('signup',views.SignUp,name='signup'),
    path('create-folder/', views.MyDrive, name='myDrive'),
    path('create-folder/<int:parent_id>/', views.MyDrive, name='myDrive'),
    path('logout', views.Logout),
    path('rmv/<int:parent_id>', views.Delete),
    path('update/<int:parent_id>', views.Update),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
