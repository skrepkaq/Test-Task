from django.shortcuts import render, redirect
from routers.services import devices


def add_devices_view(request):
    if request.method == 'POST':
        devices_raw = request.POST["devices"]  # серийные номера
        device_type_id = request.POST["devices_type"]  # id типа оборудования

        devices.add_many(request, devices_raw, device_type_id)  # обработка добавления оборудования

        # обновить страницу что бы при нажатии F5 POST запрос не отправлялся повторно
        return redirect('add_new_diveces')

    context = {'devices_types': devices.get_devices_types()}  # отображение типов оборудования на странице
    return render(request, 'add_devices.html', context)
