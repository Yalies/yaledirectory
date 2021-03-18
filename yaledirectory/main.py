import requests
import re
import unidecode


class _Model(dict):
    def __repr__(self):
        return self.__class__.__name__ + '(' + str(self.__dict__) + ')'


class Person(_Model):
    def __init__(self, raw):
        self.update(raw)
        self.update(self.__dict__)

        self.directory_title = raw.get('DirectoryTitle')
        self.first_name = raw.get('FirstName')
        self.known_as = raw.get('KnownAs')
        self.middle_name = raw.get('MiddleName')
        self.last_name = raw.get('LastName')
        self.suffix = raw.get('Suffix')
        self.display_name = raw.get('DisplayName', (self.known_as or self.first_name) + ' ' + self.last_name)
        self.matched = raw.get('Matched')
        self.netid = raw.get('NetId')
        self.phone_number = raw.get('PhoneNumber')
        self.primary_organization_name = raw.get('PrimaryOrganizationName')
        self.primary_organization_code = raw.get('PrimaryOrganizationCode')
        self.primary_organization_id = raw.get('PrimaryOrganizationId')
        self.organization_name = raw.get('OrganizationName')
        self.organization_unit_name = raw.get('OrganizationUnitName')
        self.primary_school_code = raw.get('PrimarySchoolCode')
        self.primary_school_name = raw.get('PrimarySchoolName')
        self.primary_division_name = raw.get('PrimaryDivisionName')
        self.residential_college_code = raw.get('ResidentialCollegeCode')
        self.residential_college_name = raw.get('ResidentialCollegeName')
        self.student_address = raw.get('StudentAddress')
        self.student_curriculum = raw.get('StudentCurriculum')
        self.student_expected_graduation_year = raw.get('StudentExpectedGraduationYear')
        self.upi = raw.get('UPI')
        self.internal_location = raw.get('InternalLocation')
        self.email = raw.get('EmailAddress')
        self.mailbox = raw.get('Mailbox')
        self.registered_address = raw.get('RegisteredAddress')
        self.postal_address = raw.get('PostalAddress')


class Pronunciation(_Model):
    def __init__(self, raw):
        self.update(raw)
        self.update(self.__dict__)

        self.first_name = raw.get('first_name')
        self.last_name = raw.get('last_name')
        self.email = raw.get('email')
        self.recording_link = raw.get('recording_link')
        # Courtesy: provide link without apparently useless URL params
        self.recording_url = self.recording_link.split('?')[0]
        self.name_badge_link = raw.get('name_badge_link')
        self.phonetic_spelling = raw.get('phonetic_spelling')
        self.notes = raw.get('notes')
        self.custom_objects = raw.get('custom_objects')
        self.pronouns = None
        if self.custom_objects:
            self.pronouns = self.custom_objects.get('gender_pronouns')

        # HTML blobs
        self.embed_image = raw.get('embed_image')
        self.embed_iframe = raw.get('embed_iframe')


class API:
    API_ROOT = 'https://directory.yale.edu/'

    NAME_UNACCEPTABLE_RE = re.compile(r'[^a-zA-Z]+')

    def __init__(self, people_search_session_cookie, csrf_token):
        self.session = requests.Session()
        headers = {
            'X-CSRF-Token': csrf_token,
            'Content-Type': 'application/json',
        }
        cookies = {
            '_people_search_session': people_search_session_cookie,
        }
        self.session.headers.update(headers)
        self.session.cookies.update(cookies)

    def get(self, endpoint: str, params: dict = {}):
        """
        Make a GET request to the API.

        :param params: dictionary of URL params to add to request.
        """
        request = self.session.get(self.API_ROOT + endpoint, params=params)
        if request.ok:
            return request.json()
        else:
            raise Exception('API request failed. Data returned: ' + request.text)

    def post(self, endpoint: str, data: dict = {}):
        """
        Make a POST request to the API.

        :param data: JSON data to use as request body.
        """
        request = self.session.post(self.API_ROOT + endpoint, json=data)
        if request.ok:
            return request.json()
        else:
            # TODO: Can we be more helpful?
            raise Exception('API request failed. Data returned: ' + request.text)

    def clean_name(self, name):
        name = unidecode.unidecode(name)
        name = self.NAME_UNACCEPTABLE_RE.sub('', name)
        return name

    def people(self, search_term: str = '', address: str = '',
                                            department: str = '',
                                            email: str = '',
                                            first_name: str = '',
                                            last_name: str = '',
                                            netid: str = '',
                                            phone: str = '',
                                            title: str = '',
                                            upi: str = '',
                                            college: str = '',
                                            school: str = '',
                                            include_total: bool = False):
        if search_term:
            search_body = {
                'netid': '',
                'queryType': 'term',
                'query': [
                    {'pattern': ','.join(search_term.split())}
                ]
            }
        else:
            query = {
                'address': address,
                'department': department,
                'email': email,
                'firstname': self.clean_name(first_name),
                'lastname': self.clean_name(last_name),
                'netid': netid,
                'phone': phone,
                'title': title,
                'upi': upi,
                'college': college,
                'school': school,
            }
            query = {key: val for key, val in query.items() if val}
            search_body = {
                'netid': '',
                'queryType': 'field',
                'query': query
            }
        body = {
            'peoplesearch': [
                search_body
            ]
        }
        result = self.post('api', body)
        records = result['Records']
        total_records = records['TotalRecords']
        if total_records == 0:
            people = []
        else:
            record = records['Record']
            if total_records == 1:
                record = [record]
            people = [Person(raw) for raw in record]
        if include_total:
            return people, total_records
        return people

    def person(self, *args, **kwargs):
        people = self.people(*args, **kwargs)
        if len(people) != 0:
            return people[0]
        return None

    def pronounce(self, email):
        try:
            return Pronunciation(self.get('name_coach', {
                'email': email
            }))
        except Exception:
            return None
