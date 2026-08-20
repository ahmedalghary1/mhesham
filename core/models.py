from django.db import models


class OrderedModel(models.Model):
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ("sort_order", "pk")


class SiteSetting(models.Model):
    website_name = models.CharField(max_length=120, default="Mohamed Hesham")
    role_ar = models.CharField(max_length=120, default="مصمم جرافيك")
    role_en = models.CharField(max_length=120, default="Graphic Designer")
    email = models.EmailField(default="eng.mo.hesham22@gmail.com")
    phone = models.CharField(max_length=40, default="+20 127 559 3580")
    whatsapp = models.CharField(max_length=40, default="201275593580")
    location_ar = models.CharField(max_length=160, default="المنصورة، مصر")
    location_en = models.CharField(max_length=160, default="Mansoura, Egypt")
    logo = models.ImageField(upload_to="branding/", blank=True)
    favicon = models.ImageField(upload_to="branding/", blank=True)
    profile_photo = models.ImageField(upload_to="profile/", blank=True)
    default_language = models.CharField(max_length=2, choices=(("ar", "Arabic"), ("en", "English")), default="ar")
    default_title_ar = models.CharField(max_length=180, default="محمد هشام | مصمم جرافيك")
    default_title_en = models.CharField(max_length=180, default="Mohamed Hesham | Graphic Designer")
    default_description_ar = models.TextField(default="مصمم جرافيك متخصص في الهويات البصرية والسوشيال ميديا والتصميم الرقمي والمطبوع.")
    default_description_en = models.TextField(default="Graphic Designer specializing in branding, social media, digital and print design.")
    keywords = models.CharField(max_length=300, blank=True)
    open_graph_image = models.ImageField(upload_to="seo/", blank=True)
    animation_intensity = models.CharField(max_length=10, choices=(("low", "Low"), ("normal", "Normal"), ("high", "High")), default="normal")
    show_cursor = models.BooleanField(default=True)
    show_grid = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.website_name


class HomeContent(models.Model):
    name_ar = models.CharField(max_length=120, default="محمد هشام")
    name_en = models.CharField(max_length=120, default="Mohamed Hesham")
    headline_ar = models.CharField(max_length=240, default="مصمم جرافيك يحوّل الأفكار إلى تجارب بصرية مؤثرة.")
    headline_en = models.CharField(max_length=240, default="Graphic Designer creating visual experiences that make brands stand out.")
    description_ar = models.TextField(default="مصمم جرافيك بخبرة تتجاوز 4 سنوات في تصميم الهويات البصرية ومحتوى السوشيال ميديا والحملات التسويقية والتصميمات الرقمية والمطبوعة.")
    description_en = models.TextField(default="Graphic Designer with over 4 years of experience creating visually compelling work across digital and print platforms.")
    badge_ar = models.CharField(max_length=120, default="متاح للمشاريع والتعاون")
    badge_en = models.CharField(max_length=120, default="Available for projects and collaborations")
    about_ar = models.TextField(default="أصنع حلولًا بصرية واضحة ومتسقة تساعد العلامات التجارية على الظهور والتواصل بثقة.")
    about_en = models.TextField(default="I create clear, consistent visual solutions that help brands stand out and communicate with confidence.")
    years_experience = models.PositiveSmallIntegerField(default=4)
    show_volunteering = models.BooleanField(default=True)
    show_education = models.BooleanField(default=True)
    show_certificates = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "Homepage content"


class Skill(OrderedModel):
    KIND_CHOICES = (("software", "Creative software"), ("professional", "Professional"))
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    short_code = models.CharField(max_length=3, blank=True)
    icon = models.ImageField(upload_to="skills/", blank=True)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="professional")
    is_featured = models.BooleanField(default=False)
    orbit_number = models.PositiveSmallIntegerField(default=0, choices=((0, "None"), (1, "Orbit 1"), (2, "Orbit 2"), (3, "Orbit 3")))
    orbit_speed = models.PositiveSmallIntegerField(default=24)

    def __str__(self):
        return self.name_en


class SocialLink(OrderedModel):
    platform = models.CharField(max_length=60)
    url = models.CharField(max_length=500)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.platform
