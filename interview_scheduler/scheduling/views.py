from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import datetime, timedelta
from .models import User, Availability
from .serializers import AvailabilitySerializer, ScheduleSerializer,  UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


class RegisterAvailabilityView(APIView):
    """
    API View to register availability for the logged-in user.
    Enforces time to be on an hourly basis.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AvailabilitySerializer(data=request.data)

        if serializer.is_valid():
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']

            # Validate that start_time and end_time are on the hour
            if start_time.minute != 0 or start_time.second != 0:
                raise ValidationError("Start time must be on the hour (e.g., 10:00, 11:00).")
            if end_time.minute != 0 or end_time.second != 0:
                raise ValidationError("End time must be on the hour (e.g., 10:00, 11:00).")

            # Validate that the time range is valid
            if start_time >= end_time:
                raise ValidationError("Start time must be earlier than end time.")

            # Create the availability for the logged-in user
            Availability.objects.create(
                user=request.user,  # Associate the logged-in user
                date=serializer.validated_data['date'],
                start_time=start_time,
                end_time=end_time
            )

            return Response(
                {"message": "Availability registered successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ScheduleView(APIView):
    """
    API for fetching schedulable interview time slots.
    Only accessible to Admin users (role = 3).
    """
    permission_classes = [IsAuthenticated]  # Use IsAuthenticated only

    def post(self, request):
        # Check if the user is an Admin
        if request.user.role != 3:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            candidate_id = serializer.validated_data['candidate_id']
            interviewer_id = serializer.validated_data['interviewer_id']

            try:
                candidate_availabilities = Availability.objects.filter(user_id=candidate_id)
                interviewer_availabilities = Availability.objects.filter(user_id=interviewer_id)

                # Find overlapping time slots
                slots = []
                for candidate in candidate_availabilities:
                    for interviewer in interviewer_availabilities:
                        if candidate.date == interviewer.date:
                            start = max(candidate.start_time, interviewer.start_time)
                            end = min(candidate.end_time, interviewer.end_time)

                            # Calculate 1-hour slots
                            while start < end:
                                next_slot = (datetime.combine(candidate.date, start) + timedelta(hours=1)).time()
                                if next_slot <= end:
                                    slots.append((start, next_slot))
                                start = next_slot

                return Response({"available_slots": slots}, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT tokens using email and password only.
    """
    serializer_class = CustomTokenObtainPairSerializer
    
class UserRegisterView(APIView):
    """
    API View to register a new user (Candidate or Interviewer)
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            role = serializer.validated_data.get('role')

            # Ensure role is either Candidate (1) or Interviewer (2)
            if role not in [1, 2]:
                return Response(
                    {"error": "Invalid role. Role must be either 1 (Candidate) or 2 (Interviewer)."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create the user
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                role=role
            )

            return Response(
                {"message": "User registered successfully", "user": UserSerializer(user).data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
