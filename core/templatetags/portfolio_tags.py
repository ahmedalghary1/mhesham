from django import template
from django.utils.translation import get_language

register = template.Library()


@register.filter
def localize(obj, field):
    if obj is None:
        return ""
    language = "ar" if get_language() == "ar" else "en"
    return getattr(obj, f"{field}_{language}", "") or getattr(obj, f"{field}_en", "")


@register.filter
def field_value(form, name):
    return form[name]


@register.simple_tag(takes_context=True)
def alternate_language_url(context, language):
    request = context["request"]
    path = request.path
    pieces = path.lstrip("/").split("/", 1)
    suffix = pieces[1] if len(pieces) > 1 and pieces[0] in {"ar", "en"} else "/".join(pieces)
    return f"/{language}/{suffix}" if suffix else f"/{language}/"
