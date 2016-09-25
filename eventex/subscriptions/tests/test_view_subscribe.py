import hashlib

from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscribeTestGet(TestCase):
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
        test_case = ('<form', 1), ('<input', 6), ('type="text"', 3), ('type="email"', 1), ('type="submit"', 1)
        for content, occurrences in test_case:
                self.assertContains(self.response, content, occurrences)

    def test_csrf(self):
        """Html must have csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        post_data = dict(name='Marcos Müller', email='marcos.m.muller@gmail.com', phone='982306271', cpf='10707955777')
        self.response = self.client.post('/inscricao/', post_data)

    def test_post(self):
        """Valid POST shpuld redirect to /inscricao/1"""
        #self.assertEqual(302, self.response.status_code)
        self.assertRedirects(self.response,'/inscricao/{}/'.format(hashlib.md5(b'1').hexdigest()))

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())