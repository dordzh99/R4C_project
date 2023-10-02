from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from R4C.settings import FROM_EMAIL
from .models import Robot

@receiver(post_save, sender=Robot)
def notify_customer_if_robot_added(sender, instance, **kwargs):
    if instance.is_added:
        waiting_orders = Order.objects.filter(robot_serial=instance.serial, is_waiting=True)
        for order in waiting_orders:
            subject = "Робот появился в наличии!"
            message = (
                "Добрый день! Недавно вы интересовались нашим "
                f"роботом модели {instance.model}, версии {instance.version}."
                " Этот робот теперь в наличии. Если вам подходит этот вариант"
                " - пожалуйста, свяжитесь с нами."
            )
            from_email = FROM_EMAIL
            recipient_list = [order.customer]
            send_mail(subject, message, from_email, recipient_list)
            order.is_waiting = False
            order.save()
