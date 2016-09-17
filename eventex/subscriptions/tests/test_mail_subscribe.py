from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        post_data = dict(name='Marcos Müller', email='marcos.m.muller@gmail.com', phone='982306271', cpf='10707955777')
        self.response = self.client.post('/inscricao/', post_data)
        self.email = mail.outbox[0] 

    def test_subscription_email_subject(self):
        expected = 'Confirmação de inscrição'

        self.assertEqual(expected, self.email.subject)

    def test_subscription_email_from(self):
        expected = 'contato@eventex.com.br'

        self.assertEqual(expected, self.email.from_email)

    def test_subscrition_to(self):
        expected = ['contato@eventex.com.br', 'marcos.m.muller@gmail.com']
        self.assertEqual(expected, self.email.to)

    def test_subscription_email_body(self):
        contents = ['Marcos Müller', '10707955777', 'marcos.m.muller@gmail.com', '982306271']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
