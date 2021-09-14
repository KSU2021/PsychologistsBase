from django.contrib.auth import get_user_model
from django.db import models
from multiselectfield import MultiSelectField
User = get_user_model()

SPECIALIZATION_CHOICES = (
    ('general_psychologist', 'общий психолог'),
    ('family_psychologist', 'семейный психолог'),
    ('children_psychologist', 'детский психолог'),
    ('clinical_psychologist', 'клинический психолог'),
    ('social_psychologist', 'cоциальный психолог'),
    ('corporate_psychologist', 'корпоративный психолог'),
    ('psychoanalyst', 'психоаналитик'),
)


class Psychologist(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    psychologist_id = models.IntegerField(unique=True)
    description = models.TextField()
    specialization = MultiSelectField(
                              choices=SPECIALIZATION_CHOICES,
                              max_length=200,
                              max_choices=4,
                              default='general_psychologist')
    profile_pic = models.ImageField(upload_to='profile_pic/ProfilePic/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True)
    price_per_hour_online = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_hour_offline = models.DecimalField(max_digits=10, decimal_places=2)
    link_to_page = models.URLField(max_length=200, blank=True)

    class Meta:
        ordering = ['psychologist_id', 'price_per_hour_online', 'price_per_hour_offline']

    def __str__(self):
        return "{} {} ".format(self.name, self.last_name)


class PsychologistReview(models.Model):
    psychologist_id = models.ForeignKey(Psychologist,
                                on_delete=models.CASCADE,
                                related_name='reviews')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews')

    text = models.TextField()
    # likes = models.BooleanField(default=False)
    rating = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)