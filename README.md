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


parsers
-------

Provides parsers for data formats related to Eve-Online and 3rd party utilities

* EftParser - Creates a structured representation of a ship-fit from EFT text blocks;
* KillmailParser - Not Implemented


## eve_django ##

A sample django project and utilities/apps that depend on django.
 
### eve_django.eve_sde ###
 
 
 
A set of django models and functions that wrap Eve's SDE Tables. Data currently comes from the __*.db.gz__ SQLLite dumps available at http://www.fuzzwork.co.uk/dump/
 
 
 
Almost all of the ForeignKey, OneToOne, ManyToOne, and Reverse relationships have been mapped in some form, but they can use improvement.
 
 
 
#### Setup ####
 
 
* Go to the project directory: `cd eve-code/` 
 
* Run the initial setup script: `./initial-setup.sh` (make sure __initial-setup.sh__ and __download-sde-db.sh__ are marked as executable)
 
 
_Note: the **download-sde-db.sh** script takes care of downloading sde data for you_
 
 
That should be all you need to do to get started.
 
 
#### Models and Relationships ####
 
[Still in flux, here is a PNG (that doesn't help much)](https://raw.github.com/TomNeyland/eve-code/master/eve_django/current-eve-sde-models.png)
 
 
#### Example Usage ####
 
 
 
Examples shown using a python shell launched via `python manage.py shell`, all examples assume that the classes have already been imported, eg: `from eve_sde.models import *`
 
Find all **Level 4** **Security Agents** in **The Forge**:
 
    print Agent.objects.all().filter(location__region__name='The Forge', level=4, division__name='Security')
 
    [<Agent: Lozdod Pousel>, <Agent: Adarald Ugge>, <Agent: Ailen Saakuka>, <Agent: Iitima Kisodairos>, <Agent: Aluri Yanaguno>, <Agent: Shuhola Aularoila>, <Agent: Maaltula Akora>, <Agent: Akkaras Shigakarri>, <Agent: Wahmiras Edamon>, <Agent: Kalakaaras Alamola>, <Agent: Kaila Ietsio>, <Agent: Ajeleto Ulen>, <Agent: Arai Suosaken>, <Agent: Hien Karnuras>, <Agent: Herras Soirikinen>, <Agent: Ekasvio Oshomi>, <Agent: Aokasa Dahtoh>, <Agent: Oite Pie>, <Agent: Patesobe Omokka>, <Agent: Kustiken Ikalmala>, '...(remaining elements truncated)...']`
 
 
Get the inputs to the Nanotransistor reaction:
 
    print Reaction.objects.get(name__startswith='nano').reaction_inputs.all()
 
    [<ReactionInput: Sulfuric Acid x 100>, <ReactionInput: Platinum Technite x 100>, <ReactionInput: Neo Mercurite x 100>]
 
 
Find *Level 3* and above Electromagnetic Physics Agents in The Forge:
 
    print Agent.objects.filter(research_skills__name='Electromagnetic Physics', location__region__name='The Forge', level__gte=3)
    
    [<Agent: Clel Syctonerier>, <Agent: Sakkatokka Limsen>, <Agent: Ahtamon Pavanakka>, <Agent: Aetaksan Reitufung>, <Agent: Adrek Reigeko>, <Agent: Doppepuette Ciete>]
 
 
Get a reference to the item 'Blackbird' and print its required materials:
 
    blackbird = Item.objects.get(name='Blackbird')
    
    print blackbird.material_requirements.all()
    
    [<MaterialRequirement: Tritanium x 245798>, <MaterialRequirement: Pyerite x 61845>, <MaterialRequirement: Mexallon x 18234>, <MaterialRequirement: Isogen x 4113>, <MaterialRequirement: Nocxium x 1002>, <MaterialRequirement: Zydrine x 229>, <MaterialRequirement: Megacyte x 53>]
 
 
Using the blackbird's blueprint print the extra materials:
 
    print blackbird.blueprint.extra_materials.all()
 
    [<ExtraMaterial: Tritanium x 124202.0>, <ExtraMaterial: Pyerite x 24155.0>, <ExtraMaterial: Mexallon x 17766.0>, <ExtraMaterial: Isogen x 4387.0>, <ExtraMaterial: Nocxium x 1198.0>, <ExtraMaterial: Zydrine x 321.0>, <ExtraMaterial: Megacyte x 97.0>]
 
 
Again using the blueprint, print the materials required for invention:
 
    print blackbird.blueprint.invention_materials.all()
    
    [<InventionMaterial: Datacore - Mechanical Engineering x 8.0>, <InventionMaterial: Esoteric Ship Data Interface x 1.0>, <InventionMaterial: Datacore - Caldari Starship Engineering x 8.0>]
 
 
 
Get a reference to a Region and print all of its systems:
 
    the_forge = Region.objects.get(name='The Forge')
    
    print the_forge.systems.all()
    [<System: Itamo>, <System: Mitsolen>, <System: Jatate>, <System: Mahtista>, <System: Vaankalen>, <System: Kylmabe>, <System: Ahtulaima>, <System: Geras>, <System: Sirseshin>, <System: Tuuriainas>, <System: Unpas>, <System: Shihuken>, <System: Nomaa>, <System: Ansila>, <System: Hirtamon>, <System: Hykkota>, <System: Outuni>, <System: Ohmahailen>, <System: Eskunen>, <System: Ikuchi>, '...(remaining elements truncated)...']
 
 
Print all of the stations in the forge:
 
    print the_forge.stations.all()
    
    [<Station: Gekutami V - Moon 1 - Prompt Delivery Storage>, <Station: Jakanerva III - Moon 15 - Prompt Delivery Storage>, <Station: Gekutami VII - Moon 3 - Prompt Delivery Storage>, <Station: Mitsolen IV - Moon 9 - Prompt Delivery Storage>, <Station: Jatate III - Moon 10 - Prompt Delivery Storage>, <Station: Jatate IV - Moon 17 - Prompt Delivery Storage>, <Station: Geras IX - Moon 7 - Prompt Delivery Storage>, <Station: Shihuken VII - Moon 10 - Prompt Delivery Storage>, <Station: Unpas VIII - Moon 11 - Prompt Delivery Storage>, <Station: Hentogaira III - Moon 6 - Prompt Delivery Storage>, <Station: Hentogaira IV - Prompt Delivery Storage>, <Station: Kiainti IX - Moon 8 - Prompt Delivery Storage>, <Station: Perimeter VI - Ytiri Storage>, <Station: Jita IV - Moon 6 - Ytiri Storage>, <Station: Jita V - Moon 14 - Ytiri Storage>, <Station: Urlen VII - Moon 8 - Ytiri Storage>, <Station: Otanuomi IV - Moon 5 - Ytiri Storage>, <Station: Vouskiaho IV - Moon 1 - Ytiri Storage>, <Station: Vouskiaho VI - Moon 14 - Ytiri Storage>, <Station: Otanuomi VI - Moon 9 - Ytiri Storage>, '...(remaining elements truncated)...']
 
 
And all of the moons:
 
    print the_forge.moons.all()
    
    [<Moon: Itamo I - Moon 1>, <Moon: Itamo III - Moon 1>, <Moon: Itamo IV - Moon 1>, <Moon: Itamo V - Moon 1>, <Moon: Itamo VI - Moon 1>, <Moon: Itamo VI - Moon 2>, <Moon: Itamo VI - Moon 3>, <Moon: Itamo VI - Moon 4>, <Moon: Itamo VI - Moon 5>, <Moon: Itamo VI - Moon 6>, <Moon: Itamo VI - Moon 7>, <Moon: Itamo VI - Moon 8>, <Moon: Itamo VII - Moon 1>, <Moon: Itamo VII - Moon 2>, <Moon: Itamo VII - Moon 3>, <Moon: Itamo VII - Moon 4>, <Moon: Itamo VII - Moon 5>, <Moon: Itamo VII - Moon 6>, <Moon: Itamo VIII - Moon 1>, <Moon: Itamo VIII - Moon 2>, '...(remaining elements truncated)...']
 
 
All of the moons in the_forge that can support a POS, sorted by security:
 
    print the_forge.moons.filter(system__security__lte=0.7).order_by('-security')
    
    [<Moon: Gekutami III - Moon 1>, <Moon: Gekutami IV - Moon 1>, <Moon: Gekutami IV - Moon 2>, <Moon: Gekutami V - Moon 1>, <Moon: Gekutami V - Moon 2>, <Moon: Gekutami V - Moon 3>, <Moon: Gekutami V - Moon 4>, <Moon: Gekutami VI - Moon 1>, <Moon: Gekutami VI - Moon 2>, <Moon: Gekutami VI - Moon 3>, <Moon: Gekutami VI - Moon 4>, <Moon: Gekutami VI - Moon 5>, <Moon: Gekutami VII - Moon 1>, <Moon: Gekutami VII - Moon 2>, <Moon: Gekutami VII - Moon 3>, <Moon: Gekutami VII - Moon 4>, <Moon: Gekutami VII - Moon 5>, <Moon: Gekutami VII - Moon 6>, <Moon: Gekutami VIII - Moon 1>, <Moon: Gekutami VIII - Moon 2>, '...(remaining elements truncated)...']
 
 
Get a reference to VFK and print all of its asteroid belts:
 
    vfk = System.objects.get(name='VFK-IV')
 
    print vfk.asteroid_belts.all()
    
    [<AsteroidBelt: VFK-IV III - Asteroid Belt 1>, <AsteroidBelt: VFK-IV IV - Asteroid Belt 1>, <AsteroidBelt: VFK-IV VI - Asteroid Belt 1>, <AsteroidBelt: VFK-IV VI - Asteroid Belt 2>, <AsteroidBelt: VFK-IV VI - Asteroid Belt 3>, <AsteroidBelt: VFK-IV VI - Asteroid Belt 4>, <AsteroidBelt: VFK-IV VI - Asteroid Belt 5>, <AsteroidBelt: VFK-IV VI - Asteroid Belt 6>, <AsteroidBelt: VFK-IV VI - Asteroid Belt 7>, <AsteroidBelt: VFK-IV VI - Asteroid Belt 8>, <AsteroidBelt: VFK-IV VI - Asteroid Belt 9>, <AsteroidBelt: VFK-IV VI - Asteroid Belt 10>]
 
 
Get a reference to FW Corp, Tribal Liberation Force, and print its Stations
 
    militia = Corporation.objects.get(name='Tribal Liberation Force')
    
    print militia.stations.all()
    
    [<Station: Dal I - Tribal Liberation Force Logistic Support>, <Station: Lulm IV - Tribal Liberation Force Logistic Support>, <Station: Olfeim IV - Tribal Liberation Force Logistic Support>, <Station: Ebolfer V - Tribal Liberation Force Testing Facilities>, <Station: Eszur III - Tribal Liberation Force Assembly Plant>, <Station: Auner VI - Tribal Liberation Force Logistic Support>, <Station: Hadozeko II - Tribal Liberation Force Logistic Support>, <Station: Floseswin IV - Tribal Liberation Force Logistic Support>, <Station: Gukarla V - Tribal Liberation Force Logistic Support>, <Station: Orfrold IV - Tribal Liberation Force Logistic Support>, <Station: Ofstold IV - Tribal Liberation Force Logistic Support>, <Station: Amo II - Tribal Liberation Force Logistic Support>, <Station: Abudban IV - Tribal Liberation Force Logistic Support>, <Station: Hek VII - Tribal Liberation Force Logistic Support>, <Station: Anher I - Tribal Liberation Force Logistic Support>]
 
 
Print militia agents in systems with <= 0.3 security:
 
    print print militia.agents.filter(location__system__security__lte=0.3)
    
    [<Agent: Skal Edonbald>, <Agent: Skund Manek>, <Agent: Dald Eodlan>, <Agent: Laus Haqius>, <Agent: Ahm Olruin>, <Agent: Aldwin Roar>, <Agent: Ingjaekar Hlondedbad>, <Agent: Zanmoko Osbrilar>, <Agent: Guvoli Herpwik>, <Agent: Anjell Ameko>, <Agent: Geigered Warala>, <Agent: Fusnasber Ovran>, <Agent: Svalara Ingeiker>, <Agent: Alnavar Orger>, <Agent: Amin Aiteband>, <Agent: Edore Amilgrard>, <Agent: Ragtvittak Eraleder>, <Agent: Oggur Marendei>, <Agent: Hois Odebeinn>, <Agent: Wilf Lommnersin>]
 
 
Print the Outputs/Inputs for the Enriched Uranium PI Schematic:
 
    printSchematic.objects.get(name='Enriched Uranium').schematic_outputs.all()
 
    [<SchmaticOutput: Enriched Uranium x 5>]
 
    print Schematic.objects.get(name='Enriched Uranium').schematic_inputs.all()
 
    [<SchematicInput: Precious Metals x 40>, <SchematicInput: Toxic Metals x 40>]
 
 
Print Tech 2 Caldari Ships
 
    print Item.objects.filter(group__category__name='Ship', blueprint__tech_level=2, race__name='Caldari')
    
    [<Item: Crow>, <Item: Raptor>, <Item: Buzzard>, <Item: Kitsune>, <Item: Hawk>, <Item: Harpy>, <Item: Falcon>, <Item: Rook>, <Item: Basilisk>, <Item: Cerberus>, <Item: Onyx>, <Item: Eagle>, <Item: Manticore>, <Item: Crane>, <Item: Bustard>, <Item: Widow>, <Item: Vulture>, <Item: Flycatcher>, <Item: Nighthawk>, <Item: Golem>, '...(remaining elements truncated)...']
 
 
Print all Items under the Minerals Marketgroup:
 
    print MarketGroup.objects.get(name='Minerals').items.all()
    
    [<Item: Tritanium>, <Item: Pyerite>, <Item: Mexallon>, <Item: Isogen>, <Item: Nocxium>, <Item: Zydrine>, <Item: Megacyte>, <Item: Morphite>]
 
 
Print All MetaItem versions of a Merlin:
 
  hawk = Item.objects.get(name='Hawk')
    
    print hawk.metatypes.all()
    
    [<MetaType: Hawk (Tech II)>, <MetaType: Harpy (Tech II)>, <MetaType: Worm (Faction)>]
 
 
 
 
 
## Dependencies ##
 
* django >= 1.4