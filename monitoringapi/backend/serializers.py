from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Device, ChatMessage


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'device_name', 'cpu', 'gpu', 'ram', 'os']


class UserSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'devices']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'user_message', 'gpt_response', 'timestamp']
        extra_kwargs = {
            'gpt_response': {'required': False}  # Make gpt_response optional
        }