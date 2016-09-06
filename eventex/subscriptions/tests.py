from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """Get /inscricao must return http 200"""
        self.assertEqual(200,self.response.status_code)


    def test_template(self):
        """must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscription_form.html')


    def test_html(self):
        """Validate that the returned Html has 5 input tags"""
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"',3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')


    def test_csrf(self):
        """Html must have csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')


    def test_has_form(self):
        """Context must have subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)