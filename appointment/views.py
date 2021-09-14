from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins, permissions

from .filters import AppointmentFilter
from .models import Appointment

from .serializers import AppointmentSerializer

class AppointmentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Appointment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AppointmentFilter

    def get_queryset(self):
        user = self.request.user
        return Appointment.objects.filter(user=user)




