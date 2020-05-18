from xml.etree.ElementTree import *
from xml.etree.ElementInclude import *
import re
import sys
from propagator import *
from vertex import *
from copy import copy
from extra_translation import *

INPUT="out" #QGRAF output file

graphs=XML(default_loader(INPUT,parse))
diagrams=graphs.find("diagrams")

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


file = open("diagrams.tex","w+")

for diagram in list(diagrams):
    DiagID = diagram.find("id").text
    print("Doing diagram: "+DiagID)
    file.write(DiagID+"~\\feynmandiagram[small, horizontal = in1 to out2, tree layout]{\n")
    NOpropagators=list(diagram.find("propagators"))
    NOvertices=list(diagram.find("vertices"))
    propagators=[]
    for p in NOpropagators:
        propagators.append(propagator(p))
    vertices=[]
    for v in NOvertices:
        vertices.append(Vertex(v))
    bundles = []
    for p in propagators:
        if len(bundles) > 0:
            found = False
            for b in bundles:
                if p.fromto == b[0].fromto:
                    print("adding my propagator to an existing bundle")
                    b.append(p)
                    found = True
                    break
            if not found:
                bundles.append([p])
        else:
            bundles = [[p]]
    for b in bundles:
        if len(b)==1:
            if b[0].vfrom != b[0].vto:
                b[0].texprint(file,pt)
            else: #TADPOLE
                tadfrom = copy(b[0])
                tadto = copy(b[0])
                tadfrom.vto = "tad"+tadfrom.id
                tadto.vfrom = "tad"+tadfrom.id
                shape = "half right"
                tadfrom.texprint(file,pt,shape)
                tadto.texprint(file,pt,shape)
        if len(b)==2:
            shapedict = ["quarter right", "quarter left"]

            b[0].texprint(file,pt,shapedict[0])
            if b[1].vfrom == b[0].vfrom:
                b[1].texprint(file,pt,shapedict[1])
            else:
                b[1].texprint(file,pt,shapedict[0])
        if len(b)==3:
            shapedict = ["quarter right", "quarter left"]
            b[0].texprint(file,pt,shapedict[0])
            if b[1].vfrom == b[0].vfrom:
                b[1].texprint(file,pt,shapedict[1])
            else:
                b[1].texprint(file,pt,shapedict[0])
            b[2].texprint(file,pt)
        if len(b)>4:
            print("I don't know how to deal with this !")
            raise ValueError('Too many propagators in a bundle')

    for v in vertices:
        for i in range(len(v.fields)):
            if re.search('[a-zA-Z]',v.fields[i]):
                if i < len(v.fields)-1:
                    file.write("{} [particle={}] -- [{}] {},\n".format(v.fields[i],extra_translate(v.types[i]),pt[v.types[i]],v.id))
                else:
                    file.write("{} [particle={}] -- [{}] {}\n".format(v.fields[i],extra_translate(v.types[i]),pt[v.types[i]],v.id))
  
#
#    file.write("ext1 -- [opacity = 0] mid,\n") add a comma above !
#    file.write("ext3 -- [opacity = 0] mid\n")
#    file.write("q -- [opacity = 0] q {}\n".format(len(v.fields)))
    file.write("};\n")
