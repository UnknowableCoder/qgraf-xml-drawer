from xml.etree.ElementTree import *
from xml.etree.ElementInclude import *
import re


def extra_translate(str):
  rep = {"BACKSLASH": "\\", "CARET": "^", "MINUS": "-", "PLUS": "+", "CURLYL": "{", "CURLYR": "}" }
  rep = dict((re.escape(k), v) for k, v in rep.items()) 
  pattern = re.compile("|".join(rep.keys()))
  return "$" + pattern.sub(lambda m: rep[re.escape(m.group(0))], str) + "$"
  #From Andrew Clark at StackOverflow: https://stackoverflow.com/a/6117124

class qgraf_border:
  def __init__(self, label, momentum):
    self.label = label
    self.momentum = momentum
  
class qgraf_line:
  def __init__(self, particle, antiparticle, momentum, sign, previous, next):
    self.particle = particle
    self.antiparticle = antiparticle
    self.momentum = momentum
    self.sign = sign
    self.base = previous
    self.tip = next

class qgraf_info:
  def __init__(self, diagram):
    self.id = int(diagram.find("id").text)
    self.sign = diagram.find("signsym").text[0]
    self.incoming = {}
    self.outgoing = {}
    #Dictionaries for easier access.
    #Might not be the most performant option,
    #but seems to be the simplest.
    for leg in list(diagram.find("legs")):
      if leg.find("status").text == "in":
        self.incoming[int(leg.find("id").text)]  =qgraf_border(leg.find("field").text, leg.find("momentum").text)
      elif leg.find("status").text == "out":
        self.outgoing[int(leg.find("id").text)] = qgraf_border(leg.find("field").text, leg.find("momentum").text)
      else:
        print("Error: invalid leg status \'" + leg.find("status").text + "\' in leg " + leg.find("id").text)
    self.propag = {}
    for prop in list(diagram.find("propagators")):
      self.propag[int(prop.find("begin").text)] = qgraf_line(prop.find("field").text,prop.find("dual_field").text, prop.find("momentum").text, prop.find("sign").text, int(prop.find("begin").text), int(prop.find("end").text))
    self.vertex = {}
    for vert in list(diagram.find("vertices")):
      for n in list(vert.find("fields").text.split(",")):
        self.vertex[int(n)] = int(vert.find("id").text)

  def draw_incoming(self, file, dictionary):
    for k,v in self.incoming.items():
      file.write("\n  in{} [particle={}] -- [ {} ] v{},".format(abs(k),extra_translate(v.label),dictionary[v.label],self.vertex[k]))

  def draw_vertices(self, file, dictionary):
    for k,v in self.vertex.items():
      if k < 0: #incoming or outgoing - handled elsewhere
        continue
      elif k not in self.propag: #is an ending point - will be covered by some other key-value pair
        continue
      else: #is the start of a(n internal) propagator
        p = self.propag[k]
        file.write("\n  v{}  -- [ {} , edge label = {} ] v{},".format(self.vertex[p.tip],
                                                                      dictionary[p.particle],
                                                                      extra_translate(p.particle),
                                                                      v))

  def draw_outgoing(self, file, dictionary):
    for k,v in self.outgoing.items():
      file.write("\n  v{}  -- [ {} ] out{} [particle={}],".format(self.vertex[k],dictionary[v.label],abs(k),extra_translate(v.label)))
  

  def draw(self, file, dictionary):
    if len(self.incoming) > 1:
      file.write("\n" + self.sign + "\\feynmandiagram[small, vertical = in1 to in3 ]{")
    elif len(self.outgoing) > 1:
      file.write("\n" + self.sign + "\\feynmandiagram[small, vertical = out2 to out4 ]{")
    else:
      file.write("\n" + self.sign + "\\feynmandiagram[small, horizontal = in1 to out2 ]{")
    #This ensures in and out are aligned (hopefully)
    #No worries because there should be at least one incoming and one outcoming particle
    self.draw_incoming(file, dictionary)
    self.draw_vertices(file, dictionary)
    self.draw_outgoing(file, dictionary)
    file.write("\n};")
      
        
      
    