from rest_framework import serializers

from table.models import Task, Column, Board, PermissionOnBoard, User


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

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance: PermissionOnBoard, validated_data):
        for i in validated_data.keys():
            setattr(instance, i, validated_data[i])
        instance.save()
        return instance


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


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # fields = ['id', 'text', 'date', 'fact', 'weather']
        fields = ['id', 'text', 'date']
        read_only_fields = ('id',)

    text = serializers.CharField(min_length=1, max_length=255)
    # fact = serializers.CharField(max_length=511)
    # weather = serializers.FloatField()


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # fields = ['id', 'text', 'column', 'fact', 'weather']
        fields = ['id', 'text', 'column']
        read_only_fields = ('id',)

    text = serializers.CharField(min_length=1, max_length=255)
    column = serializers.PrimaryKeyRelatedField(queryset=Column.objects.all(), required=False)
    # fact = serializers.CharField(max_length=511, required=False)
    # weather = serializers.FloatField(required=False, allow_null=True)

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance: Task, validated_data):
        instance.text = validated_data['text']
        instance.column = validated_data['column']
        instance.save()
        return instance


class ColumnListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'title_column']
        read_only_fields = ('id',)


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'title_column', 'board']
        read_only_fields = ('id',)

    title_column = serializers.CharField(min_length=1, max_length=100)
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all(), required=False)

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance: Column, validated_data):
        instance.title_column = validated_data['title_column']
        instance.save()
        return instance
