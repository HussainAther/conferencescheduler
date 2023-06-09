import requests
import requests_cache

requests_cache.install_cache('conference_cache', backend='sqlite', expire_after=3600)

class Conference:
    def __init__(self, country, start_date, attendee_count, attendees):
        """
        Initialize the Conference class with country, start_date, attendee_count, and attendees.  
        """

class ConferenceScheduler:
    def __init__(self):
        """
        Initialize the API and solution URL.
        """
        self.api_url = 'https://backendassessmentv1.onrender.com/conference'
        self.solution_url = 'https://backendassessmentv1.onrender.com/solution'

    def make_api_call(self):
        """
        Retrieve conference data from the API point.
        """
        response = requests.get(self.api_url)
        for partner in partnercheck:
            self.country_dict[partner['country']] = self.country_dict.get(partner['country'], dict()) 
            for i in range(len(partner['availableDates'])-1):
                """
                Put code here to check available dates.
                """


scheduler = ConferenceScheduler()
