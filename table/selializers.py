from rest_framework import serializers

from table.models import Task, Column, Board, PermissionOnBoard, User, TaskColumn, ColumnBoard


class TaskShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'text']


class ColumnFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'title_column', 'tasks']
        read_only_fields = list(fields)
        # read_only_fields = ('id', 'title')
    tasks = TaskShowSerializer(many=True)


class BoardFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title_board', 'columns']
        read_only_fields = list(fields)

    title_board = serializers.CharField(min_length=1, max_length=100)
    columns = ColumnFullSerializer(many=True, required=False)


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', ]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'text']
        read_only_fields = ('id',)

    text = serializers.CharField(min_length=1, max_length=255)

    def create(self, validated_data):
        return self.Meta.model.objects.create(text=validated_data['text'])

    def update(self, instance: Task, validated_data):
        instance.text = validated_data['text']
        instance.save()
        return instance


# class TaskUpdateTextSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = ['id', 'text']
#         read_only_fields = ('id',)
#
#     text = serializers.CharField(min_length=1, max_length=255)
#
#     def update(self, instance: Task, validated_data):
#         instance.text = validated_data['text']
#         instance.save()
#         return instance


class TaskUpdateColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskColumn
        fields = ['id', 'column']
        read_only_fields = ('id',)

    column = serializers.CharField(min_length=1)

    def update(self, instance: TaskColumn, validated_data):
        instance.column = validated_data['column']
        instance.save()
        return instance


class ColumnShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'title_column']


class ColumnListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColumnBoard
        fields = ['column', ]


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'title_column', 'tasks']
        read_only_fields = ('id', 'tasks')

    tasks = TaskSerializer(many=True, required=False)
    title_column = serializers.CharField(min_length=1, max_length=100)

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance: Column, validated_data):
        instance.title_column = validated_data['title_column']
        instance.save()
        return instance


# class ColumnUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Column
#         fields = ['id', 'title_column']
#         read_only_fields = ('id',)
#
#     title = serializers.CharField(min_length=1, max_length=100)
#
#     def update(self, instance: Column, validated_data):
#         instance.title = validated_data['title_column']
#         instance.save()
#         return instance


class BoardShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionOnBoard
        fields = ['id', 'title']
        # fields = ['board', ]


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionOnBoard
        fields = ['board_id', ]
        read_only_fields = ('id',)


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title_board']
        read_only_fields = ('id',)

    title_board = serializers.CharField(min_length=1, max_length=100)

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance: Board, validated_data):
        instance.title_board = validated_data['title_board']
        instance.save()
        return instance


# class BoardUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Board
#         fields = ['id', 'title_board']
#         read_only_fields = ('id',)
#
#     title = serializers.CharField(min_length=1, max_length=100)
#
#     def update(self, instance: Board, validated_data):
#         instance.text = validated_data['title_board']
#         instance.save()
#         return instance


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionOnBoard
        fields = ['id', 'user', 'board', 'permission']
        read_only_fields = ('id',)

    board = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(), required=True
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )
    permission = serializers.ChoiceField(choices=Meta.model.permission_types)

    def update(self, instance: PermissionOnBoard, validated_data):
        for i in validated_data.keys():
            setattr(instance, i, validated_data[i])
        instance.save()
        return instance

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)


# class PermissionCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PermissionOnBoard
#         fields = ['id', 'user', 'board', 'permission']
#         read_only_fields = ('id',)
#
#     board = serializers.PrimaryKeyRelatedField(
#         queryset=Board.objects.all(), required=True
#     )
#     user = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(), required=True
#     )
#     permission = serializers.ChoiceField(choices=Meta.model.permission_types)
#
#     def create(self, validated_data):
#         return self.Meta.model.objects.create(**validated_data)


#################################################################################
################### без доп связывающих таблиц ##################################
#################################################################################

class NewTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model: Task
        fields = ['id', 'text']
        read_only_fields = ('id',)

    text = serializers.CharField(min_length=1, max_length=255)


class NewTaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', ]


class NewTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model: Task
        fields = ['id', 'text', 'column']
        read_only_fields = ('id',)

    text = serializers.CharField(min_length=1, max_length=255)
    column = serializers.IntegerField()

    def create(self, validated_data):
        return self.Meta.model.objects.create(text=validated_data['text'])


class NewTaskUpdateTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'text', 'column']
        read_only_fields = ('id',)

    text = serializers.CharField(min_length=1, max_length=255)
    column = serializers.IntegerField()

    def update(self, instance: Task, validated_data):
        instance.text = validated_data['text']
        instance.save()
        return instance


class NewTaskUpdateColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'column']
        read_only_fields = ('id',)

    column = serializers.IntegerField()

    def update(self, instance: Task, validated_data):
        instance.column = validated_data['column']
        instance.save()
        return instance


# column serializers #################

class NewColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'title_column', 'board']
        read_only_fields = ('id', 'board')


class NewColumnListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', ]
        read_only_fields = ('id',)


class NewColumnCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'title_column', 'board_id']
        read_only_fields = ('id',)

    title_column = serializers.CharField(min_length=1, max_length=100)
    board_id = serializers.IntegerField()

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)


class NewColumnUpdateTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'title_column', ]
        read_only_fields = ('id',)

    title_column = serializers.CharField(min_length=1, max_length=100)

    def update(self, instance: Column, validated_data):
        instance.title_column = validated_data['title_column']
        instance.save()
        return instance


# board serializers #####################

class NewBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionOnBoard
        # fields = ['id', 'title', 'columns']
        fields = ['id', 'title_board']
        read_only_fields = ('id',)


class NewBoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionOnBoard
        fields = ['board_id', ]
        read_only_fields = ('id',)


class NewBoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title_board']
        read_only_fields = ('id',)

    title_board = serializers.CharField(min_length=1, max_length=100)

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)


class NewBoardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title_board']
        read_only_fields = ('id',)

    title_board = serializers.CharField(min_length=1, max_length=100)

    def update(self, instance: Board, validated_data):
        instance.title_board = validated_data['title_board']
        instance.save()
        return instance
