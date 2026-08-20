from django.test import TestCase
from .models import ContactMessage


class ContactTests(TestCase):
    payload = {
        "name": "Real Sender",
        "email": "sender@example.com",
        "phone": "",
        "company": "",
        "project_type": "Brand identity",
        "budget": "",
        "message": "I would like to discuss a complete visual identity project.",
        "website": "",
    }

    def test_valid_message_is_stored(self):
        response = self.client.post("/en/contact/send/", self.payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_honeypot_blocks_spam(self):
        payload = {**self.payload, "website": "https://spam.example"}
        self.client.post("/en/contact/send/", payload)
        self.assertEqual(ContactMessage.objects.count(), 0)
