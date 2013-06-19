"""A parser for EFT blocks."""

class EftParser(object):

        def parse(self, eft):
                eft_lines = eft.splitlines()
                
                #get first line and extract ship name and fit name
                to_parse = eft_lines[0]
                to_parse = to_parse.replace("[","")
                to_parse = to_parse.replace("]","")
                to_parse = to_parse.split(",")
                shipname = to_parse[0]
                fitname = to_parse[1]
                fitname = fitname[1:]

                #create empty lists to contain item names, charge names and counts
                dict_list = []

                #remove empty lines and empty slots
                for lines in eft_lines[1:]:
                        if len(lines) == 0:
                                eft_lines.remove(lines)

                        if lines.find("slot") > -1:
                                eft_lines.remove(lines)

                for lines in eft_lines[1:]:
                        #search for drones
                        if (lines[len(lines)-1].isdigit()) & (lines[len(lines)-2]=="x") :
                                dict_list.append({"name": lines[0:len(lines)-3], "charge_name": "", "count": int(lines[len(lines)-1])})
                                break
                        
                        #normal mods
                        if lines.find(",") < 0:
                                dict_list.append({"name": lines, "charge_name": "", "count": 1})
   
                        #weapons with charges
                        else:
                                posdel = lines.find(",")
                                dict_list.append({"name": lines[0:posdel], "charge_name": lines[posdel+2:], "count": 1})


                result = {"ship_type": shipname, "fit_name": fitname, "items": dict_list}
                return result
        	
def test_parser():

    parser = EftParser()

    example_eft ="""[Vindicator, Shieldicator]
Tracking Enhancer II
Tracking Enhancer II
True Sansha Capacitor Power Relay
Federation Navy Magnetic Field Stabilizer
Federation Navy Magnetic Field Stabilizer
Federation Navy Magnetic Field Stabilizer
Federation Navy Magnetic Field Stabilizer

Stasis Webifier II
100MN Afterburner II
Medium Shield Booster II
Sensor Booster II, Scan Resolution Script
Kinetic Deflection Field II

Neutron Blaster Cannon II, Void L
Neutron Blaster Cannon II, Void L
Neutron Blaster Cannon II, Void L
Neutron Blaster Cannon II, Void L
Neutron Blaster Cannon II, Void L
Neutron Blaster Cannon II, Void L
Neutron Blaster Cannon II, Void L
[empty high slot]

Large Hybrid Burst Aerator II
Large Anti-Thermal Screen Reinforcer I
[empty rig slot]


Hammerhead II x5
Warrior II x5
Vespa EC-600 x5
"""

    result = parser.parse(example_eft)
    print result
