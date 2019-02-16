import json

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt

from .models import Users
from .models import Trips

def index(request):
    return HttpResponse('heck')

@csrf_exempt
def signup(request):
	email_in = request.POST.get('email')
	password_in = request.POST.get('password')

	try:
		user = Users(email=email_in, password=make_password(password_in))
		user.save()
		return HttpResponse(json.dumps({'success':user.id}), content_type='application/json')
	except IntegrityError:
		raise Http404("email already in use")

@csrf_exempt
def login(request):
	email_in = request.POST.get('email')
	password_in = request.POST.get('password')

	user = Users.objects.get(email = email_in)
	if not check_password(password_in, user.password):
		return HttpResponse(json.dumps({'error': 'The password is incorrect'}), content_type='application/json')
	return HttpResponse(json.dumps({'success': user.id}), content_type='application/json')

@csrf_exempt
def add_trip(request):
	user_id_in = request.POST.get('user')
	car_id_in = request.POST.get('car')
	start_lat_in = request.POST.get('start_lat')
	start_lon_in = request.POST.get('start_lon')
	city_in = request.POST.get('city')
	dist_traveled_in = request.POST.get('dist_traveled')
	dist_walked_in = request.POST.get('dist_walked')
	end_time_in = request.POST.get('end_time')
	duration_in = request.POST.get('duration')

	trip = Trips(user_id = user_id_in, car_id = car_id_in, start_lat = start_lat_in, start_lon = start_lon_in, city = city_in, dist_traveled = dist_traveled_in, dist_walked = dist_walked_in, end_time = end_time_in, duration = duration_in)

	return HttpResponse(json.dumps({'trip':trip.id}, content_type='application/json'))

@csrf_exempt
def fetch_user_trips(request):
	user_id_in = request.POST.get('user')

	user = Users.objects.get(id=user_id_in)
	user_trips = list(Trips.objects.filter(user_id = user.id))
	return HttpResponse(json.dumps({'trips':users_trips}, content_type='application/json'))

@csrf_exempt
def fetch_comm_trips(request):
	city_in = request.POST.get('city')

	#latitude = float(request.POST.get('lat_str'))
	#longitude = float(request.POST.get('lon_str'))
	city_trips = list(Trips.objects.filter(city = city_in))

	return HttpResponse(json.dumps({'trips':city_trips}, content_type='application/json'))
