from django.db import models
from psychologists.models import Psychologist
from django.contrib.auth import get_user_model

User = get_user_model()



# PAYMENT_TYPES = [
#     ('I','Индивидуальный'),
#     ('C','Консультация')
# ]
#
# class Payment(models.Model):
#     patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_payments")
#     date = models.DateField(auto_now_add=True)
#     paid = models.IntegerField(null=True)
#     outstanding = models.IntegerField(null=True)
#     total = models.IntegerField(null=True)
#     payment_type = models.CharField(choices=PAYMENT_TYPES, max_length=1, default="I")
#
#     class Meta:
#         ordering = ('-id',)
#
#     def __str__(self):
#         return "Payment Patient-{} Amount-{}".format(self.patient, self.total)


STATUS_CHOICES = (
    ('in process', 'запись в обработке'),
    ('booked', 'консультация назначена'),
    ('canceled', 'консультация отменена'),
    ('finished', 'консультация завершена')
)

class Appointment(models.Model):
    # date = models.DateField()
    # time = models.TimeField()
    total_sum = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT,
                             related_name='appointments')
    status = models.CharField(max_length=20,
                              choices = STATUS_CHOICES,
                              default='booked')
    psychologist = models.ManyToManyField(Psychologist,
                                      through='AppointmentItem')

    @property
    def total(self):
        items = self.items.values('psychologist__price_per_hour_online', 'hours_online', 'psychologist__price_per_hour_offline', 'hours_offline')
        total = 0
        for item in items:
            total = total + (item['psychologist__price_per_hour_online'] * item['hours_online']) + (item['psychologist__price_per_hour_offline'] * item['hours_offline'])
        return total

    def __str__(self):
        return f'Консультация № {self.id} у {self.psychologist} от {self.created_at.strftime("%d-%m-%Y %H:%M")}'

    class Meta:
        db_table = 'appointment'
        ordering = ['-created_at']


class AppointmentItem(models.Model):
    appointment = models.ForeignKey(Appointment,
                              on_delete=models.RESTRICT,
                              related_name='items')
    psychologist = models.ForeignKey(Psychologist,
                                on_delete=models.RESTRICT,
                                related_name='appointment_items')
    # date = models.DateField()
    # time = models.TimeField()
    hours_online = models.PositiveSmallIntegerField(default=1)
    hours_offline = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = 'appointment_items'

