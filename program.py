from datetime import datetime, timedelta
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
        """
        List of conferences.
        """
        self.conferences = []

    def conference_api_call(self):
        """
        Perform the API call for the conference.
        """
        response = requests.get(API_ENDPOINT)
        data = response.json()
        self.create_schedule(data)

    def create_schedule(self, data): 
        """
        Create the schedule itself.
        """
        partners = data['partners'] # Get the list of partners.
        countries = set([partner['country'] for partner in partners])

        for country in countries:
            country_partners = [partner for partner in partners if partner['country'] == country] # Find the partners by country. 
            sorted_partners = sorted(country_partners, key=lambda x: len(x['availableDates']), reverse=True) # Get the available dates for each parter pair.
            attendees = sorted_partners[0]['email'] # Get the email addresses for each attendee.
            start_date = None

            for i in range(len(sorted_partners[0]['availableDates']) - 1):
                date1 = sorted_partners[0]['availableDates'][i]
                date2 = sorted_partners[0]['availableDates'][i + 1]

                # Convert date strings to datetime objects
                date1 = datetime.strptime(date1, "%Y-%m-%d")
                date2 = datetime.strptime(date2, "%Y-%m-%d")
                time_diff = (date2 - date1).total_seconds()  # Get the difference between the two times.

                if time_diff == 86400: # 86400 seconds = 1 day
                    start_date = date1
                    break

            conference = Conference(country, start_date, len(sorted_partners), attendees)
            self.conferences.append(conference)

        self.post_schedule()

    def post_schedule(self):
        """
        Post the schedule. 
        """
        schedule = {'Conferences': []} # Initialize a schedule variable.

        for conference in self.conferences: # Search through the conferences in the list of conferences.
            conference_data = {
                'name': conference.name,
                'startDate': conference.startDate,
                'attendeeCount': conference.attendeeCount,
                'attendees': [conference.attendees]
            }
            schedule['Conferences'].append(conference_data)

        json_data = json.dumps(schedule, cls=DateTimeEncoder)  # Convert the schedule to JSON

        response = requests.get(API_ENDPOINT, json=json_data)
        if response.status_code == 200:
            print("Schedule posted successfully.")
        else:
            print("Failed to post schedule.")

class Conference:
    def __init__(self, country, start_date, attendee_count, attendees):
        """
        Initialize the Conference class with the country, start_date, attendee_count, and attendees.
        """
        self.name = country
        self.startDate = start_date
        self.attendeeCount = attendee_count
        self.attendees = attendees

# Create an instance of the ConferenceScheduler class
scheduler = ConferenceScheduler()

# Call the conference_api_call method to fetch data and create the schedule
scheduler.conference_api_call()
