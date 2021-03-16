# [yaledirectory](https://pypi.org/project/yaledirectory) [![PyPI version](https://badge.fury.io/py/yaledirectory.svg)](https://badge.fury.io/py/yaledirectory)

> Unofficial Python interface for the undocumented Yale Directory API.

## Note
**This package may not be the right tool for your project.**

While it is rigorously designed to provide the cleanest possible interface to the [Yale Directory](https://directory.yale.edu), that platform has unavoidable limitations. Interaction requires two authenticating tokens to be pulled through browser developer tools, and because these tokens handle short-term CAS logins, they must be manually re-fetched every few days. This means that long term authentication cannot be maintained without frustrating manual work.

Beyond the practical challenges of establishing a long term interface with the Directory, the data contained within is often spotty, duplicated, poorly formatted, and difficult to query effectively. Searching is also difficult because results are limited to 25 people at a time and cannot be paginated.

It is thus highly recommended that applications wishing to access Yale identity data make use of the Yalies API instead. [Yalies](https://yalies.io) is a student-run platform, providing clean data drawn from multiple Yale sources. Data can be queried through a flexible and thoughtfully-designed API that allows long term authentication via a formal key that won't expire. To learn more and get a key, see [the API documentation](https://yalies.io/apidocs). An official Python wrapper for the API can be found [here](https://pypi.org/project/yalies) ([GitHub](https://github.com/Yalies/python-yalies)).

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
