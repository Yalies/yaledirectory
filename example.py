import yaledirectory
import os

# "api" name can be whatever is most convenient for your program
api = yaledirectory.API(os.environ['PEOPLE_SEARCH_SESSION'], os.environ['CSRF_TOKEN'])

results = api.people('Yamil')
for person in results:
    print(f'{person.display_name} {person.residential_college_name}')
print(api.person(netid='ekb33'))
