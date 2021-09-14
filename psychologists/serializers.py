from rest_framework import serializers
from .models import Psychologist, PsychologistReview


class PsychologistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Psychologist
        fields = ('id', 'name', 'last_name', 'price_per_hour_online', 'price_per_hour_offline')


class PsychologistDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Psychologist
        fields = ('id', 'name', 'last_name', 'description', 'specialization', 'price_per_hour_online', 'price_per_hour_offline', 'profile_pic', 'reviews')


class CreatePsychologistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Psychologist
        fields = '__all__'

    def validate_price_per_hour_online(self, price_per_hour_online):
        if price_per_hour_online < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной')
        return price_per_hour_online

    def validate_price_per_hour_offline(self, price_per_hour_offline):
        if price_per_hour_offline < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной')
        return price_per_hour_offline

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PsychologistReview
        fields = ('id', 'psychologist_id', 'author', 'text', 'rating', 'created_at')

    def validate_psychologist(self, psychologist):
        request = self.context.get('request')
        user = request.user
        if self.Meta.model.objects.filter(psychologist=psychologist, author=user).exists():
            raise serializers.ValidationError('Вы уже оставляли отзыв вчера')
        return psychologist

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError('Рейтинг может быть от одного до 5')
        return rating

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)