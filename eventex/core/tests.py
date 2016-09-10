from django.test import TestCase
# Create your tests here.
class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get(self):
        """Get / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'index.html')


    def test_contains_subscription_link(self):
        self.assertContains(self.response, 'href="/inscricao/"')
        #self.assertRedirects(self.response, '/inscricao/', status_code=302, target_status_code=200)