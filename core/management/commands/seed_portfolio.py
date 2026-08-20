from datetime import date
from django.core.management.base import BaseCommand

from certificates.models import Certificate, Education
from core.models import HomeContent, SiteSetting, Skill, SocialLink
from experience.models import Experience, VolunteerRole
from projects.models import Category


class Command(BaseCommand):
    help = "Load verified content from Mohamed Hesham's CV and supplied brief."

    def handle(self, *args, **options):
        SiteSetting.objects.get_or_create(pk=1)
        HomeContent.objects.get_or_create(pk=1)

        social = [
            ("Behance", "https://www.behance.net/mohamedhesham82"),
            ("LinkedIn", "https://www.linkedin.com/in/moebnhesham"),
            ("Instagram", "https://www.instagram.com/moebnhesham?igsh=dmc4YTFianByYzlk"),
            ("Pinterest", "https://pin.it/5CfaFPxfb"),
            ("WhatsApp", "https://wa.me/201275593580"),
            ("Email", "mailto:eng.mo.hesham22@gmail.com"),
            ("Full Portfolio", "https://drive.google.com/drive/folders/1EDXVY7Mnkp_k1WtBFM54d6wniQ1RMhKm?usp=drive_link"),
        ]
        for order, (platform, url) in enumerate(social):
            SocialLink.objects.update_or_create(platform=platform, defaults={"url": url, "sort_order": order})

        categories = [
            ("Social Media", "سوشيال ميديا", "social-media"), ("Branding", "هوية بصرية", "branding"),
            ("Advertising", "إعلانات", "advertising"), ("Print", "مطبوعات", "print"),
            ("Campaigns", "حملات", "campaigns"), ("UI/UX", "واجهات وتجربة مستخدم", "ui-ux"),
            ("Creative Design", "تصميم إبداعي", "creative-design"),
        ]
        for order, (en, ar, slug) in enumerate(categories):
            Category.objects.update_or_create(slug=slug, defaults={"name_en": en, "name_ar": ar, "sort_order": order})

        skills = [
            ("Photoshop", "فوتوشوب", "Ps", "software", 1), ("Illustrator", "إليستريتور", "Ai", "software", 1),
            ("Figma", "فيجما", "Fg", "software", 2), ("Canva", "كانفا", "Cv", "software", 2),
            ("InDesign", "إنديزاين", "Id", "software", 3), ("Premiere Pro", "بريمير برو", "Pr", "software", 3),
            ("Graphic Design", "تصميم جرافيك", "", "professional", 0), ("Branding", "تصميم الهوية", "", "professional", 0),
            ("Marketing", "التسويق", "", "professional", 0), ("Project Management", "إدارة المشاريع", "", "professional", 0),
            ("Leadership", "القيادة", "", "professional", 0), ("Fast Learning", "التعلم السريع", "", "professional", 0),
            ("Visual Storytelling", "السرد البصري", "", "professional", 0),
        ]
        for order, (en, ar, code, kind, orbit) in enumerate(skills):
            Skill.objects.update_or_create(name_en=en, defaults={"name_ar": ar, "short_code": code, "kind": kind, "orbit_number": orbit, "is_featured": orbit > 0, "sort_order": order})

        experiences = [
            ("Bunyan Growth", "مصمم جرافيك", "Graphic Designer", "السعودية", "Saudi Arabia", "Remote - Part Time", date(2026,5,1), None, True),
            ("Manara Digital", "مصمم جرافيك", "Graphic Designer", "السعودية", "Saudi Arabia", "Remote - Full Time", date(2026,5,1), None, True),
            ("Dawama", "مصمم جرافيك", "Graphic Designer", "السعودية", "Saudi Arabia", "Remote - Part Time", date(2026,4,1), None, True),
            ("Freelancer", "مصمم جرافيك مستقل", "Freelance Graphic Designer", "", "", "Freelance", date(2023,10,1), None, True),
            ("Plannexa.co", "مصمم جرافيك", "Graphic Designer", "السعودية", "Saudi Arabia", "Remote - Part Time", date(2026,2,1), date(2026,7,1), False),
            ("Active Milk For Dairy Solutions Co", "مصمم جرافيك", "Graphic Designer", "", "", "Remote - Part Time", date(2025,5,1), None, True),
            ("SAWA For Training and Consultation", "مصمم جرافيك", "Graphic Designer", "", "", "Remote", date(2026,1,1), date(2026,4,1), False),
            ("Alex Soft House", "مصمم جرافيك", "Graphic Designer", "", "", "Remote", date(2025,12,1), date(2026,2,1), False),
            ("Khotwat For Quality", "مصمم جرافيك", "Graphic Designer", "", "", "Hybrid", date(2025,10,1), date(2026,1,1), False),
            ("Planet Science Library Co", "مصمم جرافيك", "Graphic Designer", "", "", "On-site", date(2023,8,1), date(2023,10,1), False),
        ]
        for order, row in enumerate(experiences):
            company, pos_ar, pos_en, loc_ar, loc_en, kind, start, end, current = row
            Experience.objects.update_or_create(company=company, start_date=start, defaults={"position_ar": pos_ar, "position_en": pos_en, "location_ar": loc_ar, "location_en": loc_en, "employment_type": kind, "end_date": end, "is_current": current, "sort_order": order})

        volunteering = [
            ("Way2health Team", "عضو ميديا", "Media Member", date(2023,2,1), date(2024,9,1), False),
            ("Way2health Team", "رئيس العلاقات العامة", "PR Head", date(2024,9,1), date(2026,1,1), False),
            ("Feqh Agri Eng Team", "المؤسس وقائد الفريق", "Founder & Team Leader", date(2023,9,1), None, True),
            ("Food Sci Club Platform", "المؤسس والرئيس التنفيذي", "Founder & CEO", date(2023,9,1), None, True),
            ("Bionic Team", "عضو ميديا", "Media Member", date(2023,9,1), date(2024,9,1), False),
            ("URI Team", "عضو ميديا", "Media Member", date(2023,9,1), date(2024,9,1), False),
        ]
        for order, (org, ar, en, start, end, current) in enumerate(volunteering):
            VolunteerRole.objects.update_or_create(organization=org, role_en=en, defaults={"role_ar": ar, "start_date": start, "end_date": end, "is_current": current, "sort_order": order})

        education = [
            ("بكالوريوس الزراعة - برنامج علوم وتكنولوجيا الأغذية", "Bachelor of Agriculture - Food Science and Technology Program", "جامعة المنصورة", "Mansoura University", 2026),
            ("تطوير الأعمال - حاضنة أورنج كورنرز مصر", "Business Development at Orange Corners Egypt Incubation", "أورنج كورنرز مصر", "Orange Corners Egypt", None),
        ]
        for order, (ar, en, inst_ar, inst_en, year) in enumerate(education):
            Education.objects.update_or_create(title_en=en, defaults={"title_ar": ar, "institution_ar": inst_ar, "institution_en": inst_en, "year": year, "sort_order": order})

        certificates = [("التسويق الذاتي", "Self Marketing", 2023), ("البحث العلمي", "Scientific Research", 2024), ("ريادة الأعمال", "Entrepreneurship", 2024), ("إدارة الجودة", "Quality Management", 2025)]
        for order, (ar, en, year) in enumerate(certificates):
            Certificate.objects.update_or_create(title_en=en, defaults={"title_ar": ar, "year": year, "sort_order": order})

        self.stdout.write(self.style.SUCCESS("Verified portfolio content loaded. No sample projects were created."))
