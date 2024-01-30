from rest_framework import serializers
from .models import Responsible, Room, EnviromentalParameters, User, MeasurementInstrument


class ResponsibleSerializer(serializers.ModelSerializer):
    profession = serializers.StringRelatedField()

    class Meta:
        model = Responsible
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_number']


class RoomSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number']


class ResposibleNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsible
        fields = ['first_name', 'last_name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MeasurementInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementInstrument
        fields = ['id', 'name', 'type', 'serial_number', 'calibration_date', 'calibration_interval']


# class EnvironmentalParametersSerializer(serializers.ModelSerializer):
#     room = RoomSelectSerializer()
#     responsible = ResponsibleSerializer()
#     class Meta:
#         model = EnviromentalParameters
#         fields = ['id', 'room', 'temperature_celsius', 'humidity_percentage', 'pressure_kpa', 'pressure_mmhg', 'date_time', 'responsible']

#     def create(self, validated_data):
#         room_data = validated_data.pop('room', None)
#         responsible_data = validated_data.pop('responsible', None)
        
#         room = None
#         if room_data:
#             room, created = Room.objects.get_or_create(room_number=room_data.get('room_number'))

#         responsible = None
#         if responsible_data:
#             responsible, created = Responsible.objects.get_or_create(
#                 first_name=responsible_data.get('first_name'),
#                 last_name=responsible_data.get('last_name'),
#                 patronymic=responsible_data.get('patronymic')
#             )

#         instance = EnviromentalParameters.objects.create(
#             room=room,
#             responsible=responsible,
#             **validated_data
#         )
#         return instance

class EnvironmentalParametersSerializer(serializers.ModelSerializer):
    room = RoomSelectSerializer()
    responsible = ResponsibleSerializer()
    measurement_instrument = MeasurementInstrumentSerializer()  # Добавляем сериализатор средства измерения

    class Meta:
        model = EnviromentalParameters
        fields = ['id', 'room', 'temperature_celsius', 'humidity_percentage', 'pressure_kpa', 'pressure_mmhg', 'date_time', 'responsible', 'measurement_instrument']

    def create(self, validated_data):
        room_data = validated_data.pop('room', None)
        responsible_data = validated_data.pop('responsible', None)
        measurement_instrument_data = validated_data.pop('measurement_instrument', None)  # Добавляем обработку средства измерения

        room = None
        if room_data:
            room, created = Room.objects.get_or_create(room_number=room_data.get('room_number'))

        responsible = None
        if responsible_data:
            responsible, created = Responsible.objects.get_or_create(
                first_name=responsible_data.get('first_name'),
                last_name=responsible_data.get('last_name'),
                patronymic=responsible_data.get('patronymic')
            )

        measurement_instrument = None
        if measurement_instrument_data:
            measurement_instrument, created = MeasurementInstrument.objects.get_or_create(
                name=measurement_instrument_data.get('name'),
                type=measurement_instrument_data.get('type'),
                serial_number=measurement_instrument_data.get('serial_number'),
                calibration_date=measurement_instrument_data.get('calibration_date'),
                calibration_interval=measurement_instrument_data.get('calibration_interval')
            )

        instance = EnviromentalParameters.objects.create(
            room=room,
            responsible=responsible,
            measurement_instrument=measurement_instrument,  # Связываем объект средства измерения
            **validated_data
        )
        return instance