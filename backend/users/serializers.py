# serializers.py in the users Django app
# get_adapter in save method to get an instance of our user model
from allauth.account.adapter import get_adapter
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import CustomUser

class CustomRegisterSerializer(RegisterSerializer):
    profilePic = serializers.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = (
            'username', 
            'email', 
            'password', 
            'password2',
            'profilePic')
        
    # override get_cleaned_data of RegisterSerializer
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            "profilePic": self.validated_data.get('profilePic')
            
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.profilePic = self.cleaned_data.get('profilePic')
        user.save()
        adapter.save_user(request, user, self)
        return user