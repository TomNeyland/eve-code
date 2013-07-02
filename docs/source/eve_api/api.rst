.. module:: eve_code.eve_api.api

eve_api
========

Provides classes that wrap Eve-Online's API:

* PublicApi - Wraps all API calls that do not require authentication.
* CharacterApi - Wraps all Character related API calls, includes PublicApi functionality.
* CorporationApi -  Wraps all Corporation related API calls, includes PublicApi functionality.


Usage Examples:
---------------

First, create an api object:

.. code-block:: python

   >>> from eve_code.eve_api.api import PublicApi
   >>> api = PublicApi()

Now, lets try getting the list of conquerable stations by calling :py:func:`PublicApi.conquerable_station_list`:

.. code-block:: python

    >>> print api.conquerable_station_list()
    {
        'currentTime': datetime.datetime(2013, 6, 19, 2, 5, 37),
        'cachedUntil': datetime.datetime(2013, 7, 19, 2, 5, 37),
        'outposts':[
            {
                'corporationID': 0,
                'corporationName': 'Some Corporation',
                'solarSystemID': 30003744,
                'stationID': 0,
                'stationName': 'A-BCDE Some Station',
                'stationTypeID': 21645
            }, ...]
    }


Example output from the character names function.

.. code-block:: python
    
    >>> print api.character_names(0,)
    {
        'cachedUntil': datetime.datetime(2013, 7, 19, 2, 5, 37),
        'characters': [{'characterID': 0, 'name': 'Foo Bar', 'row': []}],
        'currentTime': datetime.datetime(2013, 6, 19, 2, 5, 37)
    }



PublicApi
----------

.. autoclass:: PublicApi
    :members:
    :undoc-members:


CharacterApi
-------------

.. autoclass:: CharacterApi
    :members:
    :undoc-members:


CorporationApi
---------------

.. autoclass:: CorporationApi
    :members:
    :undoc-members: