import sys
from qgraf_interpreter import *



#Particle dictionnary. Adapt this to your model
pt = {"H": "scalar",
      "eCARETMINUS": "fermion",
      "eCARETPLUS": "anti fermion",
      "BACKSLASHmuCARETMINUS": "fermion",
      "BACKSLASHmuCARETPLUS": "anti fermion",
      "BACKSLASHtauCARETMINUS": "fermion",
      "BACKSLASHtauCARETPLUS": "anti fermion",
      "BACKSLASHnu_e": "fermion",
      "BACKSLASHoverlineCURLYLBACKSLASHnu_eCURLYR": "anti fermion",
      "BACKSLASHnu_BACKSLASHmu": "fermion",
      "BACKSLASHoverlineCURLYLBACKSLASHnu_BACKSLASHmuCURLYR": "anti fermion",
      "BACKSLASHnu_BACKSLASHtau": "fermion",
      "BACKSLASHoverlineCURLYLBACKSLASHnu_BACKSLASHtauCURLYR": "antifermion",
      "u": "fermion",
      "BACKSLASHoverlineCURLYLuCURLYR": "anti fermion",
      "c": "fermion",
      "BACKSLASHoverlineCURLYLcCURLYR": "anti fermion",
      "t": "fermion",
      "BACKSLASHoverlineCURLYLtCURLYR": "anti fermion",
      "d": "fermion",
      "BACKSLASHoverlineCURLYLdCURLYR": "anti fermion",
      "s": "fermion",
      "BACKSLASHoverlineCURLYLsCURLYR": "anti fermion",
      "b": "fermion",
      "BACKSLASHoverlineCURLYLbCURLYR": "anti fermion",
      "BACKSLASHgamma": "photon",
      "WCARETMINUS": "photon",
      "WCARETPLUS": "photon",
      "Z": "photon",
      "g": "gluon"}



input_file = "out" #QGRAF output file
if len(sys.argv) > 1:
    input_file = sys.argv[1]

output_file = "diagrams.tex"
if len(sys.argv) > 2:
    output_file = sys.argv[2]



graphs=XML(default_loader(input_file,parse))
diagrams=graphs.find("diagrams")


file = open(output_file,"w+")

for diagram in list(diagrams):
    diag_info = qgraf_info(diagram)
    print("Drawing diagram " + str(diag_info.id))
    diag_info.draw(file, pt)
