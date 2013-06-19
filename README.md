Eve-Code
=========

Python Utilities for Eve-Online.


eve_api
--------

Provides classes that wrap Eve-Online's API:

* PublicApi - Wraps all API calls that do not require authentication.
* CharacterApi - Wraps all Character related API calls, includes PublicApi functionality.
* CorporationApi -  Wraps all Corporation related API calls, includes PublicApi functionality.


**Usagge**

Import the API class you need.
```
from eve_api.api import PublicApi
api = PublicApi()
```

Call the method you need. Methods are named after the API calls they wrap.

Example, Look up a character's ID:

```api.character_ids('Foo Bar')```

Output: 

```
{'cachedUntil': datetime.datetime(2013, 7, 19, 2, 5, 37),
 'characters': [{'characterID': 0, 'name': 'Foo Bar', 'row': []}],
 'currentTime': datetime.datetime(2013, 6, 19, 2, 5, 37)}
```


Example, List Conquerable Stations:

```
api.conquerable_station_list()
```

Output:
```
{
 'currentTime': datetime.datetime(2013, 6, 19, 2, 5, 37),
    'cachedUntil': datetime.datetime(2013, 7, 19, 2, 5, 37),
    'outposts':[
        {
            'corporationID': 0,
            'corporationName': 'Some Corporation',
            'row': [],
            'solarSystemID': 30003744,
            'stationID': 0,
            'stationName': 'A-BCDE Some Station',
            'stationTypeID': 21645
        }, ...]
}
```