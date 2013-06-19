"""A parser for EFT blocks.


Input Format:
-------------

An EFT text block.

[Apocalypse, Ratting sansha]

Heat Sink II
Heat Sink II
Heat Sink II
Damage Control II
Armor EM Hardener II
Armor Thermic Hardener II
Dark Blood Large Armor Repairer

Fleeting Propulsion Inhibitor I
Cap Recharger II
Cap Recharger II
Cap Recharger II

Mega Pulse Laser II, Multifrequency L
Mega Pulse Laser II, Multifrequency L
Mega Pulse Laser II, Multifrequency L
Mega Pulse Laser II, Multifrequency L
Mega Pulse Laser II, Multifrequency L
Mega Pulse Laser II, Multifrequency L
Mega Pulse Laser II, Multifrequency L
Mega Pulse Laser II, Multifrequency L

Large Semiconductor Memory Cell I
Large Auxiliary Nano Pump I
Large Auxiliary Nano Pump I


Hammerhead II x5
Hobgoblin II x5


Output Format:
--------------

A dictonary with the keys 'ship_type', 'fit_name', and 'items'. The value for 'items' is a list
of dictionaries that represent each of the items included in the EFT Fit.

{
    "ship_type": "Apocalypse",
    "fit_name": "Ratting sansha",
    "items": [
        {"name": "Mega Pulse Laser II", "charge_name": "Multifrequency L", "count": 1},
        {"name": "Mega Pulse Laser II", "charge_name": "Multifrequency L", "count": 1},
        {"name": "Mega Pulse Laser II", "charge_name": "Multifrequency L", "count": 1},
        {"name": "Mega Pulse Laser II", "charge_name": "Multifrequency L", "count": 1},
        {"name": "Mega Pulse Laser II", "charge_name": "Multifrequency L", "count": 1},
        {"name": "Mega Pulse Laser II", "charge_name": "Multifrequency L", "count": 1},
        {"name": "Mega Pulse Laser II", "charge_name": "Multifrequency L", "count": 1},
        {"name": "Mega Pulse Laser II", "charge_name": "Multifrequency L", "count": 1},

        {"name": "Cap Recharger II", "charge_name": ""},
        {"name": "Cap Recharger II", "charge_name": "", "count": 1},
        {"name": "Cap Recharger II", "charge_name": "", "count": 1},
        {"name": "Fleeting Propulsion Inhibitor I", "charge_name": "", "count": 1},

        {"name": "Heat Sink II", "charge_name": "", "count": 1},
        {"name": "Heat Sink II", "charge_name": "", "count": 1},
        {"name": "Heat Sink II", "charge_name": "", "count": 1},
        {"name": "Damage Control II", "charge_name": "", "count": 1},
        {"name": "Armor EM Hardener II", "charge_name": "", "count": 1},
        {"name": "Armor Thermic Hardener II", "charge_name": "", "count": 1},
        {"name": "Dark Blood Large Armor Repairer", "charge_name": "", "count": 1},

        {"name": "Large Semiconductor Memory Cell I", "charge_name": "", "count": 1},
        {"name": "Large Auxiliary Nano Pump I", "charge_name": "", "count": 1},
        {"name": "Large Auxiliary Nano Pump I", "charge_name": "", "count": 1},

        {"name": "Hammerhead II", "charge_name": "", "count": 5},
        {"name": "Hobgoblin II", "charge_name": "", "count": 5},
    ]
}

"""


class EftParser(object):

    def parse(self, eft_text):
        raise NotImplementedError("Please implement me.")


EXAMPLE_EFT_TEXT = """[Heron]
Warp Core Stabilizer
Warp Core Stabilizer

Relic Analyzer I
Data Analyzer I
1MN Afterburner I
Scan Rangefinding Array I
Scan Rangefinding Array I

Core Probe Launcher I
Prototype Cloaking Device I
Salvager I

Small Gravity Capacitor Upgrade I
Small Gravity Capacitor Upgrade I
"""


def test_parser():
    """This test needs to actually very the result"""

    parser = EftParser()

    result = parser.parse(EXAMPLE_EFT_TEXT)

    print result
