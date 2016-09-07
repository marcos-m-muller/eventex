from django.core import mail
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


class SubscribePostTest(TestCase):
    def setUp(self):
        post_data = dict(name='Marcos Müller', email='marcos.m.muller@gmail.com', phone='982306271', cpf='10707955777')
        self.response = self.client.post('/inscricao/', post_data)


    def test_post(self):
        """Valid POST shpuld redirect to /inscricao/"""
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expected = 'Confirmação de inscrição'

        self.assertEqual(expected, email.subject)


    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expected = 'contato@eventex.com.br'

        self.assertEqual(expected, email.from_email)


    def test_subscrition_to(self):
        email = mail.outbox[0]
        expected = ['contato@eventex.com.br', 'marcos.m.muller@gmail.com']
        self.assertEqual(expected, email.to)


    def test_subscription_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Marcos Müller', email.body)
        self.assertIn('10707955777', email.body)
        self.assertIn('marcos.m.muller@gmail.com', email.body)
        self.assertIn('982306271', email.body)

class SubscribeInvalidPost(TestCase):
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