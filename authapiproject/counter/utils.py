from django.core.mail import EmailMessage
import  os

class Util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data['email_subject'],
            body=data['body'],
            to=[data['to_email']],
            from_email=data.get('from_email', os.getenv('DEFAULT_FROM_EMAIL'))
        )
        email.send()
