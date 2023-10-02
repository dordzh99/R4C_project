from datetime import timedelta
import json
import openpyxl

from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import RobotForm
from .models import Robot

@csrf_exempt
@require_http_methods(["GET", "POST"])
def add_robot(request):

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        form = RobotForm(data)

        if form.is_valid():
            robot = form.save(commit=False)
            robot.serial = f'{robot.model}-{robot.version}'
            robot = form.save()

            new_robot = {
                "serial": robot.serial,
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

def download_robots_in_excel(request):
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)

    robots = Robot.objects.filter(
        created__range=(start_date, end_date)
    ).values(
        'model', 'version'
    ).annotate(robot_count=Count('id'))

    unique_models = Robot.objects.filter(
        created__range=(start_date, end_date)
    ).values_list('model', flat=True).distinct()
    workbook = openpyxl.Workbook()
    for model in unique_models:

        model_robots = robots.filter(model=model)
        worksheet = workbook.create_sheet(title=model)
        worksheet.append(['Модель', 'Версия', 'Количество за неделю'])
        worksheet.column_dimensions['C'].width = 24

        for robot in model_robots:
            worksheet.append([robot['model'], robot['version'], robot['robot_count']])

    default_sheet = workbook.get_sheet_by_name('Sheet')
    workbook.remove(default_sheet)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=robots_report.xlsx'
    workbook.save(response)

    return response
