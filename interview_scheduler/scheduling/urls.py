from django.urls import path
from .views import RegisterAvailabilityView, ScheduleView, CustomTokenObtainPairView, UserRegisterView

urlpatterns = [
    path('register-availability/', RegisterAvailabilityView.as_view(), name='register-availability'),
    path('schedule/', ScheduleView.as_view(), name='get-schedulable-slots'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register-user/', UserRegisterView.as_view(), name='register_user'),


]
