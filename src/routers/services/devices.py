import re
from django.contrib import messages
from routers.models import DeviceType, Device


def add_many(request, devices_raw: str, device_type_id: int) -> None:
    '''
    Проверяет серийные номера и добавляет их в базу данных,
    а так же отправляет на отображение возникшие ошибки
    '''
    device_type = _get_device_type_by_id(device_type_id)
    if not device_type:
        # если не найдено типа оборудования (например, пока пользователь вводил данные тип удилил из базы)
        messages.error(request, f'Типа оборудования с ID {device_type_id} не сущетвует')
        return

    for device_serial in devices_raw.split():  # разделить серийные номера
        check_res = check_device(device_serial, device_type)  # проверить каждый номер
        if check_res['state'] == 'OK':
            _add_device(device_serial, device_type)  # если всё ок - добавить в базу данных
        elif check_res['state'] == 'ERROR':
            messages.error(request, check_res['error'])  # если ошибка, отобразить её пользователю


def check_device(device_serial: str, device_type: DeviceType) -> bool:
    '''
    Проверяет серийный номер оборудования по маске
    Возвращает state OK или ERROR с ошибкой
    '''
    mask_to_re = {
        'N': r'\d',
        'A': r'[A-Z]',
        'a': r'[a-z]',
        'X': r'[A-Z\d]',
        'Z': r'[\-_@]'
    }

    re_str = ''.join([mask_to_re[s] for s in device_type.mask])  # создать re строку по маске

    if _check_device_by_serial(device_serial):  # проверить, есть ли уже данное оборудование в базе данных
        return {'state': 'ERROR', 'error': f'{device_serial} Оборудование с таким серийным номером уже существует'}
    if not re.fullmatch(re_str, device_serial):  # проверить, подходит ли серийный номер по маске
        return {'state': 'ERROR', 'error': f'{device_serial} Неверный серийный номер'}

    return {'state': 'OK'}


def get_devices_types() -> list[DeviceType]:
    '''Возвращает список из всех типов оборудования'''
    return DeviceType.objects.all()


def _get_device_type_by_id(id: int) -> DeviceType:
    '''Возвращает обьект типа оборудования по id если существует'''
    try:
        return DeviceType.objects.get(pk=id)
    except DeviceType.DoesNotExist:
        return None


def _check_device_by_serial(serial_number: str) -> bool:
    '''Возвращает True если оборудовение с данным серийным номером существует'''
    try:
        Device.objects.get(serial_number=serial_number)
    except Device.DoesNotExist:
        return False
    else:
        return True


def _add_device(device_serial: str, device_type: DeviceType) -> None:
    '''Сохраняет оборудование в базу данных'''
    Device.objects.create(type=device_type, serial_number=device_serial)
