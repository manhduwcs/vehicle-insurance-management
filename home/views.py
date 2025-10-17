from django.shortcuts import render
from accounts.decorators import customer_login_required
import json
from expenses.models import Expenses

icon_map = {
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
    context = {
        "segment": "home",
        "title": "Welcome to My Site",
        "message": "This is the home page!"
    }

    expenses = Expenses.objects.all().values("content", "amount", "date")

    def get_icon(content):
        text = content.lower()
        for key, icon in icon_map.items():
            if key in text:
                return icon
        return icon_map["default"]
    
    expense_data = [
        {"category": e["content"], "amount": float(e["amount"]), "icon": get_icon(e["content"])}
        for e in expenses
    ]
    context["expense_data"] = json.dumps(expense_data)
    return render(request, "home/index.html", context)
