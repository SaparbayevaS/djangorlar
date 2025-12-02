from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Course, Lesson
from django.db.models import F

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ['order', 'created_at', 'updated_at', 'deleted_at']

class LessonCreateSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content', 'order', 'indentation', 'is_published']
        read_only_fields = ['order', 'is_published', 'deleted_at']

        def create(self, validated_data):
            course = validated_data['coourse']
            validated_data['order'] = 0.0
            Lesson.objects.filter(course=course, deleted_at=None).update(order=F('order') + 1)
            return super().create(validated_data)

class CourseSerializer(ModelSerializer):
    lessons_count = IntegerField(source='lessons.filter(deleted_at=None).count', read_only=True)
    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ['owner', 'created_at', 'updated_at', 'deleted_at']

        def create(self, validated_data):
            validated_data['owner'] = self.context['request'].user
            return super().create(validated_data)