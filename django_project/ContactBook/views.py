from rest_framework.decorators import api_view
from django.shortcuts import render,redirect
from .models import Information
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .forms import InfromationForm
from django.db.models import Value as V
from django.db.models.functions import Concat   
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def pagination(page_no, contacts_list):

	default_count = 10
	last = len(contacts_list)
	if len(contacts_list) > default_count * (int(page_no) - 1):	
		if default_count * (page_no) < last:
			last = default_count * (page_no)
	return contacts_list[default_count * (page_no - 1):last]

@api_view(['GET', 'POST'])
@csrf_exempt
def Contacts(request):

	contacts = Information.objects.all()

	page_no = 1
	if request.method =="POST":
		info = Information()

		info.first_name = request.POST['first_name']
		info.last_name = request.POST['last_name']
		info.email = request.POST['email']
		info.contact_number = request.POST['contact_number']
		form = InfromationForm(request.POST,instance= info)

		if "page" in request.POST:
			page_no = int(request.POST['page'])

		if form.is_valid():
			info.save()
		else:
			return JsonResponse({'message' : "Invalid Field or Email already exists!"})

		contacts_list = Information.objects.all().values()

		return JsonResponse({'message' : "Added successfully.", 'contacts' : pagination(page_no, list(Information.objects.filter(email=info.email).values()))})

	elif request.method == "GET":
		users = list(Information.objects.all().values())

		if "page" in request.GET:
			page_no = int(request.GET['page'])

		return JsonResponse({'contacts' : pagination(page_no, users) })


@api_view(['DELETE'])
@csrf_exempt
def delete_contact(request,contact_id):

	try:
		Information.objects.get(id=contact_id).delete()
		contacts_list = Information.objects.all().values()
		return JsonResponse({'message' : "successfully deleted the contact"})
	except ObjectDoesNotExist as e:
		return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
	except Exception:
		return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@csrf_exempt
def edit_contact(request,contact_id):

	if id == 0:
		form = InfromationForm(request.POST)
	else:
		employee = Information.objects.get(id=contact_id)
		form = InfromationForm(request.POST,instance= employee)
	if form.is_valid():
		form.save()
		return JsonResponse({'message' : "successfully Updated", 'contacts' : list(Information.objects.filter(id=contact_id).values())})
	else:
		return JsonResponse({'message' : "Email already exists"})


def Union(lst1, lst2):
	final_list = lst1
	for lst2_item in lst2:
		for each in final_list:
			if lst2_item['id'] == each['id']:
				break
		else:
			final_list.append(lst2_item)

	return final_list


@api_view(['GET'])
@csrf_exempt
def SearchContact(request):

	query = ""

	if "deep_search" in request.GET:
		query = request.GET['deep_search']
		users = list(Information.objects.filter(email__icontains=query).values())
		users = Union(users, list(Information.objects.annotate(
			full_name=Concat('first_name', V(' '), 'last_name')).filter(full_name__icontains=query).values()))

	elif "query_email" in request.GET:
		query = request.GET['query_email']
		users = list(Information.objects.filter(email__icontains=query).values())

	elif "query_name" in request.GET:
		query = request.GET['query_name']
		contact = Information.objects.all()
		users = list(Information.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(full_name__icontains=query).values())

	else:
		return JsonResponse({"message" : "Invalid Request"}) 

	page_no = 1
	if "page" in request.GET:
		page_no = int(request.GET['page'])

	return JsonResponse({'results' : pagination(page_no, users)})