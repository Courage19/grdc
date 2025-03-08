from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm
from .models import Stand, Application, TitleDeedRequest

def home(request):
    return render(request, "base.html")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("admin_dashboard" if user.is_staff else "user_dashboard")  # ✅ Correct Dashboard Redirect
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("admin_dashboard" if user.is_staff else "user_dashboard")  # ✅ Correct Dashboard Redirect
        
        # Show error message if authentication fails
        return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("home")

def user_dashboard(request):
    return render(request, "user_dashboard.html")

def admin_dashboard(request):
    return render(request, "admin_dashboard.html")


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Stand, Application
from django.contrib import messages

@login_required
def view_stands(request):
    stands = Stand.objects.filter(is_available=True)
    return render(request, "user/view_stands.html", {"stands": stands})

@login_required
def apply_for_stand(request, stand_id):
    stand = get_object_or_404(Stand, id=stand_id)

    if Application.objects.filter(user=request.user, stand=stand).exists():
        messages.warning(request, "You have already applied for this stand.")
    else:
        Application.objects.create(user=request.user, stand=stand, status="Pending")
        stand.is_available = False  # Reserve the stand during processing
        stand.save()
        messages.success(request, "Application submitted successfully!")

    return redirect("view_stands")

@login_required
def view_application_status(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, "user/application_status.html", {"applications": applications})

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def manage_stands(request):
    stands = Stand.objects.all()
    return render(request, "admin/manage_stands.html", {"stands": stands})

@staff_member_required
def view_applied_stands(request):
    applications = Application.objects.all()
    return render(request, "admin/view_applied_stands.html", {"applications": applications})

@staff_member_required
def approve_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    application.status = "Approved"
    application.stand.is_available = False  # Stand now taken
    application.stand.save()
    application.save()
    messages.success(request, "Application approved successfully!")
    return redirect("view_applied_stands")

@staff_member_required
def reject_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    application.status = "Rejected"
    application.stand.is_available = True  # Make stand available again
    application.stand.save()
    application.save()
    messages.error(request, "Application rejected.")
    return redirect("view_applied_stands")

@staff_member_required
def add_stand(request):
    if request.method == "POST":
        stand_number = request.POST["stand_number"]
        location = request.POST["location"]
        size = request.POST["size"]
        price = request.POST["price"]
        
        Stand.objects.create(
            stand_number=stand_number, location=location, size=size, price=price, is_available=True
        )
        messages.success(request, "New stand added successfully!")
        return redirect("manage_stands")
    
    return render(request, "admin/add_stand.html")
@staff_member_required
def edit_stand(request, stand_id):
    stand = get_object_or_404(Stand, id=stand_id)
    
    if request.method == "POST":
        stand.stand_number = request.POST["stand_number"]
        stand.location = request.POST["location"]
        stand.size = request.POST["size"]
        stand.price = request.POST["price"]
        stand.save()
        messages.success(request, "Stand updated successfully!")
        return redirect("manage_stands")

    return render(request, "admin/edit_stand.html", {"stand": stand})
@staff_member_required
def delete_stand(request, stand_id):
    stand = get_object_or_404(Stand, id=stand_id)
    stand.delete()
    messages.success(request, "Stand deleted successfully!")
    return redirect("manage_stands")
@staff_member_required
def generate_report(request):
    total_stands = Stand.objects.count()
    total_applications = Application.objects.count()
    approved = Application.objects.filter(status="Approved").count()
    rejected = Application.objects.filter(status="Rejected").count()
    pending = Application.objects.filter(status="Pending").count()

    return render(request, "admin/report.html", {
        "total_stands": total_stands,
        "total_applications": total_applications,
        "approved": approved,
        "rejected": rejected,
        "pending": pending,
    })
@staff_member_required
def manage_users(request):
    users = User.objects.all()
    return render(request, "admin/manage_users.html", {"users": users})
@staff_member_required
def add_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        is_staff = "is_staff" in request.POST  # Check if admin checkbox is selected

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = is_staff  # Make user an admin if checked
        user.save()

        messages.success(request, "New user added successfully!")
        return redirect("manage_users")

    return render(request, "admin/add_user.html")
@staff_member_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.is_staff = "is_staff" in request.POST  # Update admin status
        user.save()

        messages.success(request, "User updated successfully!")
        return redirect("manage_users")

    return render(request, "admin/edit_user.html", {"user": user})
@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()

    messages.success(request, "User deleted successfully!")
    return redirect("manage_users")

