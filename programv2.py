from datetime import datetime, timedelta

import requests
import requests_cache

API_ENDPOINT = "https://backendassessmentv1.onrender.com/conference"

requests_cache.install_cache(cache_name='conference_cache', backend='sqlite', expire_after=180)

class ConferenceScheduler:
    def __init__(self):
        """
        Initialize the Conference Scheduler with the list of conferences.
        """
        self.conferences = []
        self.api_url = 'https://backendassessmentv1.onrender.com/conference'
        self.solution_url = 'https://backendassessmentv1.onrender.com/solution'

    def conference_api_call(self):
        response = requests.get(API_ENDPOINT)
        if response.status_code == 200:
            partners = response.json()['partners']
            print("Response was successful")
            return response.json
        else:
            print("Response failed. Status code", request.status_code)
        
    def create_schedule(self, data):
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
                
                # Convert date strings to datetime objects
                date1 = datetime.strptime(date1, "%Y-%m-%d")
                date2 = datetime.strptime(date2, "%Y-%m-%d")
                time_diff = (date2 - date1).total_seconds() # Get the difference between the two times.

                if time_diff == 86400:  # 86400 seconds = 1 day
                    start_date = date1
                    break
            
            conference = Conference(country, start_date, len(sorted_partners), attendees)
            self.conferences.append(conference)

        self.post_schedule()

    def post_schedule(self):
        schedule = {'Conferences': []}

        for conference in self.conferences:
            conference_data = {
                'name': conference.name,
                'startDate': conference.startDate,
                'attendeeCount': conference.attendeeCount,
                'attendees': [conference.attendees]
            }
            schedule['Conferences'].append(conference_data)

        response = requests.post(API_ENDPOINT, json=schedule)
        if response.status_code == 200:
            print("Schedule posted successfully.")
        else:
            print("Failed to post schedule.")

class Conference:
    def __init__(self, country, start_date, attendee_count, attendees):
        """
        Initialize the Conference class with country, start_date, attendee_count, and attendees.  
        """
        self.name = country
        self.startDate = start_date
        self.attendeeCount = attendee_count
        self.attendees = attendees

# Create an instance of the ConferenceScheduler class
scheduler = ConferenceScheduler()

# Call the conference_api_call method to fetch data and create the schedule
data = scheduler.conference_api_call()
schedule = scheduler.create_schedule(data)
scheduler.submit_schedule(schedule)
