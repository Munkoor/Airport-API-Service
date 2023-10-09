from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from airport.models import (
    Crew,
    Airport,
    AirplaneType,
    Airplane,
    Route,
    Flight,
    Ticket,
    Order
)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "position")


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


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source = AirportSerializer(many=False, read_only=True)
    destination = AirportSerializer(many=False, read_only=True)


class TicketSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id", "route", "airplane", "departure_time", "arrival_time", "crew"
        )


class FlightListSerializer(FlightSerializer):
    crew = serializers.StringRelatedField(many=True, read_only=True)
    capacity = serializers.IntegerField(source="airplane.capacity")
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id", "route", "airplane", "departure_time", "arrival_time", "crew",
            "capacity", "tickets_available"
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(), fields=["seat", "trip"]
            )
        ]


class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(many=False, read_only=True)


class FlightDetailSerializer(FlightSerializer):
    route = RouteListSerializer(many=False, read_only=True)
    airplane = AirplaneListSerializer(many=False, read_only=True)
    crew = CrewSerializer(many=True, read_only=True)
    taken_seats = TicketSeatSerializer(source="tickets", many=True,
                                       read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id", "route", "airplane", "departure_time", "arrival_time", "crew",
            "taken_seats")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    @transaction.atomic()
    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        order = Order.objects.create(**validated_data)
        for ticket_data in tickets_data:
            Ticket.objects.create(order=order, **ticket_data)

        return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
