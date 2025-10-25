from django.shortcuts import render, redirect
import json
from expenses.models import Expenses
from contracts.models import Contracts
from django.db.models import Sum,Count,F
from customer.models import Customer
from claims.models import Claim
from django.db.models.functions import ExtractMonth, ExtractYear
import calendar
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from categories.models import InsuranceCategories
from permissions.views import has_permission
from permissions.constants import FunctionIds, ActionIds
from django.contrib import messages

from django.core.paginator import Paginator
icon_map_expense = {
        "rent": "🏢",
        "electricity": "💡",
        "internet": "🌐",
        "maintenance": "🔧",
        "advertising": "📢",
        "supplies": "🧾",
        "water": "🚰",
        "cleaning": "🧹",
        "vehicle": "🚗",
        "insurance": "🛡️",
        "salary": "💼",
        "default": "💰"
    }

# @customer_login_required

def index(request):
    # if "username" not in request.session:
    #     return redirect("employee:login")
    # group_id = request.session.get("group_id", None)
    # if not has_permission(group_id, FunctionIds.ManageHome, ActionIds.View):
    #     messages.error(request, "You do not have permission to view the home page.")
    #     return redirect("employee:login")
    context = {
        "segment": "home",
        "title": "Welcome to My Site",
        "message": "This is the home page!"
    }

    #Expenses
    expenses = Expenses.objects.all().values("content", "amount", "date")

    def get_icon(content):
        text = content.lower()
        for key, icon in icon_map_expense.items():
            if key in text:
                return icon
        return icon_map_expense["default"]
    
    expense_data = [
        {"category": e["content"], "amount": float(e["amount"]), "icon": get_icon(e["content"])}
        for e in expenses
    ]

    # Card Data
    total_revenue = Contracts.objects.filter(
        status__in=['Actived','Inactived']
    ).aggregate(
        total_revenue=Sum('actual_value')
    )['total_revenue'] or 0
    total_customer = Customer.objects.count()
    total_contract = Contracts.objects.count()
    total_claim = Claim.objects.count()
 

    #Revenue month
    # Step 1: Query Actived + Inactived contracts
    contracts = (
        Contracts.objects.filter(status__in=["Actived", "Inactived"])
        .annotate(month=ExtractMonth("start_date"), year=ExtractYear("start_date"))
        .values("month", "year")
        .annotate(revenue=Sum("actual_premium"))
        .order_by("year", "month")
    )

    # Step 2: Convert queryset to list of dicts
    all_monthly_revenue = [
        {
            "month": calendar.month_abbr[c["month"]],  # e.g. "Jan"
            "year": c["year"],
            "revenue": float(c["revenue"] or 0),
        }
        for c in contracts
    ]

    # Step 3: Convert to JSON for JS
    monthly_revenue_json = json.dumps(all_monthly_revenue)

    #Revenue Vehicle Type
    vehicle_data = get_vehicle_revenue_data()

    # =========================
    # CONTRACT TABLE
    # =========================
    today = timezone.now().date()

    contracts_qs = (
        Contracts.objects
        .select_related("created_by", "vehicle", "insurance_category", "duration")
        .filter(status__in=["Actived", "Inactived"])
    )

    contract_list = []
    for c in contracts_qs:
        if not c.start_date:
            continue

        # 🧮 Compute Expiration Date
        months = c.duration.months if c.duration else 12
        expiration_date = c.start_date + relativedelta(months=months)

        # 🕓 Days Remaining
        days_remaining = (expiration_date - today).days

        # 🧾 Build display data
        contract_list.append({
            "contractNo": c.contract_no,
            "customerName": getattr(c.created_by, "fullname", "Unknown"),
            "vehicleName": getattr(c.vehicle, "name", "Unknown"),
            "insuranceCategory": getattr(c.insurance_category, "name", "N/A"),
            "expirationDate": expiration_date.strftime("%Y-%m-%d"),
            "daysRemaining": days_remaining,
        })

   
    claims_queryset = (
        Claim.objects.filter(status='Completed')
        .annotate(month=ExtractMonth("date"), year=ExtractYear("date"))
        .values("month", "year")
        .annotate(
            personal_compensation=Sum("personal_compensation"),
            property_compensation=Sum("property_compensation")
        )
        .order_by("year", "month")
    )

    all_claims_data = [
        {
            "month": calendar.month_abbr[c["month"]],
            "year": c["year"],
            "personal_compensation": float(c["personal_compensation"] or 0),
            "property_compensation": float(c["property_compensation"] or 0),
        }
        for c in claims_queryset
    ]
    

    claims_data_json = json.dumps(all_claims_data)

    context["expense_data"] = json.dumps(expense_data)
    context['total_revenue'] = total_revenue
    context['total_customer'] = total_customer
    context['total_contract'] = total_contract
    context['total_claim'] = total_claim
    context['monthly_revenue_json'] = monthly_revenue_json
    context['vehicle_data_json'] = json.dumps(vehicle_data)
    context['contract_list'] = json.dumps(contract_list)
    context['claims_data_json'] = claims_data_json

    return render(request, "home/index.html", context)



def get_vehicle_revenue_data():
    data = (
        Contracts.objects.filter(status__in=["Actived", "Inactived"])
        .values("vehicle__vehicle_type__name")
        .annotate(
            revenue=Sum("actual_premium"),
            count=Count("id")
        )
        .order_by("vehicle__vehicle_type__name")
    )

    # Optional: map some icons based on vehicle type name
    icon_map = {
        "Motorcycle under 50cc": "🏍️",
        "Motorcycle over 50cc": "🏍️",
        "Car under 6 seats (non-commercial)": "🚗",
        "Car from 6 to 11 seats": "🚙",
        "Commercial car under 6 seats": "🚐",
        "Truck under 3.5 tons": "🚚",
        "Truck from 3.5 to 7 tons": "🚛",
        "Tractor head": "🚜",
    }

    result = [
        {
            "type": item["vehicle__vehicle_type__name"],
            "revenue": float(item["revenue"] or 0),
            "count": item["count"],
            "icon": icon_map.get(item["vehicle__vehicle_type__name"], "🚗"),
        }
        for item in data
    ]

    return result



def home_page_customer(request):
    categories = InsuranceCategories.objects.all()
    
    context = {
        "segment": "home",
        "customer": request.user
        ,"categories": categories
    }
    return render(request, "home/home-customer.html", context)

def about(request):
    context = {
        "segment": "about",
        "customer": request.user
    }
    return render(request, "home/about.html", context)
def contact(request):
    context = {
        "segment": "contact",
        "customer": request.user
    }
    return render(request, "home/contact.html", context)

def services(request):
    categories = InsuranceCategories.objects.all()
    context = {
        "segment": "services",
        "customer": request.user,
        "categories": categories
    }
    return render(request, "home/services.html", context)