import unittest
from unittest.mock import MagicMock
from datetime import datetime
from conference_scheduler import ConferenceScheduler, Conference, DateTimeEncoder

class ConferenceSchedulerTestCase(unittest.TestCase):
    def setUp(self):
        self.scheduler = ConferenceScheduler()

    def test_conference_api_call_success(self):
        # Mock the response for a successful API call
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "partners": [
                {
                    "country": "Country1",
                    "availableDates": ["2023-06-10", "2023-06-11"],
                    "email": "partner1@example.com"
                },
                {
                    "country": "Country2",
                    "availableDates": ["2023-06-10", "2023-06-12"],
                    "email": "partner2@example.com"
                }
            ]
        }
        requests = MagicMock()
        requests.get.return_value = mock_response

        # Assign the mocked requests module to the scheduler
        self.scheduler.requests = requests

        # Call the conference_api_call method
        self.scheduler.conference_api_call()

        # Assert that the conferences list is populated correctly
        conferences = self.scheduler.conferences
        self.assertEqual(len(conferences), 2)
        self.assertEqual(conferences[0].name, "Country1")
        self.assertEqual(conferences[0].startDate, datetime(2023, 6, 10))
        self.assertEqual(conferences[0].attendeeCount, 1)
        self.assertEqual(conferences[0].attendees, "partner1@example.com")
        self.assertEqual(conferences[1].name, "Country2")
        self.assertEqual(conferences[1].startDate, datetime(2023, 6, 10))
        self.assertEqual(conferences[1].attendeeCount, 1)
        self.assertEqual(conferences[1].attendees, "partner2@example.com")

    def test_conference_api_call_failure(self):
        # Mock the response for a failed API call
        mock_response = MagicMock()
        mock_response.status_code = 404
        requests = MagicMock()
        requests.get.return_value = mock_response

        # Assign the mocked requests module to the scheduler
        self.scheduler.requests = requests

        # Call the conference_api_call method
        self.scheduler.conference_api_call()

        # Assert that the conferences list is empty
        conferences = self.scheduler.conferences
        self.assertEqual(len(conferences), 0)

    def test_create_schedule(self):
        # Prepare data for the create_schedule method
        data = {
            "partners": [
                {
                    "country": "Country1",
                    "availableDates": ["2023-06-10", "2023-06-11"],
                    "email": "partner1@example.com"
                },
                {
                    "country": "Country2",
                    "availableDates": ["2023-06-10", "2023-06-12"],
                    "email": "partner2@example.com"
                }
            ]
        }

        # Call the create_schedule method
        self.scheduler.create_schedule(data)

        # Assert that the conferences list is populated correctly
        conferences = self.scheduler.conferences
        self.assertEqual(len(conferences), 2)
        self.assertEqual(conferences[0].name, "Country1")
        self.assertEqual(conferences[0].startDate, datetime(2023, 6, 10))
        self.assertEqual(conferences[0].attendeeCount, 1)
        self.assertEqual(conferences[0].attendees,

