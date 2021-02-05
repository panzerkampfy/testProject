from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from table.views import TaskViewSet, ColumnViewSet, PermissionViewSet, BoardViewSet

router = SimpleRouter()
router.register('api/v1/tasks', TaskViewSet)
router.register('api/v1/columns', ColumnViewSet)
router.register('api/v1/boards', BoardViewSet)
router.register('api/v1/permissions', PermissionViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls'))
] + router.urls