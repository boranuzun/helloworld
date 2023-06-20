from dj_rest_auth.registration.views import RegisterView
from rest_framework import permissions
from .serializers import CustomRegisterSerializer
from .models import CustomUser

class CustomRegisterView(RegisterView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomRegisterSerializer
    permission_classes = [permissions.AllowAny]