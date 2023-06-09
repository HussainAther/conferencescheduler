import requests
import requests_cache

requests_cache.install_cache('conference_cache', backend='sqlite', expire_after=3600)

class Conference:
    def __init__(self, country, start_date, attendee_count, attendees):
        """
        Initialize the Conference class with country, start_date, attendee_count, and attendees.  
        """
        self.name = country
        self.startDate = start_date
        self.attendeeCount = attendee_count
        self.attendees = attendees

class ConferenceScheduler:
    def __init__(self):
        """
        Initialize the API and solution URL.
        """
        self.api_url = 'https://backendassessmentv1.onrender.com/conference'
        self.solution_url = 'https://backendassessmentv1.onrender.com/solution'

    def conference_api_call(self):
        """
        Retrieve conference data from the API point.
        """
        response = requests.get(self.api_url)
        data = response.json()
        return data

    def create_schedule(self, data):
        """
        Given the data create the list of conferences. 
        """
        conferences = []
        countries = {}

        for partner in data['partners']:
            country = partner['country']
            if country not in countries:
                countries[country] = {
                    'attendeeCount': 0,
                    'attendees': [],
                    'name': country,
                    'startDate': None
                }
            countries[country]['attendeeCount'] += 1
            countries[country]['attendees'].append(partner['email'])

        for country in countries.values():
            country['startDate'] = min(partner['availableDates'] for partner in data['partners'] if partner['country'] == country['name'])
            conferences.append(Conference(
                country['name'],
                country['startDate'],
                country['attendeeCount'],
                country['attendees']
            ))

        conferences.sort(key=lambda x: x.attendeeCount, reverse=True)
        return conferences

    def post_schedule(self, conferences):
        """
        Post the schedule with the given conferences. 
        """
        solution = {'Conferences': []}

        for conference in conferences:
            solution['Conferences'].append({
                'name': conference.name,
                'startDate': conference.startDate,
                'attendeeCount': conference.attendeeCount,
                'attendees': conference.attendees
            })

        response = requests.post(self.solution_url, json=solution)

        if response.status_code == 200:
            print("Solution submitted successfully.")
        else:
            print("Failed to submit the solution. Please try again.")


# Example usage
scheduler = ConferenceScheduler()
data = scheduler.conference_api_call()
schedule = scheduler.create_schedule(data)
scheduler.post_schedule(schedule)
