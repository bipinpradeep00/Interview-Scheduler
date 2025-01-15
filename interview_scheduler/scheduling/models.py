from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from  datetime import datetime
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    """
    Class for customizing the User Model objects manager class
    """

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('role', 3)

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password=None, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')
        user = self.model(email=email, **other_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
    Class for customizing the User Model objects
    """
    role_choices = ((1, 'candidate'), (2, 'Interviewer'), (3, 'Admin'))
    gender_choices = ((1, 'Male'), (2, 'Female'), (0, 'Others'))
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.SmallIntegerField(choices=gender_choices, blank=True, null=True)
    role = models.SmallIntegerField(role_choices, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=120, blank=True, null=True)
    state = models.CharField(max_length=120, blank=True, null=True)
    phone_no = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        db_table = 'auth_user'
        ordering = ['id']


class Availability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
            constraints = [
                models.CheckConstraint(
                    check=models.Q(start_time__lt=models.F('end_time')),
                    name='start_time_before_end_time'
                )
            ]

    def __str__(self):
        return f"{self.user.email} - {self.date} ({self.start_time} to {self.end_time})"

    def get_time_slots(self):
        """
        Generate a list of 1-hour slots between start_time and end_time
        """
        slots = []
        current_time = datetime.combine(self.date, self.start_time)
        end_time = datetime.combine(self.date, self.end_time)

        while current_time + timedelta(hours=1) <= end_time:
            next_time = current_time + timedelta(hours=1)
            slots.append((current_time.time(), next_time.time()))
            current_time = next_time

        return slots