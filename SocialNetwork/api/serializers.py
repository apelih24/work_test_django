import requests
import json

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from django.contrib.auth import get_user_model

from SocialNetwork.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'pk',
            'user',
            'post_text',
            'pub_date',
            'likes'
        ]
        read_only_fields = ['user', 'likes', 'pub_date']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    email = serializers.CharField(help_text='Email')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')

    def validate(self, data):
        email = data.get('email')
        print(data)
        reserved_email = get_user_model().objects.filter(email=email)
        if reserved_email:
            raise serializers.ValidationError('This email is already taken')

        # Checking email with hunter.io API
        key = '2ade274bdcae4dd44ac57da562f42c35d72ec38b'
        s = 'https://api.hunter.io/v2/email-verifier?email=' + email + '&api_key=' + key
        r = requests.get(s)
        j = json.loads(r.text)
        print(j)
        if j['data']['score'] < 50:
            raise serializers.ValidationError('Email doesnt pass hunter.io check.')
        return data

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLogInSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'token')

    def validate(self, data):
        username = data.get('username', None)
        password = data['password']
        if not username:
            raise serializers.ValidationError('Username is required.')

        user = get_user_model().objects.filter(username=username).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError('This username is not valid.')

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError('Incorrect password please try again.')

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user_obj)
        data['token'] = jwt_encode_handler(payload)

        return data


class PostLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'pk',
            'user',
            'post_text',
            'pub_date',
            'likes'
        ]
        read_only_fields = ['user', 'pub_date']
