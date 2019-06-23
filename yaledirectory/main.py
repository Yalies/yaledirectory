import requests
import re


class Person(dict):
    def __init__(self, raw):
        self.update(raw)
        self.update(self.__dict__)

        self.directory_title = raw['DirectoryTitle']
        self.display_name = raw['DisplayName']
        self.first_name = raw['FirstName']
        self.known_as = raw['KnownAs']
        self.last_name = raw['LastName']
        self.netid = raw['NetId']
        self.phone_number = raw['PhoneNumber']
        self.primary_organization_name = raw['PrimaryOrganizationName']
        self.primary_school_code = raw['PrimarySchoolCode']
        self.primary_school_name = raw['PrimarySchoolName']
        self.student_curriculum = raw['StudentCurriculum']
        self.student_expeccted_graduation_year = raw['StudentExpectedGraduationYear']
        self.upi = raw['UPI']


class YaleDirectory:
    API_ROOT = 'https://directory.yale.edu/'

    def __init__(self):
        pass

    def get(self, endpoint: str, params: dict = {}):
        """
        Make a GET request to the API.

        :param params: dictionary of custom params to add to request.
        """
        request = requests.get(self.API_ROOT + endpoint, params=params)
        if request.ok:
            return request.json()
        else:
            # TODO: Can we be more helpful?
            raise Exception('API request failed. Data returned: ' + request.text)

    def post(self, endpoint: str, data: dict = {}):
        """
        Make a POST request to the API.

        :param params: dictionary of custom data to add to request.
        """
        request = requests.post(self.API_ROOT + endpoint, json=data)
        if request.ok:
            return request.json()
        else:
            # TODO: Can we be more helpful?
            raise Exception('API request failed. Data returned: ' + request.text)

    def search(self, name: str):
        return [Person(raw) for raw in self.get('suggest', {'q': name})['Records']['Record']]

    # TODO: unacceptable name
    """
    def request(self, name: str):
        return self.post('api', {'peoplesearch': [{'netid': '', 'queryType': 'term', 'query': [{'pattern': 'Erik'}]}]})
    """
