import yaledirectory

# "api" name can be whatever is most convenient for your program
api = yaledirectory.YaleDirectory()

from pprint import pprint
results = api.search('Erik Boesen')
for person in results:
    print(f'{person.display_name} {person.residential_college_name}')
