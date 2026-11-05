from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import TakeAppointment
from notifications.utils import send_telegram_notification


@receiver(post_save, sender=TakeAppointment)
def appointment_created_updated(sender, instance, created, **kwargs):
    """
    Sends a notification to Telegram when an appointment is created or updated.
    """
    if created:
        message = (
            f"📅 New Appointment Booked!\n"
            f"Patient: {instance.full_name}\n"
            f"Phone: {instance.phone_number}\n"
            f"Message: {instance.message}\n"
            f"Date: {instance.date.strftime('%Y-%m-%d %H:%M')}"
        )
        print("✅ New Appointment Created:", instance.full_name)
    else:
        message = (
            f"✏️ Appointment Updated!\n"
            f"Patient: {instance.full_name}\n"
            f"Phone: {instance.phone_number}\n"
            f"Message: {instance.message}\n"
            f"Date: {instance.date.strftime('%Y-%m-%d %H:%M')}"
        )
        print("♻️ Appointment Updated:", instance.full_name)

    send_telegram_notification(message)


@receiver(post_delete, sender=TakeAppointment)
def appointment_deleted(sender, instance, **kwargs):
    """
    Sends a notification to Telegram when an appointment is deleted.
    """
    message = (
        f"❌ Appointment Canceled!\n"
        f"Patient: {instance.full_name}\n"
        f"Phone: {instance.phone_number}\n"
        f"Date: {instance.date.strftime('%Y-%m-%d %H:%M')}"
    )
    print("🗑️ Appointment Deleted:", instance.full_name)
    send_telegram_notification(message)


print("✅ Signals Loaded Successfully!")  # Debugging to confirm signal loading
