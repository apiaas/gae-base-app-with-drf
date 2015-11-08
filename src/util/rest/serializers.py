from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class AuthViaEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=500, min_length=3)
    password = serializers.CharField(
        max_length=500, min_length=2, style={'input_type': 'password'}
    )
    user_disabled = _('User account is disabled.')
    invalid_creds = _('Unable to login with provided credentials.')
    missing_creds = _('You must provide "email" and "password"')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError(self.user_disabled)
            else:
                raise serializers.ValidationError(self.invalid_creds)
        else:
            raise serializers.ValidationError(self.missing_creds)

        attrs['user'] = user
        return attrs
