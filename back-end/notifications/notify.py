from django.conf import settings
from notifications.tasks import (
    send_single_email_notification,
    send_mass_email_notification,
)


def send_single_notification(
    subject: str,
    recipient: str,
    content,
    notification_type: str,
    template: str = None,
    sender: str = None,
):
    """
    Sends a single email notification.

    Args:
        recipient (str): The email address of the recipient.
        subject (str): The subject of the email.
        content: The content of the email. if you are using a custom template, content should be a dictionary. Otherwise it should be the string to be sent.
        notification_type (str): The type of the notification.
        template (str, optional): The template to use for the email. Defaults to None.
        sender (str, optional): The sender's email address. Defaults to settings.DEFAULT_FROM_EMAIL.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """

    send_single_email_notification.delay(
        subject, recipient, content, notification_type, template, sender
    )

    return True


def send_mass_notification(
    data: list,
    notification_type: str,
    template: str = None,
    sender: str = settings.DEFAULT_FROM_EMAIL,
):
    """
    Sends mass email notifications.

    Args:
        data (list of tuples): A list of tuples, where each tuple contains the recipient's details in the format (subject, recipient, content).
             - subject (str): The subject of the email.
             - recipient (str): The email address of the recipient.
             - content: The content of the email. if you are using a custom template, content should be a dictionary. Otherwise it should be the string to be sent.
        notification_type (str): The type of the notification.
        template (str, optional): The template to use for the emails. Defaults to None.
        sender (str, optional): The sender's email address. Defaults to settings.DEFAULT_FROM_EMAIL.

    Returns:
        bool: True if the emails were sent successfully, False otherwise.
    """

    send_mass_email_notification.delay(data, notification_type, template, sender)

    return True