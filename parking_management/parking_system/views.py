from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Count
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Sum
from django.db.models import F
from django.db.models import Count
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required

def base(requset):
    return render(requset,"base.html")

# @login_required(login_url="dashboard")
def reports(request):
    parked_vehicles = AddVehicle.objects.filter(status=True).count()
    departed_vehicles = AddVehicle.objects.filter(status=False).count()
    categories = Category.objects.all().count()
    total_records = AddVehicle.objects.all().count()
    parking_slots = categories  # Assuming each category is a parking slot

    # Calculate total earnings by summing up the parking charges of departed vehicles
    total_earnings = AddVehicle.objects.filter(status=False).aggregate(
        total_earnings=Sum(F('categories__parking_charge')))['total_earnings'] or 0

    context = {
        'parked_vehicles': parked_vehicles,
        'departed_vehicles': departed_vehicles,
        'categories': categories,
        'total_earnings': total_earnings,
        'total_records': total_records,
        'parking_slots': parking_slots,
    }
    return render(request, 'reports.html', context)


def dashboard(request):
    parked_vehicles = AddVehicle.objects.filter(status=True).count()
    departed_vehicles = AddVehicle.objects.filter(status=False).count()
    categories = Category.objects.all().count()
    total_records = AddVehicle.objects.all().count()
    parking_slots = Category.objects.all().count()  # Assuming each category is a parking slot

    # Calculate total earnings by summing up the parking charges of departed vehicles
    total_earnings = AddVehicle.objects.filter(status=False).aggregate(
    total_earnings=Sum(F('categories__parking_charge')))['total_earnings'] or 0
    return render(request, 'dashboard.html', {
        'parked_vehicles': parked_vehicles,
        'departed_vehicles': departed_vehicles,
        'categories': categories,
        'total_earnings': total_earnings,
        'total_records': total_records,
        'parking_slots': parking_slots,
    })


# @login_required(login_url="dashboard")
def categories(request):
    if request.method == "POST":
        p_num = request.POST.get("p_num")
        v_type = request.POST.get("v_type")
        v_limit = request.POST.get("v_limit")
        p_charge = request.POST.get("p_charge")

        # Create and save the new Category instance
        data = Category(
            parking_Area_no=p_num,
            vehicle_type=v_type,
            vehicle_limit=v_limit,
            parking_charge=p_charge
        )

        data.save()
        return redirect("category")
    # Retrieve all Category instances
    display = Category.objects.all()
    context = {
        "display": display,
    }

    return render(request, "category.html", context)

# @login_required(login_url="dashboard")
def edit_cat(request):
    dis_cat=Category.objects.all()
    context={
        "dis_cat":dis_cat
    }
    return render(request,"category.html",context)

# @login_required(login_url="dashboard")
def update_cat(request,id):
    category=Category.objects.get(id=id)
    if request.method=="POST":
        category.parking_Area_no = request.POST.get("p_num")
        category.vehicle_type = request.POST.get("v_type")
        category.vehicle_limit = request.POST.get("v_limit")
        category.parking_charge = request.POST.get("p_charge")
        category.save()
        return redirect("category")

    return render(request,"category.html")

# @login_required(login_url="dashboard")
def delete_cat(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect("category")

# @login_required(login_url="dashboard")
def activate_cat(request, id):
    cat = Category.objects.get(id=id)
    cat.status = True
    cat.save()
    return redirect('category')

# @login_required(login_url="dashboard")
def deactivate_cat(request, id):
    cat = Category.objects.get(id=id)
    cat.status = False
    cat.save()
    return redirect('category')


# @login_required(login_url="dashboard")
def vehicle_entry(request):
    categories = Category.objects.annotate(total_vehicles=Count('addvehicle')).all()
    display = AddVehicle.objects.all()

    if request.method == "POST":
        vehile_num = request.POST.get("v_num")
        v_type = request.POST.get("v_type")
        p_num = request.POST.get("p_num")
        p_charge = request.POST.get("p_charge")

        try:
            category = Category.objects.get(vehicle_type=v_type, parking_Area_no=p_num, parking_charge=p_charge)
            if category.vehicle_limit:  # Check if vehicle_limit is not empty
                if int(category.vehicle_limit) > 0 and category.vehicle_count < int(category.vehicle_limit):
                # Increment the vehicle count
                    category.vehicle_count += 1
                    category.save()
                    data = AddVehicle(vehicle_no=vehile_num, categories=category)
                    data.save()  # Save the AddVehicle object to the database
                    messages.success(request, "Vehicle added successfully")
                else:
                    messages.error(request, "Vehicle limit exceeded for this category")
            else:   
                messages.error(request, "Vehicle limit is not set for this category")
 
        except Category.DoesNotExist:
            # If the category doesn't exist, create a new one
            messages.error(request, "Category does not exist. Please create a category first.")
            return render(request, 'entry.html', {'categories': categories, 'display': display})

        return render(request, 'entry.html', {'categories': categories, 'display': display})

    return render(request, 'entry.html', {'categories': categories, 'display': display})

# @login_required(login_url="dashboard")
def activate_entry(request, id):
    entry = AddVehicle.objects.get(id=id)
    entry.status = True
    entry.save()
    return redirect('entry')

# @login_required(login_url="dashboard")
def deactivate_entry(request, id):
    entry = AddVehicle.objects.get(id=id)
    entry.status = False
    entry.save()
    return redirect('entry')

# @login_required(login_url="dashboard")
def manage_vehicles(request):
    vehicles = AddVehicle.objects.all().order_by('-arrival_time')[:30]  # Get the last 30 vehicle entries
    return render(request, "manage.html", {'vehicles': vehicles})

# @login_required(login_url="dashboard")
def manage_act_entry(request, id):
    entry = AddVehicle.objects.get(id=id)
    entry.status = True
    entry.save()
    return redirect('manage')

# @login_required(login_url="dashboard")
def manage_deact_entry(request, id):
    entry = AddVehicle.objects.get(id=id)
    entry.status = False
    entry.save()
    return redirect('manage')

# @login_required(login_url="dashboard")
def mark_as_leaved(request, vehicle_id):
    vehicle = AddVehicle.objects.get(id=vehicle_id)
    vehicle.status = True  # mark as leaved
    vehicle.save()
    return redirect('manage') 

# @login_required(login_url="dashboard")
def update_status(request):
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle_id")
        status = request.POST.get("status")

        vehicle = AddVehicle.objects.get(id=vehicle_id)
        vehicle.status = status == "Parked"
        vehicle.save()

        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

# @login_required(login_url="dashboard")
def search(request):
    if request.method == "GET":
        query = request.GET.get("query") 
        vehicles = []
        if query:
            search_filter = (
                Q(vehicle_no__icontains=query)
            )
            vehicles = AddVehicle.objects.filter(search_filter)
            return render(request, "search.html", {"vehicles": vehicles}) 
    return render(request, "search.html", {}) 

# @login_required(login_url="dashboard")
def search_act_entry(request, id):
    entry = AddVehicle.objects.get(id=id)
    entry.status = True
    entry.save()
    messages.success(request, "Entry activated")
    return redirect('search')


# @login_required(login_url="dashboard")
def search_deact_entry(request, id):
    entry = AddVehicle.objects.get(id=id)
    entry.status = False
    entry.save()
    messages.success(request, "Entry deactivated")
    return redirect('search')

def accounts(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        re_enter_password = request.POST.get('re_enter_password')

        if check_password(current_password, request.user.password):
            if new_password == re_enter_password:
                request.user.set_password(new_password)
                request.user.save()
                return JsonResponse({'success': 'Password changed successfully'})
            else:
                return JsonResponse({'error': 'New password and re-enter password do not match'})
        else:
            return JsonResponse({'error': 'Current password is incorrect'})
    return render(request, 'accounts.html')


def register(request):
    if request.method == "POST":
        fullname=request.POST.get('fullname')
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                print("Username Exists.......! Try with another name")
                return redirect("register")
            else:
                if User.objects.filter(email=email).exists():
                    print("Email Already is taken, Try Another one")
                else:
                    
                        
                    user = User.objects.create_user(
                                username=username, email=email, password=password
                            )# Create a new user using the User model
                    user.save()  # send the data to the data save

                    return redirect("login")
        else:
            print("***Password did not match***")
            return redirect("register")
    else:
        return render(request, "register.html")


def login(request):
    if (
        request.method == "POST"
    ):  # if the condition is true it should enter into the if condition
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password) # Authenticate the user using the provided 'username' and 'password'

        if user is not None:
            auth.login(request, user)
            print("Login is Successfull")
            return redirect("dashboard")

        else:
            print("Invalid Credentials")
            return redirect("login")
    else:
        return render(request, "login.html")

# @login_required(login_url="dashboard")
def logout(request):
    if request.method=="POST":
        auth.logout(request) # Log out the user using the auth.logout function
        print("Logout Succesfully....")
        return redirect('login')
    
# @login_required(login_url="dashboard")
def reset_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        re_enter_password = request.POST.get('re_enter_password')

        if check_password(current_password, request.user.password):
            if new_password == re_enter_password:
                request.user.set_password(new_password)
                request.user.save()
                return JsonResponse({'success': 'Password changed successfully'})
            else:
                return JsonResponse({'error': 'New password and re-enter password do not match'})
        else:
            return JsonResponse({'error': 'Current password is incorrect'})
    return render(request, 'accounts.html')


# @login_required(login_url="dashboard")
def show_receipt(request,id):
    reciept=AddVehicle.objects.get(id=id)
    categories = reciept.categories


    context={"reciept":reciept,"categories":categories}

    return render(request,"create_pdf.html",context)

# @login_required(login_url="dashboard")                                      
def pdf_report_create(request, id):
    reciept = AddVehicle.objects.get(id=id)
    categories = reciept.categories
    template_path = 'receipt.html'
    context = {"reciept": reciept, "categories": categories}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='pdf_convert/pdf')
    response['Content-Disposition'] = 'attachment; filename="Parking_Receipt.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
# Create your views here.                                    