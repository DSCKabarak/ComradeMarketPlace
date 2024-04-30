from celery import shared_task
from django.core.mail import EmailMessage, get_connection
from marketplace.models import Notification
from django.template.loader import get_template
from marketplace.models import CustomUser


@shared_task
def send_single_email_notification(
    subject: str,
    recipient: str,
    content,
    notification_type: str,
    template: str = None,
    sender: str = None,
):
    try:
        if template:
            message = get_template(template_name=template).render(context=content)
        else:
            message = get_template("simple_template.html").render(
                context={"content": content}
            )

        user = CustomUser.objects.get(email=recipient)

        notification = Notification.objects.create(
            notification_type=notification_type,
            recipient=user,
            subject=subject,
            content=message,
        )

        mail = EmailMessage(
            subject=subject,
            body=message,
            from_email=sender,
            to=[user.email],
        )
        mail.content_subtype = "html"
        if mail.send() > 0:
            notification.is_sent = True
            notification.save()
            return True
        else:
            print(
                f"Email notification {notification} with ID {notification.id} failed to send"
            )
            return False

    except Exception as e:
        print(
            f"Error when sending single person content notification: {e.__cause__} {e.args}"
        )
        return False


@shared_task
def send_mass_email_notification(
    data: list, notification_type: str, template: str = None, sender: str = None
):
    try:
        with get_connection() as email_connection:
            for datatuple in data:
                subject, recipient, content = datatuple

                user = CustomUser.objects.get(email=recipient)

                if template:
                    message = get_template(template_name=template).render(
                        context=content
                    )
                else:
                    message = get_template("simple_template.html").render(
                        context={"content": content}
                    )

                notification = Notification.objects.create(
                    notification_type=notification_type,
                    recipient=user,
                    subject=subject,
                    content=message,
                )

                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=sender,
                    to=[user.email],
                    connection=email_connection,
                )
                email.content_subtype = "html"

                if email.send() > 0:
                    notification.is_sent = True
                    notification.save()
                else:
                    print(
                        f"Email notification {notification} with ID {notification.id} failed to send"
                    )

        return True

    except Exception as e:
        print(f"Error when sending mass email notifications: {e}")
        return False
