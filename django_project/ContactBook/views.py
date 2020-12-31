from django.shortcuts import render,redirect
from .models import Information
from django.http import HttpResponseRedirect, JsonResponse
from .forms import InfromationForm
from django.db.models import Value as V
from django.db.models.functions import Concat   
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def pagination(page_no, contacts_list):

	default_count = 10
	last = len(contacts_list)
	if len(contacts_list) > default_count * (int(page_no) - 1):	
		if default_count * (page_no) < last:
			last = 10 * (page_no)
	return contacts_list[default_count * (page_no - 1):last]


@csrf_exempt
def Contacts(request):

	contacts = Information.objects.all()

	if request.method =="POST":
		info = Information()

		info.first_name = request.POST['first_name']
		info.last_name = request.POST['last_name']
		info.email = request.POST['email']
		info.contact_number = request.POST['contact_number']

		info.save()
		contacts_list = Information.objects.all().values()
		return render(request,'ContactBook/contacts.html',{'contacts':contacts_list, 'full_results' : contacts_list})
		# return JsonResponse({'message' : "Added successfully."})

	elif request.method == "GET":
		users = list(Information.objects.all().values())
		print(users)
		page_no = 1
		if "page" in request.GET:
			page_no = int(request.GET['page'])

		return render(request,'ContactBook/contacts.html', {'paginated_results' : pagination(page_no, users), 'contacts' : users})
		# return JsonResponse({'results' : pagination(page_no, users) })
	else:
		return redirect('contacts_list')
		# return render(request,'ContactBook/users_list.html', {'results' : [], "message" : "Use only GET or POST methods"})
		# return JsonResponse({"message" : "Use only GET or POST methods"})

	# return JsonResponse({'results' : list(users)[10 * (page_no - 1):last]})
		# return render(request,'ContactBook/users_list.html', {'results' : users})

	# return render(request,'ContactBook/contacts.html',{'contacts':contacts})

@csrf_exempt
def delete_contact(request,contact_id):

	if request.method == "GET":
		return JsonResponse({'message' : "USE METHOD : POST" })
	elif request.method == "POST":
		try:
			Information.objects.get(id=contact_id).delete()

			contacts_list = Information.objects.all().values()
			return JsonResponse({'message' : "successfully deleted the contact", 'contacts' : list(contacts_list)})
		except:
			return JsonResponse({'message' : "Contact doesn't exist" })
	else:
		return JsonResponse({"message" : "Use only POST method for DELETE"}) 

	# return HttpResponseRedirect("/")

@csrf_exempt
def edit_contact(request,contact_id):
	if request.method == "GET":
		Info_instance = Information.objects.get(id=contact_id)
		form = InfromationForm(instance=Info_instance)
		return render(request, "ContactBook/editcontact.html", {'form': form})
	elif request.method == "POST":
		if id == 0:
			form = InfromationForm(request.POST)
		else:
			employee = Information.objects.get(id=contact_id)
			form = InfromationForm(request.POST,instance= employee)
		if form.is_valid():
			form.save()
			contacts_list = Information.objects.filter(id=contact_id).values()
			return JsonResponse({'message' : "successfully Updated", 'contacts' : list(contacts_list)})

		else:
			return JsonResponse({'message' : "Email already exists"})

	else:
		return JsonResponse({"message" : "Use only GET or POST methods"}) 

	# return render(request, "ContactBook/editcontect.html")


def  SearchContact(request):

	query = ""

	if "search_query" in request.GET:
		query = request.GET['search_query']
		users = list(Information.objects.filter(email__icontains=query).values())
		users = users + list(Information.objects.annotate(
			full_name=Concat('first_name', V(' '), 'last_name')).filter(full_name__icontains=query).values())

	elif "query_email" in request.GET:

		query = request.GET['query_email']
		users = list(Information.objects.filter(email__icontains=query).values())

	elif "query_user" in request.GET:

		query = request.GET['query_user']
		contact = Information.objects.all()

		users = list(Information.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(full_name__icontains=query).values())

	else:
		return JsonResponse({"message" : "Invalid Request"}) 

	page_no = 1
	if "page" in request.GET:
		page_no = int(request.GET['page'])
	
	page_contacts = pagination(page_no, users)

	if page_contacts == []:
		return render(request,'ContactBook/users_list.html', {'results' : page_contacts, 'messages' : ["Page Not Found"], 'full_results' : users})
		# return JsonResponse({'message' : "Page Not Found"})

	return render(request,'ContactBook/users_list.html', {'results' : page_contacts, 'messages' : ["Search Results for " + query], 'full_results' : users})
	# return JsonResponse({'results' : page_contacts})