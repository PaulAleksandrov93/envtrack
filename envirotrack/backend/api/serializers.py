from rest_framework import serializers
from backend.models import Responsible, Room, EnviromentalParameters, MeasurementInstrument, ParameterSet


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


class MeasurementInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementInstrument
        fields = ['id', 'name', 'type', 'serial_number', 'calibration_date', 'calibration_interval']

class ParameterSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterSet
        fields = '__all__'
        
class EnvironmentalParametersSerializer(serializers.ModelSerializer):
    room = RoomSelectSerializer()
    responsible = ResponsibleSerializer()
    measurement_instrument = MeasurementInstrumentSerializer()
    created_by = serializers.StringRelatedField()  
    modified_by = serializers.StringRelatedField()  
    parameter_sets = ParameterSetSerializer(many=True)  # Используем новое поле parameter_sets

    class Meta:
        model = EnviromentalParameters
        fields = '__all__'
        
    def update(self, instance, validated_data):
        room_data = validated_data.pop('room', None)
        responsible_data = validated_data.pop('responsible', None)
        measurement_instrument_data = validated_data.pop('measurement_instrument', None)

        if room_data:
            room, created = Room.objects.get_or_create(room_number=room_data.get('room_number'))
            instance.room = room

        if responsible_data:
            responsible, created = Responsible.objects.get_or_create(
                first_name=responsible_data.get('first_name'),
                last_name=responsible_data.get('last_name')
            )
            instance.responsible = responsible

        if measurement_instrument_data:
            measurement_instrument, created = MeasurementInstrument.objects.get_or_create(
                name=measurement_instrument_data.get('name'),
                type=measurement_instrument_data.get('type'),
                serial_number=measurement_instrument_data.get('serial_number'),
                calibration_date=measurement_instrument_data.get('calibration_date'),
                calibration_interval=measurement_instrument_data.get('calibration_interval')
            )
            instance.measurement_instrument = measurement_instrument

        if self.context['request'].user.is_authenticated:
            instance.modified_by = self.context['request'].user

        # Операции с параметрсетами
        parameter_sets_data = validated_data.pop('parameter_sets', [])

        # Удаляем все связи с параметрсетами
        instance.parameter_sets.clear()

        for param_set_data in parameter_sets_data:
            parameter_set_id = param_set_data.get('id')
            print(f"Получен parameter_set_id: {parameter_set_id}")  # Отладочный вывод

            if parameter_set_id:
                try:
                    parameter_set = ParameterSet.objects.get(id=parameter_set_id)
                except ParameterSet.DoesNotExist:
                    return Response({'error': f'ParameterSet with id {parameter_set_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = ParameterSetSerializer(data=param_set_data)
                if serializer.is_valid():
                    parameter_set = serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            instance.parameter_sets.add(parameter_set)

        instance.save()

        return instance

    def create(self, validated_data):
        room_data = validated_data.pop('room', None)
        responsible_data = validated_data.pop('responsible', None)
        measurement_instrument_data = validated_data.pop('measurement_instrument', None)

        room = None
        if room_data:
            room, created = Room.objects.get_or_create(room_number=room_data.get('room_number'))

        responsible = None
        if responsible_data:
            responsible, created = Responsible.objects.get_or_create(
                first_name=responsible_data.get('first_name'),
                last_name=responsible_data.get('last_name')
            )

        measurement_instrument = None
        if measurement_instrument_data:
            measurement_instrument, created = MeasurementInstrument.objects.get_or_create(
                **measurement_instrument_data
            )

        if self.context['request'].user.is_authenticated:
            validated_data['created_by'] = self.context['request'].user

        # Операции с параметрсетами
        parameter_sets_data = validated_data.pop('parameter_sets', [])

        instance = EnviromentalParameters.objects.create(
            room=room,
            responsible=responsible,
            measurement_instrument=measurement_instrument,
            **validated_data
        )

        for param_set_data in parameter_sets_data:
            serializer = ParameterSetSerializer(data=param_set_data)
            if serializer.is_valid():
                parameter_set = serializer.save()
                instance.parameter_sets.add(parameter_set)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return instance
    
class FilterParametersSerializer(serializers.Serializer):
    responsible = serializers.IntegerField(required=False)
    room = serializers.IntegerField(required=False)
    date = serializers.DateField(required=False)