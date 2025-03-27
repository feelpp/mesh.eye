import os
import feelpp.core as fppc
from feelpp.toolboxes.core import *
from feelpp.toolboxes.heat import *

currfiledir = os.path.dirname(os.path.realpath(__file__))
app = fppc.Environment(["myapp"], opts = toolboxes_options("heat"), config = fppc.localRepository(""))


casefile = os.path.join(currfiledir, "test_mesh.cfg")
fppc.Environment.setConfigFile(casefile)
f1 = heat(dim=3, order=1)
f1.init()
f1.printAndSaveInfo()
f1.solve()

f2 = heat(dim=3, order=2)
f2.init()
f2.printAndSaveInfo()
f2.solve()

# usage to see the nDof for P1 and P2 discretizations with the heat toolbox
# python3 test_meshes.py 2>/dev/null | grep nDof