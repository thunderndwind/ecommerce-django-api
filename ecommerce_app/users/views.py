from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from .models import UserProfile
from .services.azure_services import AzureFaceIDAuth
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FaceIDLoginView(APIView):
    def post(self, request):
        face_image = request.FILES.get('face_image')
        username = request.data.get('username')

        user = UserProfile.objects.filter(username=username).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        azure_auth = AzureFaceIDAuth()
        if azure_auth.verify_face(face_image, user.face_id):
            token = self.get_jwt_token(user)
            return Response({'token': token}, status=status.HTTP_200_OK)

        return Response({'error': 'Face not recognized'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
