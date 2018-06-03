from rest_framework import serializers
from .models import Pulse, PULSE_TYPES

class PulseSerializer(serializers.ModelSerializer):
    
   
    class Meta:
        model = Pulse
        fields = ('id', 'name', 'pulse_type', 'maximum_rabi_rate', 'polar_angle')
    
    def create(self, validated_data, many=True):
        """
        Create new Pulse
        """
        return Pulse.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update new pulse
        """
        instance.name = validated_data.get('name', instance.name)
        instance.pulse_type = validated_data.get('pulse_type', instance.pulse_type)
        instance.maximum_rabi_rate = validated_data.get('maximum_rabi_rate', instance.maximum_rabi_rate)
        instance.polar_angle = validated_data.get('polar_angle', instance.polar_angle)
        instance.save()
        return instance

