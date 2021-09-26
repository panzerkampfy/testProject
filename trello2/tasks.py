from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from trello2.celery import celery_app


@celery_app.task(default_retry_delay=5, max_retries=10)
def send_verification_email(user_id):
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        send_mail(
            'Verify your trello2 account',
            'Follow this link to verify your account: ',
            'from_dev@trello2.com',
            [user.email],
        )
    except User.DoesNotExist:
        pass


@celery_app.task(default_retry_delay=5, max_retries=10)
def hello():
    print('hello wordl')