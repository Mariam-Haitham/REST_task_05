from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from datetime import datetime
from django.utils import timezone

from .models import Flight, Booking
from .serializers import (FlightSerializer, BookingSerializer,
	BookingDetailsSerializer, UpdateBookingSerializer, AdminBookingUpdateSerializer,
		UserBookingUpdateSerializer, RegisterSerializer )
class FlightsList(ListAPIView):
	queryset = Flight.objects.all()
	serializer_class = FlightSerializer

class BookingsList(ListAPIView):

	serializer_class = BookingSerializer

	def get_queryset(self):
		queryset = Booking.objects.filter(
			date__gte = timezone.now(), 
			user = self.request.user )
		return queryset


class BookingDetails(RetrieveAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookingDetailsSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'booking_id'


class UpdateBooking(RetrieveUpdateAPIView):
	queryset = Booking.objects.all()
	serializer_class = UpdateBookingSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'booking_id'

	def get_serializer_class(self):
		if self.request.user.is_staff:
			serializer_class = AdminBookingUpdateSerializer
		else:
			serializer_class = UserBookingUpdateSerializer
		return serializer_class


class CancelBooking(DestroyAPIView):
	queryset = Booking.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'booking_id'


class BookFlight(CreateAPIView):
	serializer_class = UpdateBookingSerializer

	def perform_create(self, serializer):
		serializer.save(user=self.request.user, flight_id=self.kwargs['flight_id'])


class Register(CreateAPIView):
	serializer_class = RegisterSerializer
