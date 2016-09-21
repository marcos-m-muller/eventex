from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(name='Teste',
                           cpf='12345678901',
                           email='maas@asds.asd',
                           phone='21-999992222')
        self.obj.save()


    def test_create(self):
        self.assertTrue(Subscription.objects.exists())


    def test_created_at(self):
        """Subscription must have an auto creted at attribute"""
        self.assertIsInstance(self.obj.created_at, datetime)