import requests
import re
from lxml import html


class Person(dict):
    def __init__(self, raw):
        self.update(raw)
        self.update(self.__dict__)

        self.directory_title = raw.get('DirectoryTitle')
        self.first_name = raw.get('FirstName')
        self.known_as = raw.get('KnownAs')
        self.last_name = raw.get('LastName')
        self.display_name = raw.get('DisplayName', self.known_as + ' ' + self.last_name)
        self.matched = raw.get('Matched')
        self.netid = raw.get('NetId')
        self.phone_number = raw.get('PhoneNumber')
        self.primary_organization_name = raw.get('PrimaryOrganizationName')
        self.primary_school_code = raw.get('PrimarySchoolCode')
        self.primary_school_name = raw.get('PrimarySchoolName')
        self.residential_college_name = raw.get('ResidentialCollegeName')
        self.student_curriculum = raw.get('StudentCurriculum')
        self.student_expected_graduation_year = raw.get('StudentExpectedGraduationYear')
        self.upi = raw.get('UPI')


class YaleDirectory:
    API_ROOT = 'https://directory.yale.edu/'
    LOGIN_URL = 'https://secure.its.yale.edu/cas/login'

    def __init__(self, netid=None, password=None):
        self.session = requests.session()
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'secure.its.yale.edu',
            'Origin': 'https://secure.its.yale.edu',
            'Referer': 'https://secure.its.yale.edu/cas/login',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        self.session.headers.update(headers)
        if netid and password:
            login_page = self.session.get(self.LOGIN_URL)
            tree = html.fromstring(login_page.text)
            execution = list(set(tree.xpath("//input[@name='execution']/@value")))[0]
            _eventId = list(set(tree.xpath("//input[@name='_eventId']/@value")))[0]
            auth = self.session.post(self.LOGIN_URL,
                                     data={'username': netid,
                                           'password': password,
                                           'execution': execution,
                                           '_eventId': _eventId,
                                           'service': 'https://google.com',},
                                     headers=headers)
            print(self.session.cookies)

    def get(self, endpoint: str, params: dict = {}):
        """
        Make a GET request to the API.

        :param params: dictionary of custom params to add to request.
        """
        request = self.session.get(self.API_ROOT + endpoint, params=params)
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
        request = self.session.post(self.API_ROOT + endpoint, json=data)
        if request.ok:
            return request.json()
        else:
            # TODO: Can we be more helpful?
            raise Exception('API request failed. Data returned: ' + request.text)

    def search(self, name: str):
        # TODO: use actual urlencode?
        result = self.get('suggest', {'q': name.replace(' ', '%2C')})['Records']
        num_results = int(result['@TotalRecords'])
        if num_results == 0:
            return []
        record = result['Record']
        if num_results == 1:
            record = [record]
        print(record)
        return [Person(raw) for raw in record]

    # TODO: unacceptable name
    def request(self, name: str):
        return self.post('api', {'peoplesearch': [{'netid': '', 'queryType': 'term', 'query': [{'pattern': 'Erik'}]}]})
