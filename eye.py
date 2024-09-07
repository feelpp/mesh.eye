# -*- coding: utf-8 -*-

###
### This file was generated automatically by SALOME v7.7.1 with dump python functionality
### is was manually updated to run with SALOME v9.7.0

### to run the script:
###    path/to//salome [-t] eye.py [args:[--distance=],[--width=],[--hole=],[--shift=],[--mesh]]
###    salome -t shell eye.py args:--mesh

### output:
###   mesh in med 3.1.0 format
###   to get a msh file: gmsh -3 -bin file.med
###   NB: gmsh has to be compiled against med 3.1.0 or later...

import sys
import salome
import time

print("")
print("*******************")
print("Geometry of the eye")
print("*******************")


exec_time = time.time()

salome.salome_init()
theStudy = salome.myStudy

import salome_version
print("This code is supposed to run with salome version 9.12.0")
print("Current Salome Version is :", salome_version.getVersion(), '\n')


# Lamina params
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--hsize_eye", help="max size of the h of the computational mesh for the eye [default=1.0]", type=float, default=1.0)
parser.add_argument("--hsize_lamina", help="max size of the h of the computational mesh for the lamina [default=0.05]", type=float, default=0.05)
parser.add_argument("--mesh", help="activate mesh generation", action="store_true")
args = parser.parse_args()

hsize_eye = args.hsize_eye
hsize_lamina = args.hsize_lamina



###
### GEOM component
###


geom_time = time.time()
exec_time = time.time()

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )


Eye = geompy.ImportSTEP("Eye.step", True)
[Cornea, AqueousHumor, Iris, Lens, VitreousHumor, Sclera, Choroid, Retina, Lamina, OpticNerve] = geompy.ExtractShapes(Eye, geompy.ShapeType["SOLID"], True)

geompy.addToStudy( Eye, 'Human Eye' )
geompy.addToStudyInFather( Eye, Cornea, 'Cornea' )
geompy.addToStudyInFather( Eye, AqueousHumor, 'AqueousHumor' )
geompy.addToStudyInFather( Eye, Iris, 'Iris' )
geompy.addToStudyInFather( Eye, Lens, 'Lens' )
geompy.addToStudyInFather( Eye, VitreousHumor, 'VitreousHumor' )
geompy.addToStudyInFather( Eye, Sclera, 'Sclera' )
geompy.addToStudyInFather( Eye, Choroid, 'Choroid' )
geompy.addToStudyInFather( Eye, Retina, 'Retina' )
geompy.addToStudyInFather( Eye, Lamina, 'Lamina' )
geompy.addToStudyInFather( Eye, OpticNerve, 'OpticNerve' )


AqueousHumor.SetColor(SALOMEDS.Color(0.5019,0.0941,0.0941))
Choroid.SetColor(SALOMEDS.Color(1,0.0784,0.5764))
Cornea.SetColor(SALOMEDS.Color(1,1,0))
Iris.SetColor(SALOMEDS.Color(0.1843,0.4588,1))
Lamina.SetColor(SALOMEDS.Color(0,1,0))
Lens.SetColor(SALOMEDS.Color(0,0.666667,0))
OpticNerve.SetColor(SALOMEDS.Color(0.360784,0.207843,0.4))
Retina.SetColor(SALOMEDS.Color(0,0,0))
Sclera.SetColor(SALOMEDS.Color(1,1,1))
VitreousHumor.SetColor(SALOMEDS.Color(1,0.6470,0))

Solids = [Cornea, AqueousHumor, Iris, Lens, VitreousHumor, Sclera, Choroid, Retina, Lamina, OpticNerve]
Solids = sorted(Solids, key=lambda solid: solid.GetName() )

print("\nSolids = [", end="")
for s in Solids[:-1]:
    print(f"{s.GetName()},", end=" ")
print(f"{Solids[-1].GetName()}]\n")


Interfaces = []
Others = []

Interface_ = {}

# should create Interface by extracting Shells and MakeCommon(...)
print("\nCreate interfaces between tissus")
for i, solid1 in enumerate(Solids):
    Interfaces_solid1 = []
    Name1 = solid1.GetName()
    checksum = 0
    if not ("Lamina" in Name1):
        print(Name1)
        for j in range(0, len(Solids)):
            if i != j:
                solid2 = Solids[j]
                Name2 = solid2.GetName()
                faces = geompy.GetSharedShapesMulti([solid1, solid2], geompy.ShapeType["FACE"], False)
                if len(faces) > 0:
                    print("    Interface for %s / %s: %d"%(Name1, Name2, len(faces) ))
                    checksum += len(faces)
                    objName = Name2 + "_" + Name1 if Name1 > Name2 else Name1 + "_" + Name2
                    Interface_[(Name1, Name2)] = geompy.CreateGroup(solid1, geompy.ShapeType["FACE"], objName)
                    geompy.UnionList(Interface_[(Name1, Name2)], faces)
                    Interfaces_solid1.append(Interface_[(Name1, Name2)])

  # append Interface_solid1 to Interfaces
    Interfaces.append(Interfaces_solid1)
    print("  Build Interfaces done, total number of interfaces : %d"%checksum)
print("Done")




# loop over solids to build for each solid a list of "free groups"
print("Get free groups")
for i,solid1 in enumerate(Solids):
    Name1 = solid1.GetName()
    print("\t"+Name1+":", end=' ')

    if "Cornea" in Name1:
        FCor = geompy.ExtractShapes(solid1, geompy.ShapeType["FACE"], True)
        optic_faces =  geompy.CreateGroup(solid1, geompy.ShapeType["FACE"], "BC_%s"%(Name1) )
        geompy.UnionList(optic_faces, [FCor[0], FCor[1]])
        Others.append(optic_faces)

    elif "OpticNerve" in Name1:
        FOpt = geompy.ExtractShapes(solid1, geompy.ShapeType["FACE"], True)
        optic_faces =  geompy.CreateGroup(solid1, geompy.ShapeType["FACE"], "BC_%s"%(Name1) )
        geompy.UnionList(optic_faces, [FOpt[5], FOpt[6], FOpt[7]])
        Others.append(optic_faces)

    elif "Sclera" in Name1:
        FScl = geompy.ExtractShapes(solid1, geompy.ShapeType["FACE"], True)
        optic_faces =  geompy.CreateGroup(solid1, geompy.ShapeType["FACE"], "BC_%s"%(Name1) )
        geompy.UnionList(optic_faces, [FScl[6],FScl[7],FScl[12],FScl[13],FScl[19]])
        Others.append(optic_faces)

    elif "Lamina" in Name1:
        [Hole, In, Lateral1, Lateral0, Out] = geompy.ExtractShapes(solid1, geompy.ShapeType["FACE"], True)

        Lateral = geompy.CreateGroup(Lamina, geompy.ShapeType["FACE"], "Lateral")
        geompy.UnionList(Lateral, [Lateral0, Lateral1])
        In_ = geompy.CreateGroup(Lamina, geompy.ShapeType["FACE"], "In")
        geompy.UnionList(In_, [In])
        Hole_ = geompy.CreateGroup(Lamina, geompy.ShapeType["FACE"], "Hole")
        geompy.UnionList(Hole_, [Hole])
        Out_ = geompy.CreateGroup(Lamina, geompy.ShapeType["FACE"], "Out")
        geompy.UnionList(Out_, [Out])

    else:
        print("Nothing to do")

print("Done\n")



########

###
### SMESH component
###

geom_time = time.time() - geom_time
mesh_time = time.time()


import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()

EyeMesh = smesh.Mesh(Eye)
EyeMesh.SetName("Eye_Mesh")
NETGEN_1D_2D_3D = EyeMesh.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
print("Attach Mesh to Eye_Mesh")

# Set markers
Retina_mesh = EyeMesh.GroupOnGeom(Retina,'Retina',SMESH.VOLUME)
Choroid_mesh = EyeMesh.GroupOnGeom(Choroid,'Choroid',SMESH.VOLUME)
Vitreous_humor_mesh = EyeMesh.GroupOnGeom(VitreousHumor,'VitreousHumor',SMESH.VOLUME)
Lens_mesh = EyeMesh.GroupOnGeom(Lens,'Lens',SMESH.VOLUME)
Iris_mesh = EyeMesh.GroupOnGeom(Iris,'Iris',SMESH.VOLUME)
AqueousHumor_mesh = EyeMesh.GroupOnGeom(AqueousHumor,'AqueousHumor',SMESH.VOLUME)
Lamina_mesh = EyeMesh.GroupOnGeom(Lamina,'Lamina',SMESH.VOLUME)
OpticNerve_mesh = EyeMesh.GroupOnGeom(OpticNerve,'OpticNerve',SMESH.VOLUME)
Cornea_mesh = EyeMesh.GroupOnGeom(Cornea,'Cornea',SMESH.VOLUME)
Sclera_mesh = EyeMesh.GroupOnGeom(Sclera,'Sclera',SMESH.VOLUME)


print("Create Groups from Geometry")

# try:
Out_1 = EyeMesh.GroupOnGeom(Out,'Out',SMESH.FACE)
Out_1.SetColor( SALOMEDS.Color( 1, 0.666667, 0 ))
Out_1.SetName( 'Lamina_Out' )
Hole_1 = EyeMesh.GroupOnGeom(Hole,'Hole',SMESH.FACE)
Hole_1.SetColor( SALOMEDS.Color( 1, 0.666667, 0 ))
Hole_1.SetName( 'Lamina_Hole' )
In_1 = EyeMesh.GroupOnGeom(In,'In',SMESH.FACE)
In_1.SetColor( SALOMEDS.Color( 1, 0.666667, 0 ))
In_1.SetName( 'Lamina_In' )
Lateral_1 = EyeMesh.GroupOnGeom(Lateral,'Lateral',SMESH.FACE)
Lateral_1.SetColor( SALOMEDS.Color( 1, 0.666667, 0 ))
Lateral_1.SetName( 'Lamina_Lateral' )
print("Set BC Groups on Lamina")


Done = []
for item in Others:
    Name = item.GetName()
    if Name not in Done:
        Done.append(Name)
        print("Other inserted :", Name)
        BC_Group_Mesh = EyeMesh.GroupOnGeom(item,item.GetName(),SMESH.FACE)
        BC_Group_Mesh.SetColor( SALOMEDS.Color( 1, 0.666667, 0.333333 ))

Done = ["Lamina"]
for interface in Interfaces:
    for item in interface:
        Name = item.GetName()
        if not Name in Done:
            if "Lamina" not in Name:
                Done.append(Name)
                print("%s added"%Name)
                BC_Group_Mesh = EyeMesh.GroupOnGeom(item,Name,SMESH.FACE)
                BC_Group_Mesh.SetColor( SALOMEDS.Color( 1, 0.666667, 0.333333 ))


try:
    isDone = EyeMesh.Compute()

    EyeMesh.ExportMED( "mesh/Eye_Mesh3D.med", 0, SMESH.MED_V2_2, 1, None ,1 )

    print(EyeMesh.Dump())
    print('Mesh built successfully')

except Exception as e:
    print("Failed to create Mesh :")
    print(e)
    sys.exit(1)


mesh_time = time.time() - mesh_time
exec_time = time.time() - exec_time

print("")
print("***********************************")
print("Geometry assembly time =", geom_time)
print("Mesh generation time ="  , mesh_time)
print("Total execution time ="  , exec_time)
print("***********************************")

if salome.sg.hasDesktop():
    salome.sg.updateObjBrowser()
