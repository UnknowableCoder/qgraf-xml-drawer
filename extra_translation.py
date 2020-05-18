import re

#This allows the use of LaTeX-like syntax in qgraf's field names,
#using BACKSLASH for \, CARET for ^, MINUS for -, PLUS for +, CURLYL for { and CURLYR for }.

def extra_translate(str):
  rep = {"BACKSLASH": "\\", "CARET": "^", "MINUS": "-", "PLUS": "+", "CURLYL": "{", "CURLYR": "}" }
  rep = dict((re.escape(k), v) for k, v in rep.items()) 
  pattern = re.compile("|".join(rep.keys()))
  return "$" + pattern.sub(lambda m: rep[re.escape(m.group(0))], str) + "$"
  #From Andrew Clark at StackOverflow: https://stackoverflow.com/a/6117124
