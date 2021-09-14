# Generated by Django 3.2 on 2021-09-14 00:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Psychologist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('psychologist_id', models.IntegerField(unique=True)),
                ('description', models.TextField()),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/ProfilePic/')),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('price_per_hour_online', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_per_hour_offline', models.DecimalField(decimal_places=2, max_digits=10)),
                ('link_to_page', models.URLField(blank=True)),
            ],
            options={
                'ordering': ['psychologist_id', 'price_per_hour_online', 'price_per_hour_offline'],
            },
        ),
        migrations.CreateModel(
            name='PsychologistReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.SmallIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('psychologist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='psychologists.psychologist')),
            ],
        ),
    ]
