from datetime import timedelta
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import ContactMessageForm
from .models import ContactMessage


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    return (forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR")) or None


def contact(request):
    form = ContactMessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        ip = _client_ip(request)
        recent = ContactMessage.objects.filter(ip_address=ip, created_at__gte=timezone.now() - timedelta(minutes=10)).count() if ip else 0
        if recent >= 3:
            form.add_error(None, "Please wait before sending another message.")
        else:
            item = form.save(commit=False)
            item.ip_address = ip
            item.save()
            messages.success(request, "Message received. Mohamed will get back to you soon.")
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"ok": True, "message": "Message received."})
            return redirect("contact:contact")
    if request.headers.get("x-requested-with") == "XMLHttpRequest" and request.method == "POST":
        return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)
    return render(request, "contact/contact.html", {"form": form})


@require_POST
def quick_contact(request):
    return contact(request)
