import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from onlinecourse.models import Course, Lesson, Question, Choice
from django.contrib.auth.models import User

def populate():
    # 1. Create a Superuser for Admin testing
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@edunext.com', 'admin123')
        print("Created Admin User: admin / admin123")

    # 2. Python Course
    course_python, _ = Course.objects.get_or_create(
        name="Introduction to Python",
        defaults={
            'description': "Master the world's most popular programming language from scratch. Learn variables, loops, functions, OOP, and build real projects.",
            'image': 'course_images/python.png',
            'difficulty': 'beginner',
            'category': 'programming',
            'exam_time_limit': 10,
            'passing_score': 50,
        }
    )

    Lesson.objects.get_or_create(title="Variables & Data Types", course=course_python, defaults={'content': "Python supports multiple data types including int, float, string, list, tuple, dict, and set.", 'order': 0})
    Lesson.objects.get_or_create(title="Control Flow", course=course_python, defaults={'content': "If/else statements, for loops, while loops, and comprehensions.", 'order': 1})
    Lesson.objects.get_or_create(title="Functions & Modules", course=course_python, defaults={'content': "Define reusable functions, understand scope, and import modules.", 'order': 2})

    q1, _ = Question.objects.get_or_create(course=course_python, question_text="What is the output of print(2**3)?", defaults={'grade': 50})
    Choice.objects.get_or_create(question=q1, choice_text="6", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q1, choice_text="8", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q1, choice_text="9", defaults={'is_correct': False})

    q1b, _ = Question.objects.get_or_create(course=course_python, question_text="Which keyword is used to define a function in Python?", defaults={'grade': 50})
    Choice.objects.get_or_create(question=q1b, choice_text="function", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q1b, choice_text="def", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q1b, choice_text="func", defaults={'is_correct': False})

    # 3. Web Development Course
    course_web, _ = Course.objects.get_or_create(
        name="Full Stack Web Development",
        defaults={
            'description': "Build modern, responsive websites using HTML, CSS, JavaScript, and Django. Includes REST APIs and deployment.",
            'image': 'course_images/django.png',
            'difficulty': 'intermediate',
            'category': 'web',
            'exam_time_limit': 15,
            'passing_score': 60,
        }
    )

    Lesson.objects.get_or_create(title="HTML Basics", course=course_web, defaults={'content': "HTML is the standard markup language for documents designed to be displayed in a web browser.", 'order': 0})
    Lesson.objects.get_or_create(title="CSS Styling", course=course_web, defaults={'content': "CSS is used for styling the presentation of a document written in a markup language.", 'order': 1})
    Lesson.objects.get_or_create(title="JavaScript Fundamentals", course=course_web, defaults={'content': "JavaScript is a dynamic programming language for web development.", 'order': 2})
    Lesson.objects.get_or_create(title="Django Backend", course=course_web, defaults={'content': "Django is a high-level Python web framework that encourages rapid development.", 'order': 3})

    q2, _ = Question.objects.get_or_create(course=course_web, question_text="What does CSS stand for?", defaults={'grade': 50})
    Choice.objects.get_or_create(question=q2, choice_text="Creative Style Sheets", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q2, choice_text="Cascading Style Sheets", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q2, choice_text="Computer Style Sheets", defaults={'is_correct': False})

    q3, _ = Question.objects.get_or_create(course=course_web, question_text="Which HTML tag is used for the largest heading?", defaults={'grade': 50})
    Choice.objects.get_or_create(question=q3, choice_text="<h6>", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q3, choice_text="<head>", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q3, choice_text="<h1>", defaults={'is_correct': True})

    # 4. Cloud Computing Course
    course_cloud, _ = Course.objects.get_or_create(
        name="Cloud Computing with AWS",
        defaults={
            'description': "Learn to deploy, manage, and scale applications on Amazon Web Services. Covers EC2, S3, Lambda, and more.",
            'image': 'course_images/cloud.png',
            'difficulty': 'intermediate',
            'category': 'cloud',
            'exam_time_limit': 12,
            'passing_score': 50,
        }
    )

    Lesson.objects.get_or_create(title="AWS EC2 Basics", course=course_cloud, defaults={'content': "Learn how to provision and manage EC2 instances for scalable compute.", 'order': 0})
    Lesson.objects.get_or_create(title="S3 Storage", course=course_cloud, defaults={'content': "Amazon S3 provides object storage built for any amount of data.", 'order': 1})

    q4, _ = Question.objects.get_or_create(course=course_cloud, question_text="What does EC2 stand for?", defaults={'grade': 50})
    Choice.objects.get_or_create(question=q4, choice_text="Elastic Compute Cloud", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q4, choice_text="Electronic Computer Code", defaults={'is_correct': False})

    q4b, _ = Question.objects.get_or_create(course=course_cloud, question_text="Which AWS service is used for object storage?", defaults={'grade': 50})
    Choice.objects.get_or_create(question=q4b, choice_text="EC2", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q4b, choice_text="S3", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q4b, choice_text="RDS", defaults={'is_correct': False})

    # 5. Machine Learning Course
    course_ml, _ = Course.objects.get_or_create(
        name="Machine Learning A-Z",
        defaults={
            'description': "Hands-on machine learning with Python and Scikit-Learn. From linear regression to deep learning fundamentals.",
            'image': 'course_images/ml.png',
            'difficulty': 'advanced',
            'category': 'data',
            'exam_time_limit': 20,
            'passing_score': 70,
        }
    )

    Lesson.objects.get_or_create(title="Supervised Learning", course=course_ml, defaults={'content': "Classification and regression algorithms: Linear Regression, Decision Trees, SVM, KNN.", 'order': 0})
    Lesson.objects.get_or_create(title="Unsupervised Learning", course=course_ml, defaults={'content': "Clustering with K-Means, Hierarchical Clustering, and PCA.", 'order': 1})
    Lesson.objects.get_or_create(title="Model Evaluation", course=course_ml, defaults={'content': "Cross-validation, confusion matrices, ROC curves, and hyperparameter tuning.", 'order': 2})

    q5, _ = Question.objects.get_or_create(course=course_ml, question_text="Which algorithm is used for classification?", defaults={'grade': 50})
    Choice.objects.get_or_create(question=q5, choice_text="Linear Regression", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q5, choice_text="Logistic Regression", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q5, choice_text="K-Means", defaults={'is_correct': False})

    q5b, _ = Question.objects.get_or_create(course=course_ml, question_text="What does 'overfitting' mean?", defaults={'grade': 50})
    Choice.objects.get_or_create(question=q5b, choice_text="Model performs well on training data but poorly on new data", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q5b, choice_text="Model performs poorly on all data", defaults={'is_correct': False})

    # 6. UI/UX Design Course
    course_design, _ = Course.objects.get_or_create(
        name="UI/UX Design Masterclass",
        defaults={
            'description': "Design stunning user interfaces and amazing user experiences. Master Figma, wireframing, prototyping, and design systems.",
            'image': 'course_images/design.png',
            'difficulty': 'beginner',
            'category': 'design',
            'exam_time_limit': 8,
            'passing_score': 50,
        }
    )

    Lesson.objects.get_or_create(title="Wireframing", course=course_design, defaults={'content': "Creating low-fidelity wireframes before high-fidelity designs.", 'order': 0})
    Lesson.objects.get_or_create(title="Color Theory", course=course_design, defaults={'content': "Understanding color palettes, contrast, and accessibility in design.", 'order': 1})

    q6, _ = Question.objects.get_or_create(course=course_design, question_text="What is a wireframe?", defaults={'grade': 50})
    Choice.objects.get_or_create(question=q6, choice_text="A low-fidelity visual guide of a page layout", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q6, choice_text="A type of CSS framework", defaults={'is_correct': False})

    q6b, _ = Question.objects.get_or_create(course=course_design, question_text="What does UX stand for?", defaults={'grade': 50})
    Choice.objects.get_or_create(question=q6b, choice_text="User Experience", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q6b, choice_text="Unified Extension", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q6b, choice_text="User Execution", defaults={'is_correct': False})

    print("Database populated successfully with 6 courses, lessons, and exams!")
    print("Admin login: admin / admin123")

if __name__ == '__main__':
    populate()
