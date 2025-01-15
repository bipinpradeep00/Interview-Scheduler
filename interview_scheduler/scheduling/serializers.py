
from rest_framework import serializers
from .models import User, Availability
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for simplified User Registration
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'role']

class AvailabilitySerializer(serializers.ModelSerializer):
    """
    Serializer for Availability, excluding the user field
    """
    class Meta:
        model = Availability
        fields = ['date', 'start_time', 'end_time']  # Exclude 'user'ds = ['id', 'user', 'date', 'start_time', 'end_time']

    def validate(self, data):
        """
        Custom validation to ensure start_time is before end_time
        """
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")
        return data

class ScheduleSerializer(serializers.Serializer):
    """
    Serializer to fetch available time slots
    """
    candidate_id = serializers.IntegerField()
    interviewer_id = serializers.IntegerField()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data.update({
            "role": user.role,
        })
        return data