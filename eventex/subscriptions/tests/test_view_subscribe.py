from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


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
        """Valid POST shpuld redirect to /inscricao/"""
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))


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


class SubscribeSuccessMessage(TestCase):
    def test_success_message(self):
        post_data = dict(name='Marcos Müller', email='marcos.m.muller@gmail.com', phone='982306271', cpf='10707955777')

        response = self.client.post('/inscricao/', post_data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')