from rest_framework import serializers
from .models import Course, Submission, Learner
from django.contrib.auth.models import User

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'category', 'difficulty']

class SubmissionSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='enrollment.course.name', read_only=True)
    
    class Meta:
        model = Submission
        fields = ['verification_uuid', 'score', 'passed', 'timestamp', 'course_name']

class LearnerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Learner
        fields = ['username', 'full_name', 'streak_count', 'occupation']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()
