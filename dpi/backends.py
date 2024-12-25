
import secrets
import string
from django.core.mail import send_mail
from django.conf import settings
import random
def replace_problematic_characters(password: str) -> str:
    # Define problematic characters to replace
    problematic_chars = ['"', "'", '<', '>', '\\', '/', ';', ':', ',', '.', '|', '`']
    
    # Replace problematic characters with a placeholder, e.g., '_'
    for char in problematic_chars:
        password = password.replace(char, '_')
    
    return password


def generate_password(length=12):
    # Define allowed characters (excluding problematic ones)
    allowed_chars = string.ascii_letters + string.digits + string.punctuation
    password = "mypassword"
    # password = ''.join(random.choice(allowed_chars) for _ in range(length))
    
    # Replace problematic characters
    sanitized_password = replace_problematic_characters(password)
    
    return sanitized_password


import logging

logger = logging.getLogger(__name__)

def send_password_email(email, password):
    subject = "Your Account Password"
    message = f"Hello,\n\nYour account password is: {password}\n\nPlease change it after logging in."
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        raise


