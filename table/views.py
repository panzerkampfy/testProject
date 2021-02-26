from rest_framework import permissions as base_permissions
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from table import permissions as table_permissions
from table.models import Task, Column, Board, PermissionOnBoard
from table.selializers import TaskSerializer, TaskListSerializer, BoardSerializer, PermissionSerializer, \
    ColumnSerializer, ColumnListSerializer
from .views_helpers import get_fact_today as fact
from .views_helpers import get_weather_today as weather


class BaseViewSet(viewsets.ModelViewSet):
    serializer_map: dict = None

    def get_serializer_class(self):
        if not self.serializer_map:
            raise NotImplementedError('serializer_map must be implement')
        return self.serializer_map[self.action]

    permission_map: dict = None


class PermissionViewSet(BaseViewSet):
    queryset = PermissionOnBoard.objects.all()
    serializer_map = {
        'permission_update': PermissionSerializer
    }
    permission_map = {
        'permission_update': (base_permissions.IsAuthenticated,
                              (table_permissions.IsOwner |
                               table_permissions.IsAdmin)
                              ),
    }

    def get_permissions(self):
        if not self.permission_map:
            raise NotImplementedError('permission_map must be implement')
        return [permission() for permission in self.permission_map[self.action]]

    @action(detail=False, methods=['PUT', 'PATCH'])
    def permission_update(self, request):
        data = request.data
        self.check_object_permissions(request, board_obj_permission(request.user.id, data.get('board')))
        obj = self.get_queryset().filter(
            board=data.get('board'),
            user=data.get('user')
        ).first()
        if obj is not None:
            serializer = self.get_serializer(obj, data=data)
        else:
            serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


def task_obj_permission(id, pk) -> PermissionOnBoard:
    column_id = Task.objects.get(id=pk).column.id
    return column_obj_permission(id, column_id)


def column_obj_permission(id, pk) -> PermissionOnBoard:
    board_id = Column.objects.get(id=pk).board.id
    return board_obj_permission(id, board_id)


def board_obj_permission(id, pk) -> PermissionOnBoard:
    obj = PermissionOnBoard.objects.filter(user_id=id, board_id=pk).first()
    return obj


class TaskViewSet(BaseViewSet):
    queryset = Task.objects.all()
    serializer_map = {
        'tasks_list': TaskListSerializer,
        'create': TaskSerializer,
        'update': TaskSerializer
    }
    permission_map = {
        'tasks_list': (base_permissions.IsAuthenticated,
                       (table_permissions.IsVisitor |
                        table_permissions.IsMember |
                        table_permissions.IsOwner |
                        table_permissions.IsAdmin)
                       ),
        'create': (base_permissions.IsAuthenticated,
                   (table_permissions.IsMember |
                    table_permissions.IsOwner |
                    table_permissions.IsAdmin)
                   ),
        'update': (base_permissions.IsAuthenticated,
                   (table_permissions.IsMember |
                    table_permissions.IsOwner |
                    table_permissions.IsAdmin)
                   ),
        'destroy': (base_permissions.IsAuthenticated,
                    (table_permissions.IsMember |
                     table_permissions.IsOwner |
                     table_permissions.IsAdmin)
                    )
    }

    @action(detail=True, methods=['GET'])
    def tasks_list(self, request, pk):
        try:
            Column.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request, column_obj_permission(request.user.id, pk))
        objs = self.get_queryset().filter(column=pk)
        serializer = self.get_serializer(objs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            Column.objects.get(id=request.data.get('column'))
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request, column_obj_permission(request.user.id, request.data.get('column')))
        data = self.request.data
        data['fact'] = fact()
        data['weather'] = weather(request.user.id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        try:
            obj = self.get_queryset().get(id=pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request, task_obj_permission(request.user.id, pk))
        data = request.data
        if data.get('column'):
            data['text'] = obj.text
            try:
                column_id = Column.objects.get(id=data.get('column')).id
                self.check_object_permissions(request, column_obj_permission(request.user.id, column_id))
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif data.get('text'):
            data['column'] = obj.column.id
        serializer = TaskSerializer(obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk):
        try:
            task = self.get_queryset().get(pk=pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request, task_obj_permission(request.user.id, pk))
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ColumnViewSet(BaseViewSet):
    queryset = Column.objects.all()
    serializer_map = {
        'column_list': ColumnListSerializer,
        'column_create': ColumnSerializer,
        'update': ColumnSerializer
    }

    permission_map = {
        'column_list': (base_permissions.IsAuthenticated,
                        (table_permissions.IsVisitor |
                         table_permissions.IsMember |
                         table_permissions.IsOwner |
                         table_permissions.IsAdmin)
                        ),
        'column_create': (base_permissions.IsAuthenticated,
                          (table_permissions.IsMember |
                           table_permissions.IsOwner |
                           table_permissions.IsAdmin)
                          ),
        'update': (base_permissions.IsAuthenticated,
                   (table_permissions.IsMember |
                    table_permissions.IsOwner |
                    table_permissions.IsAdmin)
                   ),
        'destroy': (base_permissions.IsAuthenticated,
                    table_permissions.IsOwner
                    ),
    }

    @action(detail=True, methods=['GET'])
    def column_list(self, request, pk):
        self.check_object_permissions(request, board_obj_permission(request.user.id, pk))
        objs = self.get_queryset().filter(board=pk)
        serializer = self.get_serializer(objs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def column_create(self, request):
        try:
            board_id = request.data.get('board')
            board = Board.objects.get(id=board_id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request, board_obj_permission(request.user.id, board_id))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        try:
            obj = self.get_queryset().get(pk=pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request, column_obj_permission(request.user.id, pk))
        data = request.data
        serializer = self.get_serializer(obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk):
        try:
            column = self.get_queryset().get(pk=pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request, column_obj_permission(request.user.id, pk))
        column.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BoardViewSet(BaseViewSet):
    queryset = Board.objects.all()
    serializer_map = {
        'list': BoardSerializer,
        'create_board': BoardSerializer,
        'update': BoardSerializer
    }

    permission_map = {
        'list': (base_permissions.IsAuthenticated,
                 (table_permissions.IsVisitor |
                  table_permissions.IsMember |
                  table_permissions.IsOwner |
                  table_permissions.IsAdmin)
                 ),
        'update': (base_permissions.IsAuthenticated,
                   (table_permissions.IsOwner |
                    table_permissions.IsAdmin)
                   ),
        'create_board': (base_permissions.IsAuthenticated,),
        'destroy': (base_permissions.IsAuthenticated,
                    (table_permissions.IsOwner |
                     table_permissions.IsAdmin)
                    )
    }

    def list(self, request):
        boards = self.get_queryset().filter(users=request.user)
        serializer = self.get_serializer(boards, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def create_board(self, request):
        data = request.data
        board_serializer = self.get_serializer(data=data)
        board_serializer.is_valid(raise_exception=True)
        board_serializer.save()

        permission_data = {'board': board_serializer.data.get('id'), 'user': request.user.id, 'permission': "1"}
        permission_serializer = PermissionSerializer(data=permission_data)
        permission_serializer.is_valid(raise_exception=True)
        permission_serializer.save()

        return Response(data=board_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk, *args, **kwargs):
        try:
            board = self.get_queryset().get(pk=pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request, board_obj_permission(request.user.id, pk))
        data = request.data
        serializer = self.get_serializer(board, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk):
        try:
            board = self.get_queryset().get(pk=pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request, board_obj_permission(request.user.id, pk))
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
