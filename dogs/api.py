from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets, permissions, serializers
from django.db.models import Avg, Count, Max, Min
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from dogs.models import Breed, Dog, Owner, Country, Hobby
from dogs.serializers import DogCreateSerializer, DogListSerializer, BreedSerializer, OwnerSerializer, CountrySerializer, HobbySerializer, DogUpdateSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Разрешить чтение всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить запись только владельцу объекта
        return obj.user == request.user

class DogsViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Dog.objects.all()
    serializer_class = DogListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user'] 

    def get_serializer_class(self):
        if self.action == 'create':
            return DogCreateSerializer
        if self.action == 'update':
            return DogUpdateSerializer
        return super(DogsViewset, self).get_serializer_class()        

    def get_queryset(self):
        qs = super().get_queryset()  # Используем super() для получения queryset

        # Если пользователь не суперпользователь, фильтруем по текущему пользователю
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        else:
            # Если суперпользователь, добавляем возможность фильтрации по пользователю
            user_id = self.request.query_params.get('user_id', None)  # Получаем user_id из параметров запроса
            if user_id is not None:
                qs = qs.filter(user_id=user_id)

        return qs
        
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=['GET'], url_path='stats')
    def get_stats(self, request, *args, **kwargs):
        stats = Dog.objects.aggregate(
            count=Count('*'),
            avg=Avg('id'),
            max=Max('id'),
            min=Min('id'),
        )

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data) 

class BreedsViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAuthenticated]


class OwnersViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    def get_queryset(self):
        qs = super().get_queryset()  # Используем super() для получения queryset

        # Если пользователь не суперпользователь, фильтруем по текущему пользователю
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        else:
            # Если суперпользователь, добавляем возможность фильтрации по пользователю
            user_id = self.request.query_params.get('user_id', None)  # Получаем user_id из параметров запроса
            if user_id is not None:
                qs = qs.filter(user_id=user_id)

        return qs
        
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=['GET'], url_path='stats')
    def get_stats(self, request, *args, **kwargs):
        stats = Owner.objects.aggregate(
            count=Count('*'),
            avg=Avg('id'),
            max=Max('id'),
            min=Min('id'),
        )

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data) 

class CountryViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]

class HobbyViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Hobby.objects.all()
    serializer_class = HobbySerializer
    permission_classes = [IsAuthenticated]