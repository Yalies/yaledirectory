# yaledirectory [![PyPI version](https://badge.fury.io/py/yaledirectory.svg)](https://badge.fury.io/py/yaledirectory)

> Python library for interfacing with the undocumented Yale Directory API.

[View Directory](https://directory.yale.edu)

## Setup
First, install the module:

```sh
pip3 install yaledirectory
```

Then, to use these functions, you must import the module:

```py
import yaledirectory
```

Before using the library, you must instantiate its class, for example:

```py
# "api" may be replaced by whatever name is appropriate for your application.
api = yaledirectory.API(people_search_session_cookie, csrf_token)
```

The parameters `people_search_session_cookie` and `csrf_token` can be found by using your browser's developer tools while logged into the directory to read the cookie called `_people_search_session` and the header called `X-CSRF-Token` from a request to the directory website. This allows for the API wrapper to simulate authentication.

## Use
- `api.people()`: fetch a list of all people matching given parameters.
- `api.person()`:  return the top match for the given query.

The parameters for these methods are the same:
- `search_term`: pass this parameter to perform a general search across all fields. If you do not pass `search_term`, a search will be performed using the other provided fields.
- `address`
- `department`
- `email`
- `first_name`
- `last_name`
- `netid`
- `phone`
- `upi`
- `college`
- `school`

## Examples
```py
# Fetch a list of everyone matching the search_term Dylan.
# Note: search_term is assumed to be the first parameter.
dylans = api.people('Dylan')
# Get single user, by netid
erik = api.person(netid='ekb33')
# Get people with the first name Josh in Grace Hopper in Yale College
joshes_in_hopper = api.people(first_name='Josh', college='GH', school='YC')
# Get people named John in the Public Health department
public_health_johns = api.people(search_term='John', department='Public Health')
```
See `example.py` for further usage examples.

## Author
[Erik Boesen](https://github.com/ErikBoesen)

## License
[GPL](LICENSE)
