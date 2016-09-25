import hashlib

from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(name='Marcos Moreira Müller', phone='21982306271', email='marcos.m.muller@gmail.com', cpf='10707955777', hashed_pk=hashlib.md5(b'1').hexdigest())
        self.response = self.client.get('/inscricao/{}/'.format(self.obj.hashed_pk))

    def test_get(self):
        self.assertTrue(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscription_detail.html')

    def test_context(self):
        print('TESTE{}TESTE'.format(self.obj.hashed_pk))
        subscription = self.response.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        content = (self.obj.name, self.obj.phone, self.obj.cpf, self.obj.email)
        with self.subTest():
            for expected in content:
                self.assertContains(self.response, expected)

class SubscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get('/inscricao/0/')
        self.assertEqual(404, resp.status_code)