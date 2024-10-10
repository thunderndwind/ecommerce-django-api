from rest_framework import serializers
from .models import UserProfile
from django.core.files.images import get_image_dimensions
from .services.azure_services import AzureFaceIDAuth

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'password', 'email', 'phone_number', 'address', 'profile_image']

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address'],
            profile_image=validated_data.get('profile_image')
        )
        
        face_image = validated_data.get('profile_image')
        if face_image:
            azure_face_auth = AzureFaceIDAuth()
            face_id = azure_face_auth.register_face(face_image)  # Call Azure API to register Face ID
            user.face_id = face_id
            user.save()

        return user
