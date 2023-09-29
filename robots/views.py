import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import RobotForm

@csrf_exempt
@require_http_methods(["GET", "POST"])
def add_robot(request):

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        form = RobotForm(data)

        if form.is_valid():
            robot = form.save()
            new_robot = {
                "serial": f'{robot.model}-{robot.version}',
                "model": robot.model,
                "version": robot.version,
                "created": robot.created.strftime('%Y-%m-%d %H:%M:%S')
            }
            return JsonResponse({
                "message": "Робот добавлен!",
                "robot": new_robot})

        else:
            return JsonResponse({
                "message": "Ошибка валидации формы",
                "errors": form.errors})
