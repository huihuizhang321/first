from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/crm/', include('crm.urls')),
    path('api/chat/', include('chat.urls')),
]
