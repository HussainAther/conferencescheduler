from datetime import datetime
import json
import requests
import requests_cache

API_ENDPOINT = "https://backendassessmentv1.onrender.com/conference"

requests_cache.install_cache(cache_name='conference_cache', backend='sqlite', expire_after=180)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class ConferenceScheduler:
    def __init__(self):
        self.conferences = []

    def conference_api_call(self):
        try:
            response = requests.get(API_ENDPOINT)
            response.raise_for_status()  # Raise exception for non-200 status codes
            data = response.json()
            self.create_schedule(data)
        except requests.exceptions.RequestException as e:
            print("Error occurred during API call:", str(e))
            # Handle the error gracefully or raise the exception to the caller

    def create_schedule(self, data):
        try:
            partners = data['partners']
            countries = set([partner['country'] for partner in partners])

            for country in countries:
                country_partners = [partner for partner in partners if partner['country'] == country]
                sorted_partners = sorted(country_partners, key=lambda x: len(x['availableDates']), reverse=True)
                attendees = sorted_partners[0]['email']
                start_date = None

                for i in range(len(sorted_partners[0]['availableDates']) - 1):
                    date1 = sorted_partners[0]['availableDates'][i]
                    date2 = sorted_partners[0]['availableDates'][i + 1]

                    date1 = datetime.strptime(date1, "%Y-%m-%d")
                    date2 = datetime.strptime(date2, "%Y-%m-%d")
                    time_diff = (date2 - date1).total_seconds()

                    if time_diff == 86400:
                        start_date = date1
                        break

                conference = Conference(country, start_date, len(sorted_partners), attendees)
                self.conferences.append(conference)

            self.post_schedule()
        except (KeyError, ValueError) as e:
            print("Error occurred while creating the schedule:", str(e))
            # Handle the error gracefully or raise the exception to the caller

    def post_schedule(self):
        try:
            schedule = {'Conferences': []}

            for conference in self.conferences:
                conference_data = {
                    'name': conference.name,
                    'startDate': conference.startDate,
                    'attendeeCount': conference.attendeeCount,
                    'attendees': [conference.attendees]
                }
                schedule['Conferences'].append(conference_data)

            json_data = json.dumps(schedule, cls=DateTimeEncoder)

            response = requests.post(API_ENDPOINT, json=json_data)
            response.raise_for_status()  # Raise exception for non-200 status codes

            if response.status_code == 200:
                print("Schedule posted successfully.")
            else:
                print("Failed to post schedule.")
        except requests.exceptions.RequestException as e:
            print("Error occurred while posting the schedule:", str(e))
            # Handle the error gracefully or raise the exception to the caller

class Conference:
    def __init__(self, country, start_date, attendee_count, attendees):
        self.name = country
        self.startDate = start_date
        self.attendeeCount = attendee_count
        self.attendees = attendees

# Create an instance of the ConferenceScheduler class
scheduler = ConferenceScheduler()

# Call the conference_api_call method to fetch data and create the schedule
scheduler.conference_api_call()
