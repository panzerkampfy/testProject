from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from table.views import TaskViewSet, ColumnViewSet, PermissionViewSet, \
    BoardViewSet, NewTaskViewSet, NewColumnViewSet, \
    NewBoardViewSet

router = SimpleRouter()
router.register('api_v1/tasks', TaskViewSet)
router.register('api_v1/columns', ColumnViewSet)
router.register('api_v1/boards', BoardViewSet)
router.register('api_v1/permissions', PermissionViewSet)

# new_router = SimpleRouter()
# new_router.register('api_v2/tasks', NewTaskViewSet)
# new_router.register('api_v2/columns', NewColumnViewSet)
# new_router.register('api_v2/boards', NewBoardViewSet)
# new_router.register('api_v2/permissions', PermissionViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))
] + router.urls