from django.db import transaction
from rest_framework import permissions as base_permissions
from table import permissions as table_permissions
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from table.models import Task, Column, Board, PermissionOnBoard, TaskColumn, ColumnBoard
from table.selializers import TaskSerializer, TaskShowSerializer, \
    ColumnSerializer, ColumnListSerializer, \
    BoardSerializer, BoardListSerializer, BoardShowSerializer, \
    PermissionSerializer, BoardFullSerializer, TaskListSerializer, ColumnShowSerializer
from table.selializers import NewTaskSerializer, NewTaskCreateSerializer, \
    NewTaskUpdateTextSerializer, NewTaskUpdateColumnSerializer, NewTaskListSerializer, \
    NewColumnSerializer, NewColumnCreateSerializer, NewColumnUpdateTextSerializer, \
    NewColumnListSerializer, NewBoardListSerializer, NewBoardCreateSerializer, \
    NewBoardUpdateSerializer

class BaseViewSet(viewsets.ModelViewSet):
    serializer_map: dict = None

    def get_serializer_class(self):
        if not self.serializer_map:
            raise NotImplementedError('serializer_map must be implement')
        return self.serializer_map[self.action]

    permission_map: dict = None

    def get_permissions(self):
        if not self.permission_map:
            raise NotImplementedError('permission_map must be implement')
        return [permission() for permission in self.permission_map[self.action]]


class TaskViewSet(BaseViewSet):
    queryset = Task.objects.all()
    serializer_map = {
        'task_open': TaskShowSerializer,
        'task_list': TaskListSerializer,
        'task_add': TaskSerializer,
        'task_update': TaskSerializer
        # 'task_move': TaskUpdateColumnSerializer
    }
    permission_map = {
        'task_open': (base_permissions.IsAuthenticated,
                      (table_permissions.IsVisitor |
                       table_permissions.IsMember |
                       table_permissions.IsOwner |
                       table_permissions.IsAdmin)
                      ),
        'task_list': (base_permissions.IsAuthenticated,
                      (table_permissions.IsVisitor |
                       table_permissions.IsMember |
                       table_permissions.IsOwner |
                       table_permissions.IsAdmin)
                      ),
        'task_add': (base_permissions.IsAuthenticated,
                     (table_permissions.IsMember |
                      table_permissions.IsOwner |
                      table_permissions.IsAdmin)
                     ),
        'task_update': (base_permissions.IsAuthenticated,
                        (table_permissions.IsMember |
                         table_permissions.IsOwner |
                         table_permissions.IsAdmin)
                        ),
        'task_move': (base_permissions.IsAuthenticated,
                      (table_permissions.IsMember |
                       table_permissions.IsOwner |
                       table_permissions.IsAdmin)
                      )
        # 'task_open': (base_permissions.IsAuthenticated,),
        # 'task_list': (base_permissions.IsAuthenticated,),
        # 'task_add': (base_permissions.IsAuthenticated,),
        # 'task_update': (base_permissions.IsAuthenticated,),
        # 'task_move': (base_permissions.IsAuthenticated,)
    }

    @action(detail=False, methods=['GET'])
    def task_open(self, request):
        objs = self.get_queryset().get(id=request.data.get('task_id'))
        serializer = self.get_serializer(objs, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def task_list(self, request):
        objs = self.get_queryset().filter(column=request.data.get('column_id'))
        serializer = self.get_serializer(objs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['POST'])
    def task_add(self, request):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        column_id = data.get('column_id')
        TaskColumn.objects.create(task=obj, column=Column.objects.get(id=column_id))
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['PUT', 'PATCH'])
    def task_update(self, request, pk):
        data = request.data
        obj = self.get_queryset().get(pk=pk)
        serializer = self.get_serializer(obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['PUT', 'PATCH'])
    def task_move(self, request, pk):
        data = request.data
        obj = TaskColumn.objects.get(task=pk)
        serializer = self.get_serializer(obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ColumnViewSet(BaseViewSet):
    queryset = Column.objects.all()
    serializer_map = {
        'column_list': ColumnListSerializer,
        'column_info': ColumnShowSerializer,
        'column_add': ColumnSerializer,
        'column_update': ColumnSerializer
    }

    permission_map = {
        'column_list': (base_permissions.IsAuthenticated,
                        (table_permissions.IsVisitor |
                         table_permissions.IsMember |
                         table_permissions.IsOwner |
                         table_permissions.IsAdmin)
                        ),
        'column_add': (base_permissions.IsAuthenticated,
                       (table_permissions.IsMember |
                        table_permissions.IsOwner |
                        table_permissions.IsAdmin)
                       ),
        'column_update': (base_permissions.IsAuthenticated,
                          (table_permissions.IsMember |
                           table_permissions.IsOwner |
                           table_permissions.IsAdmin)
                          ),
        'column_info': (base_permissions.IsAuthenticated,
                          (table_permissions.IsVisitor |
                           table_permissions.IsMember |
                           table_permissions.IsOwner |
                           table_permissions.IsAdmin)
                          ),
        'column_delete': (base_permissions.IsAuthenticated,
                          table_permissions.IsOwner
                          ),
        # 'column_list': (base_permissions.IsAuthenticated,),
        # 'column_add': (base_permissions.IsAuthenticated,),
        # 'column_update': (base_permissions.IsAuthenticated,)
    }

    @action(detail=True, methods=['GET'])
    def column_list(self, request, pk):
        objs = ColumnBoard.objects.filter(board_id=pk)
        serializer = self.get_serializer(objs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def column_info(self, request, pk):
        column = self.get_queryset().get(id=pk)
        serializer = self.get_serializer(data=column, many=False)
        print(serializer.is_valid())
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def column_add(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        board = Board.objects.get(id=request.data.get('board_id'))
        ColumnBoard.objects.create(column=obj, board=board)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['PUT', 'PATCH'])
    def column_update(self, request, pk):
        obj = self.get_queryset().get(id=pk)
        if obj.count() == 0:
            data = {'error': "404 Column not found"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = self.get_serializer(obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['DELETE'])
    def column_delete(self, request, pk):
        obj = self.get_queryset().filter(pk=pk)
        print(obj)
        if obj.count() == 0:
            data = {'error': "404 Column not found"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        else:
            obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BoardViewSet(BaseViewSet):
    queryset = Board.objects.all()
    serializer_map = {
        'board_list': BoardListSerializer,
        'board_add': BoardSerializer,
        'board_update': BoardSerializer
    }

    permission_map = {
        'board_list': (base_permissions.IsAuthenticated,
                       (table_permissions.IsVisitor |
                        table_permissions.IsMember |
                        table_permissions.IsOwner |
                        table_permissions.IsAdmin)
                       ),
        'board_update': (base_permissions.IsAuthenticated,
                         (table_permissions.IsOwner |
                          table_permissions.IsAdmin)
                         ),
        'board_add': (base_permissions.IsAuthenticated,),
        # 'board_delete': (base_permissions.IsAuthenticated,
        #                  (table_permissions.IsOwner |
        #                   table_permissions.IsAdmin)
        #                  ),
        # 'all': (base_permissions.IsAuthenticated, table_permissions.IsAdmin)
        # 'board_list': (base_permissions.IsAuthenticated,),
        # 'board_add': (base_permissions.IsAuthenticated,),
        # 'board_update': (base_permissions.IsAuthenticated,),
        'board_delete': (base_permissions.IsAuthenticated,)
    }

    # def get_queryset(self):
    #     return self.queryset.filter(users__id=self.request.user.id)

    # в ответе список досок для юзера отправившего request
    @action(detail=False, methods=['GET'])
    def board_list(self, request):
        boards_per_user = PermissionOnBoard.objects.filter(user=request.user)
        serializer = self.get_serializer(boards_per_user, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def board_add(self, request):
        data = request.data
        board_serializer = self.get_serializer(data=data)
        board_serializer.is_valid(raise_exception=True)
        with transaction.atomic():  # если ошибка на создание убрать эту строку
            board_serializer.save()

        permission_data = {}
        permission_data['board'] = board_serializer.data.get('id')
        permission_data['user'] = request.user.id
        permission_data['permission'] = "1"
        permission_serializer = PermissionSerializer(data=permission_data)
        permission_serializer.is_valid(raise_exception=True)
        permission_serializer.save()

        return Response(data=board_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['PUT', 'PATCH'])
    def board_update(self, request, pk):
        data = request.data
        obj = self.get_queryset().get(pk=pk)
        serializer = self.get_serializer(obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    # http://127.0.0.1:8000/api_v1/boards/37/board_delete/
    # @action(detail=True, methods=['DELETE'])
    # def board_delete(self, request, pk):
    #     column_id_list = ColumnBoard.objects.filter(board_id=pk)
    #     # Task.objects.filter(id=tasks_id_list)
    #     for column in column_id_list:
    #         print(column)
    #         print(Column.objects.get(id=column.id))
    #         Column.objects.get(id=column.id).delete()
    #     # print(column_id_list.count())
    #     column = self.get_queryset().filter(pk=pk)
    #     if column.count() == 0:
    #         responce = {}
    #         responce['error'] = "404 Board not found"
    #         return Response(data=responce, status=status.HTTP_400_BAD_REQUEST)
    #
    #     else:
    #         column.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class PermissionViewSet(BaseViewSet):
    queryset = PermissionOnBoard.objects.all()
    serializer_map = {
        'permission_update': PermissionSerializer,
        'permission_create': PermissionSerializer,
    }

    permission_map = {
        'permission_update': (base_permissions.IsAuthenticated |
                              table_permissions.IsOwner
                              ),
        'permission_create': (base_permissions.IsAuthenticated,)
    }

    @action(detail=False, methods=['PUT', 'PATCH'])
    def permission_update(self, request):
        data = request.data
        board_id = data.get('board')
        user_id = data.get('user')
        obj = self.get_queryset().get(
            board=board_id,
            user=user_id
        )
        serializer = self.get_serializer(obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def permission_create(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


def CheckPermissionOnTask(request, pk):
    column_id = Task.objects.get(id=pk).column
    board_id = Column.objects.get(id=column_id).board
    return PermissionOnBoard.objects.get(
        user=request.user.id,
        board=board_id
    ).first()


class NewTaskViewSet(BaseViewSet):
    queryset = Task.objects.all()
    serializer_map = {
        'task_open': NewTaskSerializer,
        'task_list': NewTaskListSerializer,
        'task_add': NewTaskCreateSerializer
    }
    permission_map = {
        # 'task_open': (base_permissions.IsAuthenticated,
        #               (table_permissions.IsVisitor |
        #                table_permissions.IsMember |
        #                table_permissions.IsOwner |
        #                table_permissions.IsAdmin)
        #               ),
        # 'task_list': (base_permissions.IsAuthenticated,
        #               (table_permissions.IsVisitor |
        #                table_permissions.IsMember |
        #                table_permissions.IsOwner |
        #                table_permissions.IsAdmin)
        #               ),
        # 'task_add': (base_permissions.IsAuthenticated,
        #              (table_permissions.IsMember |
        #               table_permissions.IsOwner |
        #               table_permissions.IsAdmin)
        #              ),
        # 'task_update': (base_permissions.IsAuthenticated,
        #                 (table_permissions.IsMember |
        #                  table_permissions.IsOwner |
        #                  table_permissions.IsAdmin)
        #                 ),
        # 'task_move': (base_permissions.IsAuthenticated,
        #               (table_permissions.IsMember |
        #                table_permissions.IsOwner |
        #                table_permissions.IsAdmin)
        #               )
        'task_open': (base_permissions.IsAuthenticated,),
        'task_list': (base_permissions.IsAuthenticated,),
        'task_add': (base_permissions.IsAuthenticated,),
        'task_update': (base_permissions.IsAuthenticated,),
        'task_move': (base_permissions.IsAuthenticated,)
    }

    @action(detail=False, methods=['GET'])
    def task_open(self, request):
        task_id = request.data.get('task_id')
        obj_permission = CheckPermissionOnTask(request=request, pk=task_id)
        obj = self.get_queryset().get(id=task_id)
        serializer = self.get_serializer(obj, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def task_list(self, request, pk):
        # column_id = pk
        obj_permission = CheckPermissionOnColumn(request=request, pk=pk)
        objs = self.get_queryset().filter(column=pk)
        serializer = self.get_serializer(objs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # task add
    # {
    #     "text": "uiop",
    #     "column": 7
    # }
    @action(detail=False, methods=['POST'])
    def task_add(self, request):
        data = request.data
        obj_permission = CheckPermissionOnColumn(request=request, pk=data.get('column_id'))
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['PUT', 'PATCH'])
    def task_update(self, request, pk):
        obj_permission = CheckPermissionOnTask(request=request, pk=pk)
        data = request.data
        obj = self.get_queryset().get(pk=pk)
        if request.data.get('text'):
            serializer = NewTaskUpdateTextSerializer(obj, data=data)
        else:
            serializer = NewTaskUpdateColumnSerializer(obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


def CheckPermissionOnColumn(request, pk):
    board_id = Column.objects.get(id=pk).board_id
    return PermissionOnBoard.objects.get(
        user=request.user.id,
        board=board_id
    )

def CheckPermissionOnBoard(request, pk):
    board_id = pk
    return PermissionOnBoard.objects.get(
        user=request.user.id,
        board=board_id
    )


class NewColumnViewSet(BaseViewSet):
    queryset = Column.objects.all()
    serializer_map = {
        'column_list': NewColumnListSerializer,
        'column_add': NewColumnCreateSerializer,
        'column_update': NewColumnUpdateTextSerializer
    }

    permission_map = {
        # 'column_list': (base_permissions.IsAuthenticated,
        #                 (table_permissions.IsVisitor |
        #                  table_permissions.IsMember |
        #                  table_permissions.IsOwner |
        #                  table_permissions.IsAdmin)
        #                 ),
        # 'column_add': (base_permissions.IsAuthenticated,
        #                (table_permissions.IsMember |
        #                 table_permissions.IsOwner |
        #                 table_permissions.IsAdmin)
        #                ),
        # 'column_update': (base_permissions.IsAuthenticated,
        #                   (table_permissions.IsMember |
        #                    table_permissions.IsOwner |
        #                    table_permissions.IsAdmin)
        #                   ),
        'column_delete': (base_permissions.IsAuthenticated,
                          table_permissions.IsOwner
                          ),
        'column_list': (base_permissions.IsAuthenticated,),
        'column_add': (base_permissions.IsAuthenticated,),
        'column_update': (base_permissions.IsAuthenticated,)
    }

    lookup_field = 'pk'
    # вернет идишники колонок по pk борды
    @action(detail=True, methods=['GET'])
    def column_list(self, request, pk):
        obj_permission = CheckPermissionOnBoard(request=request, pk=pk)
        objs = Column.objects.filter(board_id=pk)
        serializer = self.get_serializer(objs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def column_add(self, request, pk):
        obj_permission = CheckPermissionOnBoard(request=request, pk=pk)
        # board = Board.objects.get(id=pk)
        data = request.data
        data['board_id'] = pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['PUT', 'PATCH'])
    def column_update(self, request, pk):
        obj_permission = CheckPermissionOnColumn(request=request, pk=pk)
        data = request.data
        obj = self.get_queryset().get(pk=pk)
        serializer = self.get_serializer(obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        self.get_object()


    # http://127.0.0.1:8000/api_v1/columns/37/column_delete/
    @action(detail=True, methods=['DELETE'])
    def column_delete(self, request, pk):
        obj_permission = CheckPermissionOnColumn(request=request, pk=pk)
        obj = self.get_queryset().filter(pk=pk)
        if obj.count() == 0:
            responce = {}
            responce['error'] = "404 Column not found"
            return Response(data=responce, status=status.HTTP_400_BAD_REQUEST)

        else:
            obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewBoardViewSet(BaseViewSet):
    queryset = Board.objects.all()
    serializer_map = {
        'board_list': NewBoardListSerializer,
        'board_add': NewBoardCreateSerializer,
        'board_update': NewBoardUpdateSerializer
    }

    permission_map = {
        'board_list': (base_permissions.IsAuthenticated,
                       (table_permissions.IsVisitor |
                        table_permissions.IsMember |
                        table_permissions.IsOwner |
                        table_permissions.IsAdmin)
                       ),
        'board_update': (base_permissions.IsAuthenticated,
                         (table_permissions.IsOwner |
                          table_permissions.IsAdmin)
                         ),
        'board_add': (base_permissions.IsAuthenticated,),
        # 'board_delete': (base_permissions.IsAuthenticated,
        #                  (table_permissions.IsOwner |
        #                   table_permissions.IsAdmin)
        #                  ),
        # 'all': (base_permissions.IsAuthenticated, table_permissions.IsAdmin)
        # 'board_list': (base_permissions.IsAuthenticated,),
        # 'board_add': (base_permissions.IsAuthenticated,),
        # 'board_update': (base_permissions.IsAuthenticated,),
        'board_delete': (base_permissions.IsAuthenticated,)
    }

    # def get_queryset(self):
    #     return self.queryset.filter(users__id=self.request.user.id)

    # в ответе список досок для юзера отправившего request
    @action(detail=False, methods=['GET'])
    def board_list(self, request):
        boards_per_user = PermissionOnBoard.objects.filter(user=request.user)
        serializer = self.get_serializer(boards_per_user, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['POST'])
    # def board_add(self, request):
    #     data = request.data
    #     board_serializer = self.get_serializer(data=data)
    #     board_serializer.is_valid(raise_exception=True)
    #     with transaction.atomic():  # если ошибка на создание убрать эту строку
    #         board_serializer.save()
    #
    #     permission_data = {}
    #     permission_data['board'] = board_serializer.data.get('id')
    #     permission_data['user'] = request.user.id
    #     permission_data['permission'] = "1"
    #     permission_serializer = PermissionCreateSerializer(data=permission_data)
    #     permission_serializer.is_valid(raise_exception=True)
    #     permission_serializer.save()
    #
    #     return Response(data=board_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['PUT', 'PATCH'])
    def board_update(self, request, pk):
        data = request.data
        obj = self.get_queryset().get(pk=pk)
        serializer = self.get_serializer(obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    # http://127.0.0.1:8000/api_v1/boards/37/board_delete/
    # @action(detail=True, methods=['DELETE'])
    # def board_delete(self, request, pk):
    #     column_id_list = ColumnBoard.objects.filter(board_id=pk)
    #     # Task.objects.filter(id=tasks_id_list)
    #     for column in column_id_list:
    #         print(column)
    #         print(Column.objects.get(id=column.id))
    #         Column.objects.get(id=column.id).delete()
    #     # print(column_id_list.count())
    #     column = self.get_queryset().filter(pk=pk)
    #     if column.count() == 0:
    #         responce = {}
    #         responce['error'] = "404 Board not found"
    #         return Response(data=responce, status=status.HTTP_400_BAD_REQUEST)
    #
    #     else:
    #         column.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# registration method POST
# {
#     "username": "user3",
#     "email": "user3@mail.com",
#     "password1": "1234qwertyU",
#     "password2": "1234qwertyU"
# }
