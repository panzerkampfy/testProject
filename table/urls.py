from django.urls import path

from table.views import TaskViewSet, ColumnViewSet, BoardViewSet, PermissionViewSet

urlpatterns = [
    path('tasks/<int:pk>/', TaskViewSet.as_view({'put': 'update',
                                                 'delete': 'destroy',
                                                 'get': 'tasks_list'}), name='tasks_actions'),
    path('tasks/', TaskViewSet.as_view({'post': 'create'}), name='tasks_actions'),

    path('columns/<int:pk>/', ColumnViewSet.as_view({'put': 'update',
                                                     'delete': 'destroy',
                                                     'get': 'column_list'}), name='columns_actions'),
    path('columns/', ColumnViewSet.as_view({'post': 'create'}), name='columns_actions'),

    path('boards/<int:pk>/', BoardViewSet.as_view({'put': 'update',
                                                   'delete': 'destroy'}), name='boards_actions'),
    path('boards/', BoardViewSet.as_view({'get': 'list',
                                          'post': 'create'}, name='boards_actions')),

    path('permissions/', PermissionViewSet.as_view({'put': 'permission_update'}), name='permissions_actions'),
]
