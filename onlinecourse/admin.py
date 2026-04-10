from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission, ExamViolation, UserLessonProgress


# Inline classes
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


# Model Admins
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'category', 'difficulty', 'total_enrollment', 'exam_time_limit', 'passing_score', 'pub_date')
    list_filter = ['pub_date', 'category', 'difficulty']
    search_fields = ['name', 'description']


class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'course', 'grade']
    list_filter = ['course']


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'get_course', 'score', 'passed', 'attempt_number', 'time_taken_display', 'timestamp')
    list_filter = ('passed', 'enrollment__course', 'timestamp')
    search_fields = ['enrollment__user__username', 'enrollment__course__name']

    def get_user(self, obj):
        return obj.enrollment.user.username
    get_user.short_description = 'User'

    def get_course(self, obj):
        return obj.enrollment.course.name
    get_course.short_description = 'Course'

    def time_taken_display(self, obj):
        mins = obj.time_taken_seconds // 60
        secs = obj.time_taken_seconds % 60
        return f"{mins}m {secs}s"
    time_taken_display.short_description = 'Time Taken'


class ExamViolationAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'timestamp', 'description')
    list_filter = ('course', 'timestamp', 'user')
    search_fields = ['user__username', 'course__name']


# Register all
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(ExamViolation, ExamViolationAdmin)
admin.site.register(UserLessonProgress)

# Customize admin header
admin.site.site_header = "Nexly Administration"
admin.site.site_title = "Nexly Admin"
admin.site.index_title = "Manage Your Learning Platform"
