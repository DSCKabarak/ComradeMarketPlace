from django.conf import settings
from notifications.tasks import (
    send_single_email_notification,
    send_mass_email_notification,
)
from accounts.models import CustomUser

def send_single_notification(
    subject: str,
    recipient: str,
    content,
    notification_type: str,
    description: str,
    template: str = None,
    sender: str = settings.DEFAULT_FROM_EMAIL,
):
    """
    Sends a single email notification.

    Args:
        recipient (str): The email address of the recipient.
        subject (str): The subject of the email.
        content: The content of the email. if you are using a custom template, content should be a dictionary of values to be used within the template. Otherwise it should be the string to be sent.
        notification_type (str): The type of the notification.
        template (str, optional): The template to use for the email. Defaults to None.
        sender (str, optional): The sender's email address. Defaults to settings.DEFAULT_FROM_EMAIL.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        send_single_email_notification.delay(
        subject, recipient, content, description, notification_type, template, sender
    )
    except Exception as e:
        raise Exception(f"Error sending single notification: {e}")



def send_mass_notification(
    data: list,
    notification_type: str,
    template: str = None,
    sender: str = settings.DEFAULT_FROM_EMAIL,
):
    """
    Sends mass email notifications.

    Args:
        data (list of tuples): A list of tuples, where each tuple contains the recipient's details in the format (subject, recipient, content, description).
             - subject (str): The subject of the email.
             - recipient (str): The email address of the recipient.
             - content: The content of the email. if you are using a custom template, content should be a dictionary of values to be used within the template. Otherwise it should be the string to be sent.
             - description (str): The description of the notification that will be displayed to the user.
        notification_type (str): The type of the notification.
        template (str, optional): The template to use for the emails. Defaults to None.
        sender (str, optional): The sender's email address. Defaults to settings.DEFAULT_FROM_EMAIL.

    Returns:
        bool: True if the emails were sent successfully, False otherwise.
    """
    try:
        send_mass_email_notification.delay(data, notification_type, template, sender)
    except Exception as e:
        raise Exception(f"Error sending mass notification: {e}")


def send_new_category_notification(category):
    """
    Sends a notification when a new category is created.

    Args:
        category (Category): The category that was created.
    """
    email_data = list()
    users = CustomUser.objects.all()

    for user in users:
        email_data.append(
            (
                f"Hello, {user.email}, a new category has been added to the marketplace.",
                user.email,
                {
                    "category": category.category_name,
                    "sub_category": category.sub_category,
                },
                f"A new category, {category.category_name}, has been added to the marketplace.",
            )
        )
    try:
        send_mass_notification(
            data=email_data,
            notification_type="category_added",
            template="category_added.html",
        )
        print("Emails sent successfully.")
    except Exception as e:
        raise Exception(f"An error occurred while sending notifications: {str(e)}")
