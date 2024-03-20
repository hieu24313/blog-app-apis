from rest_framework import serializers

from ultis.avatar_generation import get_default_avatar
from ultis.helper import validate_image_format
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    # gender = serializers.CharField(source='get_gender_display')

    class Meta:
        model = CustomUser
        fields = ['id',
                  'full_name',
                  'username',
                  'phone_number',
                  'email',
                  'gender',
                  'is_active',
                  'avatar'

                  ]

    def validate(self, data):
        if 'avatar' in data:
            validate_image_format(data['avatar'])
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        avatar_url = get_default_avatar(data['avatar'], data['full_name'], data['phone_number'])
        data['avatar'] = self.context['request'].build_absolute_uri(avatar_url)

        return data
