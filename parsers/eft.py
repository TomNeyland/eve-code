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

                #remove empty lines
                for lines in eft_lines[1:]:
                        if len(lines) == 0:
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
                print result
    	
def test_parser():
    """This test needs to actually very the result"""

    parser = EftParser()

    example_eft ="""[Apocalypse, Ratting sansha]

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
"""

    result = parser.parse(example_eft)


test_parser()
