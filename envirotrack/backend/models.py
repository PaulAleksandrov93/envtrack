from django.db import models
from django.contrib.auth.models import User


class Profession(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'


class Responsible(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество')
    profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True, verbose_name='Профессия')
    

    def __str__(self):        
        return f'{self.last_name} {self.first_name} {self.patronymic}'
    
    class Meta:
        verbose_name = 'Ответственный'
        verbose_name_plural = 'Ответственные'
    
    
class Room(models.Model):
    room_number = models.CharField(max_length=10, verbose_name='Номер помещения')
    responsible_persons = models.ManyToManyField(Responsible, related_name="rooms", verbose_name='Ответственный')
    

    def __str__(self):
        return f'Помещение № {self.room_number}'
    
    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'


class MeasurementInstrument(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    type = models.CharField(max_length=255, verbose_name='Тип')
    serial_number = models.CharField(max_length=50, verbose_name='Заводской номер')
    calibration_date = models.DateField(verbose_name='Дата поверки')
    calibration_interval = models.PositiveIntegerField(verbose_name='Межповерочный интервал')  # Интервал в месяцах, например

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Средство измерения'
        verbose_name_plural = 'Средства измерения'
    

class ParameterSet(models.Model):
    temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2)
    humidity_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    pressure_kpa = models.DecimalField(max_digits=7, decimal_places=2)
    pressure_mmhg = models.DecimalField(max_digits=7, decimal_places=2)
    time = models.TimeField()

    def __str__(self):
        return f'Parameter Set {self.id}'

    class Meta:
        verbose_name = 'Набор параметров'
        verbose_name_plural = 'Наборы параметров'


class EnviromentalParameters(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    responsible = models.ForeignKey(Responsible, related_name='environmental_parameters', on_delete=models.SET_NULL, null=True)
    measurement_instrument = models.ForeignKey(MeasurementInstrument, on_delete=models.CASCADE, null=True) 

    created_at = models.DateTimeField(null=True)  # Дата и время создания
    created_by = models.ForeignKey(User, related_name='created_parameters', on_delete=models.SET_NULL, null=True)  # Кто создал
    modified_at = models.DateTimeField(auto_now=True, null=True)  # Дата и время последнего изменения
    modified_by = models.ForeignKey(User, related_name='modified_parameters', on_delete=models.SET_NULL, null=True)  # Кто изменил

    parameter_sets = models.ManyToManyField(ParameterSet, related_name='environmental_parameters', blank=True)

    def __str__(self):
        return f'{self.room.room_number} - {self.created_at}'

    class Meta:
        verbose_name = 'Параметры окружающей среды'
        verbose_name_plural = 'Параметры окружающей среды'
