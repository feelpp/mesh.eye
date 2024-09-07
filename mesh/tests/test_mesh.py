import os
import feelpp.core as fppc
from feelpp.toolboxes.core import *
from feelpp.toolboxes.heat import *

pwd = os.getcwd()
app = fppc.Environment(["myapp"], opts= toolboxes_options("heat"), config=fppc.localRepository(""))


casefile = os.path.join(pwd, "test_mesh.cfg")
fppc.Environment.setConfigFile(casefile)
f1 = heat(dim=3, order=1)
f1.init()
f1.printAndSaveInfo()

f2 = heat(dim=3, order=2)
f2.init()
f2.printAndSaveInfo()

# usage to see the nDof for P1 and P2 discretizations with the heat toolbox
# python3 test_meshes.py 2>/dev/null | grep nDof