from .models import SiteSetting, SocialLink


def site_context(request):
    settings_obj, _ = SiteSetting.objects.get_or_create(pk=1)
    return {
        "site_settings": settings_obj,
        "social_links": SocialLink.objects.filter(is_visible=True),
        "is_ar": request.LANGUAGE_CODE == "ar",
    }
