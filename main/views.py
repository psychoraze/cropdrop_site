from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import HttpResponse
from .forms import ContactForm


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")  # или куда нужно после входа
    else:
        form = AuthenticationForm()
    return render(request, "main/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматически залогинить после регистрации
            return redirect("home")  # отправляем на главную страницу
    else:
        form = UserCreationForm()
    return render(request, "main/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


def home(request):
    return render(request, "main/home.html")


@login_required
def pipes(request):
    return render(request, "main/pipes.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]

            # Отправка письма
            try:
                send_mail(subject, message, sender, ["psychorazed@gmail.com"])
                return redirect("success")
            except Exception as e:
                print(f"Error sending email: {e}")
        else:
            print(f"Form is not valid: {form.errors}")
    else:
        form = ContactForm()

    return render(request, "main/contact.html", {"form": form})


def success_view(request):
    return render(request, "success.html")


@login_required
def about(request):
    return render(request, "main/about.html")


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

# Глобальные переменные для хранения последних данных
latest_data = {
    "humidity_data": [],
    "servo_status": {
        "servo1": "Ожидание",
        "servo2": "Ожидание",
        "servo3": "Ожидание",
        "servo4": "Ожидание",
        "servo5": "Ожидание",
        "servo6": "Ожидание",
    },
}


@csrf_exempt
def api_data(request):
    global latest_data

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Ожидается humidity: число, servos: список из 6 элементов (True/False)
            humidity = data.get("humidity")
            servos = data.get("servos")

            if humidity is None or servos is None or len(servos) != 6:
                return JsonResponse({"error": "Некорректный формат данных"}, status=400)

            # Добавление записи во влажность
            now = datetime.now().strftime("%H:%M:%S")
            pipe_num = len(latest_data["humidity_data"]) % 6 + 1
            latest_data["humidity_data"].append(
                {"pipe": pipe_num, "humidity": humidity, "time": now}
            )

            # Ограничение последних 10 записей
            latest_data["humidity_data"] = latest_data["humidity_data"][-10:]

            # Обновление статусов сервоприводов
            for i in range(6):
                status = "Активирован" if servos[i] else "Ожидание"
                latest_data["servo_status"][f"servo{i+1}"] = status

            return JsonResponse({"status": "ok"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == "GET":
        return JsonResponse(latest_data)

    else:
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

# Хранилище данных
received_data = []


@csrf_exempt
@require_http_methods(["POST"])
def receive_data(request):
    try:
        data = json.loads(request.body)
        received_data.append(data)
        return JsonResponse({"status": "ok"})
    except json.JSONDecodeError:
        return JsonResponse({"status": "invalid json"}, status=400)


# 👉 ЭТА ФУНКЦИЯ ДЛЯ pipes.js (GET-запросов)
@require_http_methods(["GET"])
def get_data(request):
    return JsonResponse({"pipes": received_data})
