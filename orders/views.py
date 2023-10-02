import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from robots.models import Robot
from .forms import OrderForm
from .models import Customer

@csrf_exempt
@require_POST
def place_order(request):
    data = json.loads(request.body.decode('utf-8'))
    form = OrderForm(data)
    robot_serial = data.get('robot_serial')
    customer = data.get('customer')
    client, created = Customer.objects.get_or_create(email=customer)

    if form.is_valid():
        if Robot.objects.filter(serial=robot_serial).exists():
            order = form.save(commit=False)
            order.customer = client
            order.is_waiting = False
            order.save()
            response_data = {
                "message": (
                f"Робот с серийным номером {order.robot_serial} есть!"
                )
            }
            status_code = 200
        
        else: 
            order = form.save(commit=False)
            order.customer = client
            order.is_waiting = True
            order.save()
            response_data = {
                "message": (
                    f"Робота {robot_serial} нет в наличии."
                    "Пожалуйста, ожидайте, мы обязательно Вам сообщим!"
                )
            }
            status_code = 200
    else:
        errors = form.errors
        return JsonResponse({"errors": errors}, status=400)
    return JsonResponse(response_data, status=status_code)
