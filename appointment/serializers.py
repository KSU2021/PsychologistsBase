from rest_framework import serializers

from .models import Appointment, AppointmentItem

class AppointmentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentItem
        exclude = ('id', 'appointment')


class AppointmentSerializer(serializers.ModelSerializer):
    items = AppointmentItemSerializer(many=True)
    created_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)


    class Meta:
        model = Appointment
        exclude = ('user', 'psychologist')


    def create(self, validated_data):
        request = self.context.get('request')
        items = validated_data.pop('items')
        user = request.user
        appointment = Appointment.objects.create(user=user)
        total = 0
        for item in items:
            total = total + item['psychologist'].price_per_hour_online * item['hours_online'] + item['psychologist'].price_per_hour_offline * item['hours_offline']
            AppointmentItem.objects.create(appointment=appointment,
                                     psychologist=item['psychologist'],
                                     hours_online=item['hours_online'],
                                     hours_offline=item['hours_offline'],
                                           )
        appointment.total_sum = total
        appointment.save()
        return appointment







