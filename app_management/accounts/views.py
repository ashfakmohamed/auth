from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.models import App


@login_required
def dashboard(request):
    return render(
        request,
        "apps/admin.html" if request.user.is_staff else "apps/user.html",
        {"apps": App.objects.all().order_by("name")},
    )


@login_required
def profile(request):
    return render(request, "accounts/profile.html")
