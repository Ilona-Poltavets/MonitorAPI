import openai
from rest_framework import generics, viewsets
from .models import Device, ChatMessage
from django.contrib.auth.models import User
from .serializers import DeviceSerializer, UserSerializer, ChatMessageSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI

openai.api_key = settings.OPENAI_API_KEY


class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def perform_create(self, serializer):
        # Get the user message from the request data
        user_message = self.request.data.get('user_message')

        if user_message:
            # Generate GPT response using the OpenAI API
            # response = openai.Completion.create(
            #     model="gpt-3.5-turbo",  # Or another available model
            #     prompt=user_message,
            #     max_tokens=150
            # )

            client = OpenAI(
                # This is the default and can be omitted
                api_key=settings.OPENAI_API_KEY,
            )

            # chat_completion = client.chat.completions.create(
            #     messages=[
            #         {
            #             "role": "user",
            #             "content": user_message,
            #         }
            #     ],
            #     model="gpt-3.5-turbo",
            #     # model="text-embedding-3-large"
            # )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" for free access or "gpt-4" for GPT-4 (if available)
                messages=[
                    {"role": "user", "content": "Hello, how are you?"}
                ]
            )
            # Extract the GPT response from the API response
            # gpt_response = chat_completion.choices[0].text.strip()

            gpt_response = response.choices[0].message['content']
            # Create and save the ChatMessage instance with both the user_message and gpt_response
            serializer.save(user_message=user_message, gpt_response=gpt_response)
        else:
            # If no user message is provided, raise an error (optional)
            raise ValueError("User message is required.")


# List all devices
class DeviceListView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = [IsAuthenticated]


# List all users and their devices
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]


class UserByIdView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    lookup_field = 'id'


# Add or modify device for a user
class DeviceCreateView(generics.CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
