# QGRAF Diagram Drawer
## Dependencies
This code uses [QGRAF](http://cfif.ist.utl.pt/~paulo/qgraf.html) and [tikz-feynman](https://github.com/JP-Ellis/tikz-feynman). It requires Python 3.* to run (the current author can ensure it works under Python 3.7.4, any other version is still untested but, in principle, should work).

## Use

The program *qgraf-xml-drawer* is a Python 3.* program for drawing Feynman diagrams. The code translates [QGRAF](http://cfif.ist.utl.pt/~paulo/qgraf.html) diagrams into a *LuaLaTeX*-compatible description, using [tikz-feynman](https://github.com/JP-Ellis/tikz-feynman).

### QGRAF
The program is provided with a *QGRAF* style file called `xmldraw.sty`, which must be used in order to be able to correctly generate the graphs from the output.  Any set of Feynman rules compatible with *QGRAF* can be handled.

### Graph Generation

For the graphs to be correctly generated and drawn, the particle dictionnary must be appropriate for the model in use, namely the type of line that corresponds to the propagator of each particle must be provided.

The *QGRAF* output file and the file to which the user desires to output the *LuaLaTeX* code can be indicated as the first and second command-line arguments to the program, respectively, in the form `python drawer.py <QGRAF_output_file> <LuaLaTeX_target_file>`, with the default values being adjustable in the code.

## Limitations

The original code handles bundles and tadpoles, which the version here contained does not. For the purposes for which it was developed, these features were not particularly relevant, though they might be added at a later time if such a need arises.

Any other issue that may arise comes from lack of testing, though any and all feedback is appreciated.

## Citing

The original code is citeable using the following DOI:

[![DOI](https://zenodo.org/badge/59492920.svg?maxAge=0)](https://zenodo.org/badge/latestdoi/59492920)

Original author: Nicolas Deutschmann

Current author: Nuno Fernandes
