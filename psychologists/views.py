from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters

from .models import Psychologist, PsychologistReview
from psychologists.permissions import IsAuthorOrIsAdmin, IsPsychologistOrIsAdmin
from .serializers import (PsychologistSerializer, PsychologistDetailsSerializer,
                          CreatePsychologistSerializer, ReviewSerializer)



@api_view(['GET'])
def psychologists_list(request):
    psychologists = Psychologist.objects.all()
    serializer = PsychologistSerializer(psychologists, many=True)
    return Response(serializer.data)


class PsychologistFilter(filters.FilterSet):
    online_price_from = filters.NumberFilter('price_per_hour_online', 'gte')
    online_price_to = filters.NumberFilter('price_per_hour_online', 'lte')
    offline_price_from = filters.NumberFilter('price_per_hour_offline', 'gte')
    offline_price_to = filters.NumberFilter('price_per_hour_offline', 'lte')

    class Meta:
        model = Psychologist
        fields = ('online_price_from', 'online_price_to', 'offline_price_from', 'offline_price_to')


class PsychologistViewSet(viewsets.ModelViewSet):
    queryset = Psychologist.objects.all()
    filter_backends = [filters.DjangoFilterBackend,
                       rest_filters.SearchFilter,
                       rest_filters.OrderingFilter]
    filterset_class = PsychologistFilter
    search_fields = ['name', 'last_name', 'description']
    ordering_fields = ['name', 'last_name', 'price_per_hour_online', 'price_per_hour_offline' ]

    def get_serializer_class(self):
        if self.action == 'list':
            return PsychologistSerializer
        elif self.action == 'retrieve':
            return PsychologistDetailsSerializer
        return CreatePsychologistSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsPsychologistOrIsAdmin()]
        return []


    @action(['GET'], detail=True)
    def reviews(self, request, pl=None):
        psychologist = self.get_object()
        reviews = psychologist.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=200)


# Создает только залогиненный пользователь
# Редактировать или удалять может либо админ, либо автор

class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = PsychologistReview.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['create', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrIsAdmin()]
        return []

    # def hotel_like(self):
