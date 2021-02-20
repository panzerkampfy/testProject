from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('table.urls')),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('dj_rest_auth.urls')),
    # path('api/v1/registration/', include('dj_rest_auth.registration.urls'))
]