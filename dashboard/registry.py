from certificates.models import Certificate, Education
from contact.models import ContactMessage
from core.models import HomeContent, SiteSetting, Skill, SocialLink
from experience.models import Experience, VolunteerRole
from media_library.models import MediaAsset
from projects.models import Category, Project, ProjectImage

MODEL_REGISTRY = {
    "projects": (Project, "Projects", ("title_en", "title_ar", "client")),
    "categories": (Category, "Categories", ("name_en", "name_ar")),
    "project-images": (ProjectImage, "Project gallery", ("alt_en", "alt_ar")),
    "experience": (Experience, "Experience", ("company", "position_en", "position_ar")),
    "volunteering": (VolunteerRole, "Volunteering", ("organization", "role_en", "role_ar")),
    "skills": (Skill, "Skills", ("name_en", "name_ar")),
    "certificates": (Certificate, "Certificates", ("title_en", "title_ar")),
    "education": (Education, "Education", ("title_en", "title_ar")),
    "media": (MediaAsset, "Media library", ("title", "alt_en", "alt_ar")),
    "social": (SocialLink, "Social links", ("platform", "url")),
    "home": (HomeContent, "Home content", ("name_en", "name_ar")),
    "settings": (SiteSetting, "Site settings", ("website_name", "email")),
    "messages": (ContactMessage, "Messages", ("name", "email", "company", "message")),
}


def get_registered_model(key):
    return MODEL_REGISTRY.get(key)
