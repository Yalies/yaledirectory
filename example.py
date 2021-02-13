import yaledirectory
import os

# "api" name can be whatever is most convenient for your program
api = yaledirectory.API(os.environ['PEOPLE_SEARCH_SESSION'], os.environ['CSRF_TOKEN'])

results = api.people(first_name='Dylan', school='YC')
for person in results:
    print(f'{person.display_name} is in {person.residential_college_name}')
erik = api.person(netid='ekb33')
print(erik.email)
results = api.people(search_term='John', department='Public Health')
print('Found at least %d people named John in Public Health department.' % len(results))

print('Performing a broad request with total included')
results, total = api.people(netid='e', include_total=True)
print('There are %d matching people, but only %d were returned this time.' % (total, len(results)))
