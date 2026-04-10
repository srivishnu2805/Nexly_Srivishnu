from celery import shared_task
import time

@shared_task
def generate_and_email_certificate(submission_id):
    """
    Simulates a heavy async task to generate a high-res PDF
    and email it to the student.
    """
    # Simulating heavy processing (e.g. PDF generation, SMTP server connection)
    time.sleep(3)
    return f"Certificate generated and emailed for submission {submission_id}."
