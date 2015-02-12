""" This is the model initializer and controller. Parameters are specified
herein and the progression through the different combinations of 
parameters happens here as well. The final data from the run are gathered
and printed to file.


Written by Jon Atwell
"""


import AC_Products
import AC_ProductRules
import AC_ProductRuleNet
import AC_Cells 
import AC_CellNet
import AC_grapher
import random
import networkx as nx
import sys
import os
import time


def get_step_count(PRODUCT_TYPES):
    """A utility function to determine how long to run the model.
    """

    STEPS = 270000
    
    if PRODUCT_TYPES == 3:
        STEPS = 410000
    elif PRODUCT_TYPES == 4:
        STEPS = 580000
    elif PRODUCT_TYPES == 5:
        STEPS = 770000
    elif PRODUCT_TYPES == 6:
        STEPS = 980000
    elif PRODUCT_TYPES == 7:
        STEPS = 1210000
    elif PRODUCT_TYPES == 8:
        STEPS = 1460000
    elif PRODUCT_TYPES == 9:
        STEPS = 1720000
                         
    return STEPS

node = os.uname()[1]
if "cscs" in node:
     node = node.split(".")[0]


"""The stack of if-then statement below is a hack for me to distribute runs 
onto a cluster that doesn't have a scheduler and  that you don't have access to.
You can just delete it. All that matters is that you define a list of PRODUCT_TYPES
and URN_TYPEs to iterate over.
"""


if node == "draga":
    PRODUCT_TYPES = [2]
    URN_TYPE = ["endo-poor-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="lupa":
    PRODUCT_TYPES = [3]
    URN_TYPE = ["endo-poor-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="sciame":
    PRODUCT_TYPES = [4]
    URN_TYPE = ["endo-poor-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab01":
    PRODUCT_TYPES = [5]
    URN_TYPE = ["endo-poor-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab03":
    PRODUCT_TYPES = [2]
    URN_TYPE = ["endo-rich-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab04":
    PRODUCT_TYPES = [3]
    URN_TYPE = ["endo-rich-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab05":
    PRODUCT_TYPES = [4]
    URN_TYPE = ["endo-rich-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab06":
    PRODUCT_TYPES = [5]
    URN_TYPE = ["endo-rich-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab07":
    PRODUCT_TYPES = [2]
    URN_TYPE = ["fixed-poor-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab08":
    PRODUCT_TYPES = [3]
    URN_TYPE = ["fixed-poor-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab10":
    PRODUCT_TYPES = [4]
    URN_TYPE = ["fixed-poor-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab12":
    PRODUCT_TYPES = [5]
    URN_TYPE = ["fixed-poor-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab13":
    PRODUCT_TYPES = [2]
    URN_TYPE = ["fixed-rich-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab14":
    PRODUCT_TYPES = [3]
    URN_TYPE = ["fixed-rich-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab15":
    PRODUCT_TYPES = [4]
    URN_TYPE = ["fixed-rich-source"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab16":
    PRODUCT_TYPES = [2]
    URN_TYPE = ["fixed-rich-target"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab17":
    PRODUCT_TYPES = [2]
    URN_TYPE = ["fixed-poor-target"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab18":
    PRODUCT_TYPES = [3]
    URN_TYPE = ["fixed-rich-target"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
elif node=="cscs-lab19":
    PRODUCT_TYPES = [3]
    URN_TYPE = ["fixed-poor-target"]#, "endo-rich-source", "fixed-rich-source", "fixed-poor-source", "fixed-rich-target", "fixed-poor-target"]
else:
    print "Node not found"
   
              
CHEM = "ALL"           
INTEL = False            
TOPO = "spatial"     
CELL_COUNT = 100
PRODUCT_COUNT = 200
RULE_COUNT = 200


# The set of for-loops for parameter sweeps (or tests)
for TYPES in PRODUCT_TYPES:
    for URN in URN_TYPE:
        for count_run in range(1):                          
            name =  "-".join([str(TYPES), CHEM, str(INTEL),
                URN, TOPO])
            parts = URN.split("-")
            URN = "-".join(parts[:2])
            REPRO = parts[2]

            print node, "started", name, "#", count_run, "at", time.ctime() 
            
            # as rng to reproduce runs if desired
            seed = random.randint(0,sys.maxint)
            
            RNG = random.Random(seed)
            
            #Setting up the environment including the products
            myurn = AC_Products.Urn(URN, TYPES, RNG,
                PRODUCT_COUNT)

            # Creating all of the rules 
            myrules = AC_ProductRules.create_RuleSet(CHEM,
                TYPES, RULE_COUNT, RNG)

            #Creating a network object for compatible rules
            myRuleNet = AC_ProductRuleNet.ProductRuleNet()
            
            # creating the actual cells
            cells = [AC_Cells.Cell(myurn,myRuleNet, RNG, i+1,
                INTEL, REPRO, TOPO)\
                for i in range(CELL_COUNT)]
            
            #passing out the myrules to cells at random
            for i in range(len(myrules)):
                cell = RNG.choice(cells)
                cell.add_ProductRule(myrules.pop(0))

            STEPS = get_step_count(TYPES)

            # Creating a network of neighbors on torus grid
            mynet = AC_CellNet.CellNet(cells, RNG, STEPS)
           
            #Filling in the actual compatible rule network. 
            for cell in cells:
                for ngh in cell.neighbors:
                    for r1 in cell.product_netrules.values():
                        for r2 in ngh.product_netrules.values():
                            # check of compatibility in funct.
                            myRuleNet.add_edge(r1,r2) 

            
            # This while loop is the core loop of the model.
            while (mynet.master_count < STEPS and
                mynet.last_added_rule + 20000 >
                mynet.master_count):
                mynet.get_random_rule() 
                
            myRuleNet.update_cycle_counts(mynet.master_count)
            
            count_alive = 0
            for cell in mynet.net.nodes():
                if cell.count_rules  > 0:
                    count_alive += 1        
      
            # Quick output of key data for sweep analysis
            try:
                output_file = open(name+".csv", "a+")
            except:
                output_file = open(name+".csv", "w+")

            data =  (str(count_run)+","+ 
                str(myRuleNet.cycle_counts)+","+
                str(myRuleNet.get_plus3cell_complexity())+","+
                str(myRuleNet.get_plus3rule_complexity())+","+
                str(count_alive)+","+str(mynet.last_added_rule)+"\n")
            output_file.write(data)
            output_file.close()
            
            
            # Creating a JSON file to visualize the network
            AC_grapher.output_JSON(mynet,myRuleNet, name 
                +"-"+str(count_run)+ ".html")
            print node, "finished", name, "#", count_run, "at", time.ctime() 



