from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint


class Crew(models.Model):
    select_position = (
        ('Captain', 'Captain'),
        ('Co-pilot', 'Co-pilot'),
        ('Cabin Crew', 'Cabin_crew'),
        ('Radio Operator', 'Radio_operator'),
        ('Navigator', 'Navigator'),
        ('Flight Engineer', 'Flight_engineer'),
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.CharField(max_length=20, choices=select_position, default="Cabin_crew")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}(closest big city: {self.closest_big_city})"


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE,
                               related_name="source_routes")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE,
                                    related_name="destination_routes")
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source.name} - {self.destination.name}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew)

    def __str__(self):
        return f"{self.route}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name="tickets")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["seat", "flight"],
                             name="unique_ticket_seat_flight")
        ]
        ordering = ("seat", )

    def __str__(self):
        return f"{self.flight} - (row: {self.row}, seat: {self.seat})"

    def clean(self):
        if not (1 <= self.row <= self.flight.airplane.rows):
            raise ValidationError({"row": f"row must be in range [1, {self.flight.airplane.rows}"})

        if not (1 <= self.seat <= self.flight.airplane.seats_in_row):
            raise ValidationError({"seat": f'seat must be in range [1, {self.flight.airplane.seats_in_row}]'})

    def save(
            self, force_insert=False, force_update=False, using=None,
            update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(force_insert, force_update, using,
                                        update_fields)
