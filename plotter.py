import matplotlib.pyplot as plt



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


x = [3,4,5,6,7,8,9]
plt.axis([1,10,-.05,1.1])

PRODUCT_TYPES = [3,4,5,6,7,8,9]
CHEMISTRY = ["ALL"] # "SOLOH"
INTEL_TYPE = [False] # => "selective"
URN_TYPE = ["fixed-rich-target","fixed-poor-target", "fixed-rich-source","fixed-poor-source", "endo-rich-source","endo-poor-source"]
TOPOLOGY = ["spatial"] # "well-mixed"

stack = {}
#graph_type = "Cycles Alive"
#graph_type = "3+ Cycles Alive"
#graph_type = "3+ Rules Alive"
graph_type = "Cell Count"
max = 0
for TYPES in PRODUCT_TYPES:
	for CHEM in CHEMISTRY:
		for INTEL in INTEL_TYPE:
			for URN in URN_TYPE:
				for TOPO in TOPOLOGY:
					mystr = "-".join([str(TYPES), CHEM, str(INTEL), URN, TOPO])
					datafile = open(mystr+".csv","r+")
					vals = []
					three_vals = []
					cells = []
					rules = []
					count_runs = 0.
					
					step_count = get_step_count(TYPES)
					for line in datafile:

						pre = line.replace("{","|").replace("}","|")
						raw = pre.strip().split("|")
						run = int(raw[0].replace(",",""))
						precycles = raw[1].split(",")
						cycles = {}
						for i in precycles:
							try:
								j,k = i.split(":")
								cycles[int(j)] = int(k)
							except:
								cycles = {}

						after = raw[2].split(",")

						if graph_type == "Cycles Alive":
							count_runs += 1
							add_info = "Fraction of 100 runs w/ Hypercycles"			
							if int(after[4]) > step_count*.95:
								if len(cycles.keys()) > 0:
									vals.append(1)
								else:
									vals.append(0)

						elif graph_type == "3+ Cycles Alive":
							count_runs += 1
							add_info = "Fraction of 100 runs w/ 3+ cycles"
							if cycles != {}:
								if len(cycles.keys()) > 1:
									vals.append(1)
								else:
									vals.append(0)
							else:		
								vals.append(0)

						elif graph_type == "3+ Rules Alive":
							count_runs += 1
							add_info = "Fraction of 100 runs w/ 3+ Rules in Cycle"
							if after[2]=='False':
								vals.append(0)
							else:
								vals.append(1)

						elif graph_type == "Cell Count":
							add_info = "Average # cells alive, if alive"
							
							if int(after[4]) > step_count*.95:
								if len(cycles.keys()) > 0:
									a = int(after[3])
									vals.append(a)
									count_runs += 1
									if a > max:
										print "new max", a
										max = a
							plt.axis([1,10,-0.5,max])
					if count_runs == 0:
						count_runs = 1 #because numerator is 0 anyway
							
							

              				try:
              					stack[URN].append(sum(vals)/count_runs)
              				except:
              					stack[URN] = [sum(vals)/count_runs]

print stack

plt.plot(x,stack["fixed-rich-source"], label="source-rich", color="k", marker="s",markeredgecolor="k",ms=8,linestyle="solid", linewidth=2)
plt.plot(x,stack["fixed-poor-source"], label="souce-poor", color="k", marker="^",linestyle="solid",linewidth=2,markeredgecolor="k",ms=8)
plt.plot(x,stack["endo-rich-source"], label="stigmergy-rich", color="r", marker="s",linestyle="solid",linewidth=2,markeredgecolor="r",ms=8)
plt.plot(x,stack["endo-poor-source"], label="stigmergy-poor", color="r", marker="^",linestyle="solid",linewidth=2,markeredgecolor="r",ms=8)
plt.plot(x,stack["fixed-rich-target"], label="target-rich", color="b", marker="s",linestyle="solid",linewidth=2,markeredgecolor="b",ms=8)
plt.plot(x,stack["fixed-poor-target"], label="target-poor", color="b", marker="^",linestyle="solid",linewidth=2,markeredgecolor="b",ms=8)
#plt.plot(x,nonspatial, label="nonspatial", color="g", marker="s",linestyle="solid",linewidth=2,markeredgecolor="g",ms=8)


plt.title("ALL Chem - No Pass Back - " + graph_type)
plt.ylabel(add_info)
plt.xlabel("Types of Products in Chemistry")
legend = plt.legend(bbox_to_anchor=(.01, -0.3, 1., .102), loc=3,ncol=3, mode="expand", borderaxespad=1.)
plt.savefig(graph_type, bbox_extra_artists=(legend,), bbox_inches='tight')
