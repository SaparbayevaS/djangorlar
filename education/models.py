from django.db.models import Model, CharField, TextField, BooleanField, ForeignKey, CASCADE, DateTimeField, DecimalField, PositiveSmallIntegerField
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Course(Model):
    title = CharField(max_length=255)
    description = TextField(blank=True, null=True)
    is_active = BooleanField(default=True)
    owner = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="owned_cources")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    deleted_at = DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()
    
    def __str__(self):
        return self.title
    
class Lesson(Model):
    course = ForeignKey(Course, on_delete=CASCADE, related_name="lessons")
    title = CharField(max_length=255)
    content = TextField()
    order = DecimalField(max_digits=10, decimal_places=2)
    indentation = PositiveSmallIntegerField(default=0)
    is_published = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    deleted_at = DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()
    
    def __str__(self):
        return self.title


