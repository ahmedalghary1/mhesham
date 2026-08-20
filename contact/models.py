from django.db import models


class ContactMessage(models.Model):
    STATUS = (("unread", "Unread"), ("read", "Read"), ("archived", "Archived"))
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    company = models.CharField(max_length=120, blank=True)
    project_type = models.CharField(max_length=120)
    budget = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=12, choices=STATUS, default="unread")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} - {self.project_type}"
