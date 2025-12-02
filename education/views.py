from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer, LessonCreateSerializer
from django.shortcuts import get_list_or_404
from django.utils import timezone
from rest_framework.decorators import action



class CourseViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        is_active = request.query_params.get('is_active')
        courses = Course.objects.filter(deleted_at=None)
        if is_active is not None:
            courses = courses.filter(is_active=is_active.lower() == 'true')
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = CourseSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        course = get_list_or_404(Course, pk=pk, deleted_at=None)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        course = get_list_or_404(Course, pk=pk, deleted_at=None, oqner=request.user)
        serializer = CourseSerializer(course, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        course = get_list_or_404(Course, pk=pk, deleted_at=None, owner=request.user)
        course.deleted_at = timezone.now()
        course.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        course = get_list_or_404(Course, pk=pk, deleted_at=None, owner=request.user)
        if course.is_active:
            return Response({"detail": "Course already active"}, status=status.HTTP_400_BAD_REQUEST)
        course.is_active = True
        course.save()
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        course = get_list_or_404(Course, pk=pk, deleted_at=None, owner=request.user)
        if not course.is_active:
            return Response({"detail": "Course already inactive"}, status=status.HTTP_400_BAD_REQUEST)
        course.is_active = False
        course.save()
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        course = get_list_or_404(Course, pk=pk, deleted_at=None)
        lessons = Lesson.objects.filter(course=course, deleted_at=None)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
        
    

class LessonViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request, course_pk=None):
        lessons = Lesson.objects.filter(course_id=course_pk, deleted_at=None)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = LessonCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        lesson = serializer.save()
        return Response(LessonSerializer(lesson).data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        lesson = get_list_or_404(Lesson, pk=pk, deleted_at=None)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        lesson = get_list_or_404(Lesson, pk=pk, deleted_at=None, course__owner=request.user)
        serializer = LessonSerializer(lesson, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        lesson = get_list_or_404(Lesson, pk=pk, deleted_at=None, course__owner=request.user)
        lesson.deleted_at = timezone.now()
        lesson.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        lesson = get_list_or_404(Lesson, pk=pk, deleted_at=None, course__owner=request.user)
        lesson.is_published = True
        lesson.save()
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        lesson = get_list_or_404(Lesson, pk=pk, deleted_at=None, course__owner=request.user)
        lesson.is_published = False
        lesson.save()
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'])
    def move(self, request, pk=None):
        lesson = get_list_or_404(Lesson, pk=pk, deleted_at=None, course__owner=request.user)
        before_id = request.data.get('before_lesson_id')
        course_lessons = Lesson.objects.filter(coutse=lesson.course, deleted_at=None).order_by('order')
        if before_id:
            try:
                before_lesson = course_lessons.get(pk=before_id)
                new_order = before_lesson.order - 0.1
            except Lesson.DoesNotExist:
                return Response({"detail": "before_lesson_id not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            new_order = course_lessons.last().order + 1 if course_lessons.exists() else 0.0

        lesson.order = new_order
        lesson.save()
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

