from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Course, Lesson, Question, Choice, Enrollment, Submission, Learner, UserLessonProgress, ExamViolation
from datetime import date
import uuid

class NexlyModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.course = Course.objects.create(
            name="Test Course", 
            description="A test description",
            passing_score=80
        )
        self.question = Question.objects.create(course=self.course, question_text="What is 1+1?", grade=100)
        self.choice_correct = Choice.objects.create(question=self.question, choice_text="2", is_correct=True)
        self.choice_incorrect = Choice.objects.create(question=self.question, choice_text="3", is_correct=False)

    def test_question_score_correct(self):
        """Test that Question.is_get_score returns True for correct choices."""
        self.assertTrue(self.question.is_get_score([self.choice_correct.id]))

    def test_question_score_incorrect(self):
        """Test that Question.is_get_score returns False for incorrect choices."""
        self.assertFalse(self.question.is_get_score([self.choice_incorrect.id]))

    def test_question_score_partial(self):
        """Test that Question.is_get_score returns False if not all correct choices selected."""
        # Create another correct choice
        choice_correct2 = Choice.objects.create(question=self.question, choice_text="Two", is_correct=True)
        self.assertFalse(self.question.is_get_score([self.choice_correct.id]))
        self.assertTrue(self.question.is_get_score([self.choice_correct.id, choice_correct2.id]))

    def test_learner_streak_init(self):
        """Test Learner model streak initialization."""
        learner = Learner.objects.create(user=self.user)
        self.assertEqual(learner.streak_count, 0)
        self.assertIsNone(learner.last_activity_date)

class NexlyViewIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student1', password='password123', first_name="Student")
        self.course = Course.objects.create(name="Python 101", description="Learn Python", passing_score=100)
        self.lesson = Lesson.objects.create(title="Intro", content="Hello world", course=self.course, order=1)
        self.question = Question.objects.create(course=self.course, question_text="Is Python fun?", grade=100)
        self.choice = Choice.objects.create(question=self.question, choice_text="Yes", is_correct=True)

    def test_index_view(self):
        response = self.client.get(reverse('onlinecourse:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python 101")

    def test_course_detail_unauthenticated(self):
        response = self.client.get(reverse('onlinecourse:course_details', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login to Enroll")

    def test_enrollment_and_dashboard(self):
        self.client.login(username='student1', password='password123')
        # Enroll
        response = self.client.get(reverse('onlinecourse:enroll', args=[self.course.id]))
        self.assertEqual(response.status_code, 302) # Redirects to detail
        
        # Check Dashboard
        response = self.client.get(reverse('onlinecourse:student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python 101")

    def test_exam_submission_pass(self):
        self.client.login(username='student1', password='password123')
        self.client.get(reverse('onlinecourse:enroll', args=[self.course.id]))
        
        # Submit Exam
        submit_url = reverse('onlinecourse:submit', args=[self.course.id])
        data = {
            f'choice_{self.choice.id}': self.choice.id,
            'time_taken': 30
        }
        response = self.client.post(submit_url, data)
        self.assertEqual(response.status_code, 302) # Redirect to result
        
        # Check Submission record
        submission = Submission.objects.get(enrollment__user=self.user)
        self.assertTrue(submission.passed)
        self.assertEqual(submission.score, 100)

    def test_lesson_completion_and_streak(self):
        self.client.login(username='student1', password='password123')
        url = reverse('onlinecourse:mark_lesson_complete', args=[self.course.id, self.lesson.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        
        # Verify Progress
        self.assertTrue(UserLessonProgress.objects.filter(user=self.user, lesson=self.lesson).exists())
        
        # Verify Streak
        learner = Learner.objects.get(user=self.user)
        self.assertEqual(learner.streak_count, 1)
        self.assertEqual(learner.last_activity_date, date.today())

    def test_public_showcase(self):
        # Create a passed submission first
        enrollment = Enrollment.objects.create(user=self.user, course=self.course)
        submission = Submission.objects.create(enrollment=enrollment, score=100, passed=True)
        
        url = reverse('onlinecourse:public_showcase', args=[self.user.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python 101")
        self.assertContains(response, "Skill DNA Profile")

    def test_certificate_verification(self):
        enrollment = Enrollment.objects.create(user=self.user, course=self.course)
        submission = Submission.objects.create(enrollment=enrollment, score=100, passed=True)
        
        url = reverse('onlinecourse:verify_certificate', args=[submission.verification_uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Certificate Verified")
        self.assertContains(response, str(submission.verification_uuid))

class NexlySystemTests(TestCase):
    """System-level flow testing."""
    def test_complete_user_journey(self):
        c = Client()
        
        # 1. Registration
        reg_url = reverse('onlinecourse:registration')
        c.post(reg_url, {'username': 'newuser', 'psw': 'pass123', 'firstname': 'New', 'lastname': 'User'})
        user = User.objects.get(username='newuser')
        self.assertEqual(user.first_name, 'New')

        # 2. Course Discovery & Enrollment
        course = Course.objects.create(name="Deep Dive", passing_score=50)
        Lesson.objects.create(title="Lesson 1", content="Content", course=course)
        q = Question.objects.create(course=course, question_text="Q?", grade=100)
        Choice.objects.create(question=q, choice_text="Ans", is_correct=True)
        
        c.get(reverse('onlinecourse:enroll', args=[course.id]))
        
        # 3. Learning
        lesson = course.lesson_set.first()
        c.post(reverse('onlinecourse:mark_lesson_complete', args=[course.id, lesson.id]))
        
        # 4. Exam & Certification
        c.post(reverse('onlinecourse:submit', args=[course.id]), {
            f'choice_{q.choice_set.first().id}': q.choice_set.first().id,
            'time_taken': 10
        })
        
        submission = Submission.objects.get(enrollment__user=user)
        self.assertTrue(submission.passed)
        
        # 5. Verification
        verify_url = reverse('onlinecourse:verify_certificate', args=[submission.verification_uuid])
        response = c.get(verify_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New User")
