from django.test import TestCase

# Create your tests here.
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class PulseTests(APITestCase):
    def test_create_pulse(self):
        """
        Create pulse
        """
        url = reverse('pulses')
        data = {
            "data": {
                "type": "pulse",
                "attributes": {
                    "name": "anish pulse", 
                    "maximum_rabi_rate": 100.32,
                    "polar_angle": 0.1,
                    "pulse_type": "cinbb"
                }
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # returned data contains id
        self.assertNotEqual(response.data, data)
        self.assertEqual(response.data["data"]["attributes"], data["data"]["attributes"])
    
# TODO - write test cases for all methods
