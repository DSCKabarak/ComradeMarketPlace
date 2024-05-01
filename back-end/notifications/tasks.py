from celery import shared_task
from django.core.mail import EmailMessage, get_connection
from notifications.models import Notification
from django.template.loader import get_template
from marketplace.models import CustomUser


@shared_task
def send_single_email_notification(
    subject: str,
    recipient: str,
    content,
    description: str,
    notification_type: str,
    template: str = None,
    sender: str = None,
):
    from marketplace.models import CustomUser
    
    try:
        if template:
            message = get_template(template_name=template).render(context=content)
        else:
            message = get_template("simple_template.html").render(
                context={"content": content}
            )
    except Exception as e:
        raise Exception(f"Error when rendering the template: {e.__cause__} {e.args}")

    try:
        user = CustomUser.objects.get(email=recipient)
    except Exception as e:
        raise Exception(f"Error when getting the user: {e.__cause__} {e.args}")

    try:
        notification = Notification.objects.create(
            notification_type=notification_type,
            recipient=user,
            subject=subject,
            description=description,
            content=message,
        )
    except Exception as e:
        raise Exception(f"Error when creating the notification: {e.__cause__} {e.args}")

    try:
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
            raise Exception(
                f"Email notification {notification} with ID {notification.id} failed to send"
            )
    except Exception as e:
        raise Exception(f"Error when sending the email: {e.__cause__} {e.args}")


@shared_task
def send_mass_email_notification(
    data: list, notification_type: str, template: str = None, sender: str = None
):
    successful = True

    try:
        with get_connection() as email_connection:
            for datatuple in data:
                subject, recipient, content, description = datatuple

                try:
                    user = CustomUser.objects.get(email=recipient)
                except Exception as e:
                    successful = False
                    raise Exception(f"Error when getting user: {e}")

                try:
                    if template:
                        message = get_template(template_name=template).render(
                            context=content
                        )
                    else:
                        message = get_template("simple_template.html").render(
                            context={"content": content}
                        )
                except Exception as e:
                    successful = False
                    raise Exception(f"Error when rendering template: {e}")

                try:
                    notification = Notification.objects.create(
                        notification_type=notification_type,
                        recipient=user,
                        subject=subject,
                        content=message,
                        description=description,
                    )
                except Exception as e:
                    successful = False
                    raise Exception(f"Error when creating notification: {e}")

                try:
                    email = EmailMessage(
                        subject=subject,
                        body=message,
                        from_email=sender,
                        to=[user.email],
                        connection=email_connection,
                    )
                    email.content_subtype = "html"
                except Exception as e:
                    successful = False
                    raise Exception(f"Error when creating email message: {e}")

                try:
                    if email.send() > 0:
                        notification.is_sent = True
                        notification.save()
                    else:
                        successful = False
                        raise Exception(
                            f"Email notification {notification} with ID {notification.id} failed to send"
                        )
                except Exception as e:
                    successful = False
                    raise Exception(f"Error when sending email: {e}")

    except Exception as e:
        successful = False
        raise Exception(f"Error when sending mass email notifications: {e}")

    return successful
