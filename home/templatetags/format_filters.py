from django import template

register = template.Library()

@register.filter
def format_currency_short(value):
    """
    Format large currency values into a human-readable form:
    1,200 => 1.2K ₫
    1,500,000 => 1.5M ₫
    1,200,000,000 => 1.2B ₫
    96569609709.69 => 96.6B ₫
    """
    if value is None:
        return "0 ₫"
    
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "0 ₫"

    if value >= 1_000_000_000:
        formatted = f"{value / 1_000_000_000:.1f}B ₫"
    elif value >= 1_000_000:
        formatted = f"{value / 1_000_000:.1f}M ₫"
    elif value >= 1_000:
        formatted = f"{value / 1_000:.1f}K ₫"
    else:
        formatted = f"{value:.0f} ₫"
    
    # Replace decimal comma for Vietnamese style (e.g. 1.5B → 1,5B)
    formatted = formatted.replace(".", ",")
    return formatted
