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
parser.add_argument("--add-syringe", help="add the syringe", default=True, type=bool)
parser.add_argument("--mesh", help="activate mesh generation", action="store_true")
args = parser.parse_args()

hsize_eye = args.hsize_eye
hsize_lamina = args.hsize_lamina

add_syringe = args.add_syringe
if add_syringe:
    print("Syringe added")



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
[Cornea0, AqueousHumor0, Iris0, Lens0, VitreousHumor0, Sclera0, Choroid0, Retina0, Lamina0, OpticNerve0] = geompy.ExtractShapes(Eye, geompy.ShapeType["SOLID"], True)

if add_syringe:
    Cylinder_1 = geompy.MakeCylinder(O, OY, 0.127, 0.05)
    syringe = geompy.MakeTranslation(Cylinder_1, -11, -2.5, 0)

    geompy.addToStudy( syringe, 'Syringe' )

    AqueousHumor_Cut = geompy.MakeCutList(AqueousHumor0, [syringe], True)
    New_Eye = geompy.MakePartition([Cornea0, AqueousHumor_Cut, Iris0, Lens0, VitreousHumor0, Sclera0, Choroid0, Retina0, Lamina0, OpticNerve0, syringe], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0, 0)

    [Cornea, Syringe, AqueousHumor, Iris, Lens, VitreousHumor, Sclera, Choroid, Retina, Lamina, OpticNerve] = geompy.ExtractShapes(New_Eye, geompy.ShapeType["SOLID"], True)

else:
    New_Eye = geompy.MakePartition([Cornea0, AqueousHumor0, Iris0, Lens0, VitreousHumor0, Sclera0, Choroid0, Retina0, Lamina0, OpticNerve0], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0, 0)

    [Cornea, AqueousHumor, Iris, Lens, VitreousHumor, Sclera, Choroid, Retina, Lamina, OpticNerve] = geompy.ExtractShapes(New_Eye, geompy.ShapeType["SOLID"], True)

geompy.addToStudy( New_Eye, 'Human Eye' )
geompy.addToStudyInFather( New_Eye, Cornea, 'Cornea' )
geompy.addToStudyInFather( New_Eye, AqueousHumor, 'AqueousHumor' )
geompy.addToStudyInFather( New_Eye, Iris, 'Iris' )
geompy.addToStudyInFather( New_Eye, Lens, 'Lens' )
geompy.addToStudyInFather( New_Eye, VitreousHumor, 'VitreousHumor' )
geompy.addToStudyInFather( New_Eye, Sclera, 'Sclera' )
geompy.addToStudyInFather( New_Eye, Choroid, 'Choroid' )
geompy.addToStudyInFather( New_Eye, Retina, 'Retina' )
geompy.addToStudyInFather( New_Eye, Lamina, 'Lamina' )
geompy.addToStudyInFather( New_Eye, OpticNerve, 'OpticNerve' )
if add_syringe:
    geompy.addToStudyInFather( New_Eye, Syringe, 'Syringe' )
    Syringe.SetColor(SALOMEDS.Color(0.525490196,0.576470588,0.694117647))


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



if add_syringe:
    Solids = [Cornea, AqueousHumor, Iris, Lens, VitreousHumor, Sclera, Choroid, Retina, Lamina, OpticNerve, Syringe]
else:
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

    elif "Syringe" in Name1 and add_syringe:
        FSyr = geompy.ExtractShapes(solid1, geompy.ShapeType["FACE"], True)

        BC_Inj = geompy.CreateGroup(solid1, geompy.ShapeType["FACE"], "BC_Injection")
        geompy.UnionList(BC_Inj, [FSyr[2]])
        Others.append(BC_Inj)

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

EyeMesh = smesh.Mesh(New_Eye)
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
if add_syringe:
    Syringe_mesh = EyeMesh.GroupOnGeom(Syringe, 'Syringe', SMESH.VOLUME)


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


####################################
# Second mesh

if add_syringe:

    Eye_AH = geompy.MakePartition([AqueousHumor, Syringe], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0, 0)
    [SyringeAH, AqueousHumorAH] = geompy.ExtractShapes(Eye_AH, geompy.ShapeType["SOLID"], True)

    Faces_AqueousHumorAH = geompy.ExtractShapes(AqueousHumorAH, geompy.ShapeType["FACE"], True)
    for i, face, in enumerate(Faces_AqueousHumorAH):
        geompy.addToStudy(face, f"Face_AqueousHumorAH_{i}")
    Faces_SyringeAH = geompy.ExtractShapes(SyringeAH, geompy.ShapeType["FACE"], True)
    for i, face, in enumerate(Faces_SyringeAH):
        geompy.addToStudy(face, f"Face_SyringeAH_{i}")

    BC_Injection_Faces = [Faces_SyringeAH[2]]
    AqueousHumor_In_Faces = [Faces_AqueousHumorAH[20], Faces_AqueousHumorAH[54]]
    AqueousHumor_Cornea_Faces = [Faces_AqueousHumorAH[3], Faces_AqueousHumorAH[4]]
    AqueousHumor_Iris_Faces = [
        Faces_AqueousHumorAH[7], Faces_AqueousHumorAH[12], Faces_AqueousHumorAH[14], Faces_AqueousHumorAH[48],
        Faces_AqueousHumorAH[5], Faces_AqueousHumorAH[6], Faces_AqueousHumorAH[8], Faces_AqueousHumorAH[9],
        Faces_AqueousHumorAH[10], Faces_AqueousHumorAH[29], Faces_AqueousHumorAH[17], Faces_AqueousHumorAH[18],
        Faces_AqueousHumorAH[19], Faces_AqueousHumorAH[21], Faces_AqueousHumorAH[22], Faces_AqueousHumorAH[23],
        Faces_AqueousHumorAH[24], Faces_AqueousHumorAH[32], Faces_AqueousHumorAH[33], Faces_AqueousHumorAH[37],
        Faces_AqueousHumorAH[40], Faces_AqueousHumorAH[44], Faces_AqueousHumorAH[45], Faces_AqueousHumorAH[49],
        Faces_AqueousHumorAH[50], Faces_AqueousHumorAH[55], Faces_AqueousHumorAH[58], Faces_AqueousHumorAH[59],
        Faces_AqueousHumorAH[64], Faces_AqueousHumorAH[65], Faces_AqueousHumorAH[66], Faces_AqueousHumorAH[67]
    ]
    AqueousHumor_Lens_Faces = [
        Faces_AqueousHumorAH[11], Faces_AqueousHumorAH[13], Faces_AqueousHumorAH[36], Faces_AqueousHumorAH[38],
        Faces_AqueousHumorAH[26], Faces_AqueousHumorAH[27], Faces_AqueousHumorAH[28], Faces_AqueousHumorAH[30],
        Faces_AqueousHumorAH[31], Faces_AqueousHumorAH[34], Faces_AqueousHumorAH[35], Faces_AqueousHumorAH[39],
        Faces_AqueousHumorAH[41], Faces_AqueousHumorAH[42], Faces_AqueousHumorAH[43], Faces_AqueousHumorAH[46],
        Faces_AqueousHumorAH[47], Faces_AqueousHumorAH[52], Faces_AqueousHumorAH[53], Faces_AqueousHumorAH[56],
        Faces_AqueousHumorAH[57], Faces_AqueousHumorAH[60], Faces_AqueousHumorAH[61], Faces_AqueousHumorAH[62], Faces_AqueousHumorAH[63]
    ]
    AqueousHumor_Syringe_Faces = [Faces_AqueousHumorAH[0], Faces_AqueousHumorAH[1]]
    AqueousHumor_VitreousHumor_Faces = [Faces_AqueousHumorAH[51]]
    AqueousHumor_Sclera_Faces = [Faces_AqueousHumorAH[15], Faces_AqueousHumorAH[16]]


    Eye_Mesh_AH = smesh.Mesh(Eye_AH)
    NETGEN_1D_2D_3D_AH = Eye_Mesh_AH.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
    smesh.SetName(Eye_Mesh_AH.GetMesh(), "Eye_Mesh_AH")

    # Set markers
    Vitreous_humor_1_AH = Eye_Mesh_AH.GroupOnGeom(AqueousHumorAH, 'AqueousHumor', SMESH.VOLUME)
    Syringe_1_AH = Eye_Mesh_AH.GroupOnGeom(SyringeAH, 'Syringe', SMESH.VOLUME)
    Done = []
    Names = ["AqueousHumor_In", "AqueousHumor_Cornea", "AqueousHumor_Iris", "AqueousHumor_Lens", "AqueousHumor_Syringe", "AqueousHumor_VitreousHumor", "AqueousHumor_Sclera", "BC_Injection"]

    for name, faces in zip(Names, [AqueousHumor_In_Faces, AqueousHumor_Cornea_Faces, AqueousHumor_Iris_Faces, AqueousHumor_Lens_Faces, AqueousHumor_Syringe_Faces, AqueousHumor_VitreousHumor_Faces, AqueousHumor_Sclera_Faces, BC_Injection_Faces]):
        if name not in Done:
            BC_Group = geompy.CreateGroup(Eye_AH, geompy.ShapeType["FACE"], name)
            geompy.UnionList(BC_Group, faces)
            BC_Group_Mesh = Eye_Mesh_AH.GroupOnGeom(BC_Group, name, SMESH.FACE)
            print("Other inserted :", name)
            Done.append(name)

    NETGEN_3D_Parameters_AH = NETGEN_1D_2D_3D_AH.Parameters()
    NETGEN_3D_Parameters_AH.SetMaxSize( 0.1 )

    isDone = Eye_Mesh_AH.Compute()
    assert isDone, "Failed to compute mesh"

    Eye_Mesh_AH.ExportMED( "mesh/Eye_Mesh3D_AH.med", 0, SMESH.MED_V2_2, 1, None, 1 )