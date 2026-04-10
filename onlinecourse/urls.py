from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Home / Course listing
    path(route='', view=views.CourseListView.as_view(), name='index'),
    path('enrolled/', views.EnrolledCourseListView.as_view(), name='enrolled_courses'),

    # Authentication
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    # Course detail
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    path('<int:course_id>/lesson/<int:lesson_id>/complete/', views.mark_lesson_complete, name='mark_lesson_complete'),
    path('<int:course_id>/study-guide/', views.generate_study_guide, name='generate_study_guide'),

    # Enrollment
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('<int:course_id>/exam/', views.take_exam, name='take_exam'),

    # Exam submit
    path('course/<int:course_id>/rate/', views.rate_course, name='rate_course'),
    path('course/<int:course_id>/submit/', views.submit, name='submit'),

    # Exam result
    path('<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),

    # Exam violation logging
    path('<int:course_id>/log_violation/', views.log_violation, name='log_violation'),

    # Student dashboard
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('showcase/<str:username>/', views.public_showcase, name='public_showcase'),

    # Leaderboard
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('<int:course_id>/leaderboard/', views.leaderboard, name='course_leaderboard'),

    # PDF Certificate
    path('<int:course_id>/certificate/<int:submission_id>/', views.generate_certificate, name='generate_certificate'),
    path('verify/certificate/<uuid:verification_uuid>/', views.verify_certificate, name='verify_certificate'),

    # API Layer
    path('api/courses/', views.CourseListAPI.as_view(), name='api_course_list'),
    path('api/showcase/<str:username>/', views.PublicShowcaseAPI.as_view(), name='api_public_showcase'),

    # Admin analytics and recruiter
    path('analytics/', views.admin_analytics, name='admin_analytics'),
    path('recruiters/', views.recruiter_portal, name='recruiter_portal'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
