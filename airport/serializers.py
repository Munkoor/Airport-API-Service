from rest_framework import serializers
from airport.models import Crew, Airport, AirplaneType, Airplane


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = ("name", "closest_big_city")


class AirplaneTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airplane
        fields = ("name", "rows", "seats_in_row", "airplane_type")


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(many=False, read_only=True)
