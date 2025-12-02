from django.db.models import EmailField, CharField, BooleanField, DateField, DecimalField, DateTimeField
from django.contrib.auth.models import  AbstractBaseUser,  BaseUserManager, PermissionsMixin
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is not required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser should have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser should have is_superuser=True')
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    email = EmailField(unique=True)
    username = CharField(max_length=150, unique=True)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    phone = CharField(max_length=20, blank=True, null=True)
    city = CharField(max_length=50, blank=True, null=True)
    country = CharField(max_length=50, blank=True, null=True)
    department = CharField(max_length=50, blank=True, null=True)
    role = CharField(max_length=50, choices=ROLE_CHOICES, default='employee')
    birth_date = DateField(blank=True, null=True)
    salary = DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    date_joined = DateTimeField(default=timezone.now)
    last_login = DateTimeField(blank=True, null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['email'] 

    def __str__(self):
        return self.email



