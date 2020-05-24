import datetime

from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template

from .forms import PersonField, OfficeField, AreaField, RequestField, UserField, NewPersonField
from .models import Person, Office, Area, Request
from .utils import render_to_pdf, handle_uploaded_file

def index(request):
    template = 'index.html'
    context = {}

    if request.user:
        return redirect('login')

    return render(request, template, context)

def login_view(request):
    template = 'login.html'
    context = {}

    if request.user and request.user.is_active:
        return redirect(route_user(request.user)[1])

    if request.method == 'POST':
        # User login
        if request.POST.get('id') and not request.POST.get('username'):
            user_id = request.POST.get('id')
            user = get_object_or_404(User, pk=user_id)
            if route_user(user)[0]:
                messages.warning(request, 'Mila kaonty hidirana ianao', 'warning')    
            else:    
                login(request, user)
                return redirect('users')

        # Employee/Filler/Admin login
        else:
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                route = route_user(user)
                if route[0]:
                    return redirect(route[1])

            else:
                messages.warning(request, 'Hamarino fa misy diso azafady', 'warning')
            
    return render(request, template, context)

def route_user(user:object):
    employee_group = Group.objects.get(name='employee')
    filler_group = Group.objects.get(name='filler')
    manager_group = Group.objects.get(name='manager')
    
    if user.is_staff:
        return (True, 'admin:index')

    elif user in employee_group.user_set.all():
        return (True, 'employees')

    elif user in filler_group.user_set.all():
        return (True, 'filler')

    elif user in manager_group.user_set.all():
        return (True, 'manager')

    else:
        return (False, 'users')

@login_required(login_url='login')
def users(request):
    template = 'users/profile.html'
    context = {
        'user' : request.user
    }

    if request.method == 'POST':
        if request.POST.get('document_request'):
            try:
                last_request = request.user.person.request_set.latest('request_date')
                if can_request_document(last_request.request_date):
                    new_req_doc = Request.objects.create(dup_number=int(request.POST.get('request_number')), requester=request.user.person, office=request.user.person.birthplace.center)
                    new_req_doc.save()
                    messages.success(request, 'Voaray ny fangatahanao.', 'success')
                else:
                    messages.warning(request, 'Mbola tsy afaka manao fangatahana ianao.', 'warning')
            except:
                new_req_doc = Request.objects.create(dup_number=int(request.POST.get('request_number')), requester=request.user.person, office=request.user.person.birthplace.center)
                new_req_doc.save()
                messages.success(request, 'Voaray ny fangatahanao.', 'success')

    return render(request, template, context)

def can_request_document(last_request_date):
    period = datetime.date.today() - last_request_date
    if period.days >= 7:
        return True
    return False

def users_request(request):
    template = 'users/make_request.html'
    context = {}

    return render(request, template, context)
        
def users_requests(request):
    template = 'users/all_requests.html'
    context = {}

    return render(request, template, context)

def employees(request):
    template = 'employees/dashboard.html'
    context = {
        'user' : request.user,
        'office' : request.user.person.job_location.center
    }

    return render(request, template, context)

def employees_requests(request):
    template = 'employees/all_requests.html'

    context = {
        'user' : request.user,
        'office' : request.user.person.job_location.center
    }

    if request.method == 'POST':
        file_name = str(request.POST.get('request_id')) + '.pdf'
        handle_uploaded_file(request.FILES['pdf_req_file'], file_name)
        request_inst = Request.objects.get(pk=int(request.POST.get('request_id')))
        request_inst.pdf = file_name
        request_inst.state = 'Vita'
        request_inst.save()

    return render(request, template, context)

def employees_edit_user(request, *args, **kwargs):
    template = 'employees/edit_user.html'

    conn_user = request.user
    inst_person = Person.objects.get(pk=kwargs.get('person_id'))
    inst_user = inst_person.account

    person_modelform = PersonField(instance=inst_person)
    user_modelform = UserField(instance=inst_user)

    context = {
        'user' : conn_user,
        'person_modelform' : person_modelform,
        'user_modelform' : user_modelform,
        'office' : request.user.person.job_location.center
    }

    if request.method == 'POST':
        person_modelform = PersonField(request.POST, instance=inst_person)
        user_modelform = UserField(request.POST, instance=inst_user)
        if person_modelform.is_valid() and user_modelform.is_valid():
            person_modelform.save()
            user_modelform.save()
            return redirect('employees')

    return render(request, template, context)


def request_pdf(request, *args, **kwargs):
    template = 'base_pdf.html'
    context = {
        'request': Request.objects.get(pk=kwargs.get('request_id'))
    }
    return render_to_pdf(template, context)

def filler(request):
    template = 'filler/fill_form.html'

    conn_user = request.user

    person_modelform = PersonField()
    user_modelform = UserField()

    context = {
        'person_modelform' : person_modelform,
        'user_modelform' : user_modelform,
        'user' : conn_user
    }

    if request.method == 'POST':
        birthdate = request.POST.get('birthdate').split('/')
        birthdate = birthdate[2] + '-' + birthdate[1] + '-' + birthdate[0]
        user_modelform = UserField(request.POST)
        person_modelform = PersonField(request.POST)
        last_user_id = User.objects.latest('pk').pk
        new_user = User.objects.create(username=str(last_user_id+1), password='tenymiafina', first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'))
        new_pers = Person.objects.create(birthdate=birthdate, birthplace=Area.objects.get(pk=request.POST.get('birthplace')), account=new_user)
        messages.success(request, 'Ny tarehimarika hahafahany miditra dia ny : ' + str(new_user.pk), 'success')

    return render(request, template, context)

def manage_view(request):
    template = 'manage/employee_managing.html'
    employee_group = Group.objects.get(name='employee')
    context = {
        'employees' : User.objects.filter(groups=employee_group.pk)
    }

    return render(request, template, context)

def manage_edit_employee(request, *args, **kwargs):
    template = 'manage/edit_employee.html'

    conn_user = request.user
    inst_person = Person.objects.get(pk=kwargs.get('person_id'))
    inst_user = inst_person.account

    person_modelform = PersonField(instance=inst_person)
    user_modelform = UserField(instance=inst_user)

    context = {
        'user' : conn_user,
        'person_modelform' : person_modelform,
        'user_modelform' : user_modelform,
    }

    if request.method == 'POST':
        birthdate = request.POST.get('birthdate').split('/')
        birthdate = birthdate[2] + '-' + birthdate[1] + '-' + birthdate[0]
        inst_person.birthdate = birthdate
        inst_person.birthplace = Area.objects.get(pk=request.POST.get('birthplace'))
        inst_person.save()
        inst_user.first_name = request.POST.get('first_name')
        inst_user.last_name = request.POST.get('last_name')
        inst_user.save()
        return redirect('manager')

    return render(request, template, context)
def logout_view(request):
    logout(request)
    return redirect('index')