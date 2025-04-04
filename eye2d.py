#!/usr/bin/env python

import sys
import salome
import time

salome.salome_init()

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS



import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--hsize_max", help="max size of the h of the computational mesh for the eye [default=1.0]", type=float, default=1.0)
parser.add_argument("--hsize_min", help="max size of the h of the computational mesh for the lamina [default=0.05]", type=float, default=0.05)
parser.add_argument("--add-syringe", default=True, type=bool, help="add the syringe")
parser.add_argument("--mesh", help="activate mesh generation", action="store_true")
args = parser.parse_args()

add_syringe = args.add_syringe
if add_syringe:
    print("Syringe is added")


###
### GEOM component
###

geom_time = time.time()
exec_time = time.time()



geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Human_Eye = geompy.ImportSTEP("Eye.step", True, False)


CutPlane = geompy.MakePlane(O, OZ, 50)
PlaneEye = geompy.MakePartition([Human_Eye], [CutPlane], [], [], geompy.ShapeType["FACE"], 0, [], 0)

ExtractedFaces = geompy.ExtractShapes(PlaneEye, geompy.ShapeType["FACE"], True)

CorneaPlan = ExtractedFaces[2]
AqueousHumorPlan = ExtractedFaces[5]
Iris2Plan = ExtractedFaces[46]
Iris1Plan = ExtractedFaces[214]
LensPlan = ExtractedFaces[201]
Sclera2Plan = ExtractedFaces[296]
Sclera1Plan = ExtractedFaces[291]
Choroid2Plan = ExtractedFaces[304]
Choroid1Plan = ExtractedFaces[293]
VitreousHumorPlan = ExtractedFaces[292]
RetinaPlan = ExtractedFaces[303]
Lamina2Plan = ExtractedFaces[309]
Lamina1Plan = ExtractedFaces[323]
OpticNervePlan = ExtractedFaces[328]

if add_syringe:
    Bloc = geompy.MakeFaceHW(0.127, 0.05, 1)
    syringe = geompy.MakeTranslation(Bloc, -10.5, -2.5, 0)

    geompy.addToStudy(syringe, 'Syringe' )

    AqueousHumor_Cut = geompy.MakeCutList(AqueousHumorPlan, [syringe], True)

    EyePlan = geompy.MakePartition([CorneaPlan, Iris1Plan, Iris2Plan, LensPlan, AqueousHumor_Cut, syringe, Choroid1Plan, Choroid2Plan, RetinaPlan, VitreousHumorPlan, Lamina1Plan, Lamina2Plan, OpticNervePlan, Sclera1Plan, Sclera2Plan], [], [], [], geompy.ShapeType["FACE"], 0, [], 0)

    [Cornea, Syringe, AqueousHumor, Iris2, Lens, Iris1, Sclera2, VitreousHumor, Choroid2, Sclera1, Retina, Choroid1, Lamina2, Lamina1, OpticNerve] = geompy.ExtractShapes(EyePlan, geompy.ShapeType["FACE"], True)


else:

    EyePlan = geompy.MakePartition([CorneaPlan, Iris1Plan, Iris2Plan, LensPlan, AqueousHumorPlan, Choroid1Plan, Choroid2Plan, RetinaPlan, VitreousHumorPlan, Lamina1Plan, Lamina2Plan, OpticNervePlan, Sclera1Plan, Sclera2Plan], [], [], [], geompy.ShapeType["FACE"], 0, [], 0)
    [Cornea, AqueousHumor, Iris2, Lens, Iris1, Sclera2, VitreousHumor, Choroid2, Sclera1, Retina, Choroid1, Lamina2, Lamina1, OpticNerve] = geompy.ExtractShapes(EyePlan, geompy.ShapeType["FACE"], True)


Group_Iris = geompy.CreateGroup(EyePlan, geompy.ShapeType["FACE"])
geompy.UnionList(Group_Iris, [Iris1, Iris2])
Group_Sclera = geompy.CreateGroup(EyePlan, geompy.ShapeType["FACE"])
geompy.UnionList(Group_Sclera, [Sclera1, Sclera2])
Group_Choroid = geompy.CreateGroup(EyePlan, geompy.ShapeType["FACE"])
geompy.UnionList(Group_Choroid, [Choroid1, Choroid2])
Group_Lamina = geompy.CreateGroup(EyePlan, geompy.ShapeType["FACE"])
geompy.UnionList(Group_Lamina, [Lamina1, Lamina2])



VitreousHumor.SetColor(SALOMEDS.Color(1,0.647,0))
Retina.SetColor(SALOMEDS.Color(0,0,0))
OpticNerve.SetColor(SALOMEDS.Color(0,1,1))
Group_Iris.SetColor(SALOMEDS.Color(0.1843,0.4588,1))
Group_Sclera.SetColor(SALOMEDS.Color(1,1,1))
Group_Choroid.SetColor(SALOMEDS.Color(1,0.0784,0.5764))
Group_Lamina.SetColor(SALOMEDS.Color(0,1,0))
Cornea.SetColor(SALOMEDS.Color(1,1,0))
AqueousHumor.SetColor(SALOMEDS.Color(0.5019,0.0941,0.0941))
if add_syringe:
    Syringe.SetColor(SALOMEDS.Color(0.5019,0.0941,0.0941))
Lens.SetColor(SALOMEDS.Color(0,0.666667,0))


geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( EyePlan, 'EyePlan' )
geompy.addToStudyInFather( EyePlan, Cornea, 'Cornea' )
geompy.addToStudyInFather( EyePlan, AqueousHumor, 'AqueousHumor' )
if add_syringe:
    geompy.addToStudyInFather( EyePlan, Syringe, 'Syringe' )
geompy.addToStudyInFather( EyePlan, Lens, 'Lens' )
geompy.addToStudyInFather( EyePlan, VitreousHumor, 'VitreousHumor' )
geompy.addToStudyInFather( EyePlan, Retina, 'Retina' )
geompy.addToStudyInFather( EyePlan, OpticNerve, 'OpticNerve' )
geompy.addToStudyInFather( EyePlan, Group_Iris, 'Iris' )
geompy.addToStudyInFather( EyePlan, Group_Sclera, 'Sclera' )
geompy.addToStudyInFather( EyePlan, Group_Choroid, 'Choroid' )
geompy.addToStudyInFather( EyePlan, Group_Lamina, 'Lamina' )



Faces = [Cornea, AqueousHumor, Syringe, Group_Iris, Lens, VitreousHumor, Group_Sclera, Group_Choroid, Retina, Group_Lamina, OpticNerve]
Faces = sorted(Faces, key=lambda solid:solid.GetName() )

for f in Faces:
    l = geompy.ExtractShapes(f, geompy.ShapeType["EDGE"], True)
    print(f.GetName(), len(l))


Interfaces = []
Interface_dict = {}
Others_interfaces = []

print('\nCreate interface between faces')
for i, face in enumerate(Faces):
    Interfaces_face1 = []
    Name1 = face.GetName()
    checksum = 0

    if "Lamina" not in Name1:

        for j in range(len(Faces)):
            if i != j:
                otherface = Faces[j]
                Name2 = otherface.GetName()
                # if "Lamina" not in Name2:

                wires = geompy.GetSharedShapesMulti( [face, otherface], geompy.ShapeType["EDGE"], False )
                d = len(wires)
                if d > 0:
                    print(f"    Interface for {Name1} / {Name2} : {d}")

                    if (Name1 == "AqueousHumor" and Name2 == "Iris") or (Name2 == "AqueousHumor" and Name1 == "Iris"):

                        assert len(wires) == 14
                        wires = [wires[0]] + wires[2:12] + [wires[13]]
                        print("    AqueousHumor/Iris : ", len(wires))

                    checksum += len(wires)


                    interfaceName = f"{Name2}_{Name1}" if Name1 > Name2 else f"{Name1}_{Name2}"
                    Interface_dict[(Name1, Name2)] = geompy.CreateGroup(face, geompy.ShapeType["EDGE"], interfaceName)
                    geompy.UnionList(Interface_dict[(Name1, Name2)], wires)
                    Interfaces_face1.append(Interface_dict[(Name1, Name2)])

        Interfaces.append(Interfaces_face1)
        print(f"  Interfaces for {Name1} done, with {checksum} interfaces")
print("Done")


# loop over faces to build for each solid a list of "free groups"
print("Get free groups")

Others = {
    "Cornea" : [0, 1],
    "OpticNerve" : [7, 8, 9],
    "Sclera" : [5, 7, 10, 12, 15, 16, 24, 25],
    "Pia" : [2, 6, 5, 7, 8],
    # "AqueousHumor" : [18, 27],
}

for i, face in enumerate(Faces):
    Name = face.GetName()
    print(f"    {Name} :", end=" ")

    if Name in Others.keys():
        Edges = geompy.ExtractShapes(face, geompy.ShapeType["EDGE"], True)
        external_edges = geompy.CreateGroup(face, geompy.ShapeType["EDGE"], f"BC_{Name}")
        geompy.UnionList(external_edges, [Edges[i] for i in Others[Name]])
        Others_interfaces.append(external_edges)

    if Name in "Lamina":
        dict_Lamina = {
            "Hole" : [2, 4],
            "Lateral" : [1, 7],
            "In" : [0, 5],
            "Out" : [3, 6]
        }
        Edges = geompy.ExtractShapes(face, geompy.ShapeType["EDGE"], True)
        for BC in dict_Lamina:
            edges = geompy.CreateGroup(face, geompy.ShapeType["EDGE"], f"Lamina_{BC}")
            geompy.UnionList(edges, [Edges[i] for i in dict_Lamina[BC]])
            Others_interfaces.append(edges)

    if Name in "Syringe":
        Edges = geompy.ExtractShapes(face, geompy.ShapeType["EDGE"], True)
        Syringe_edge = geompy.CreateGroup(face, geompy.ShapeType["EDGE"], "BC_Injection")
        geompy.UnionList(Syringe_edge, [Edges[2]])
        Others_interfaces.append(Syringe_edge)

    if Name in "AqueousHumor":
        Edges = geompy.ExtractShapes(face, geompy.ShapeType["EDGE"], True)
        # AH_Out_edge = geompy.CreateGroup(face, geompy.ShapeType["EDGE"], "AqueousHumor_Out")
        # geompy.UnionList(AH_Out_edge, [Edges[10], Edges[24]])
        # Others_interfaces.append(AH_Out_edge)

        AH_In_edge = geompy.CreateGroup(face, geompy.ShapeType["EDGE"], "AqueousHumor_In")
        geompy.UnionList(AH_In_edge, [Edges[18], Edges[27]])
        Others_interfaces.append(AH_In_edge)

    print("ok")

print("Done")

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()


Eye_Mesh = smesh.Mesh(EyePlan)
NETGEN_2D_1 = Eye_Mesh.Triangle(algo=smeshBuilder.NETGEN_1D2D)

smesh.SetName(Eye_Mesh.GetMesh(), 'Eye_Mesh')

# Set markers
Vitreous_humor_1 = Eye_Mesh.GroupOnGeom(VitreousHumor, 'VitreousHumor', SMESH.FACE)
Retina_1 = Eye_Mesh.GroupOnGeom(Retina, 'Retina', SMESH.FACE)
Choroid_1 = Eye_Mesh.GroupOnGeom(Group_Choroid, 'Choroid', SMESH.FACE)
Lens_1 = Eye_Mesh.GroupOnGeom(Lens, 'Lens', SMESH.FACE)
Iris_1 = Eye_Mesh.GroupOnGeom(Group_Iris, 'Iris', SMESH.FACE)
AqueousHumor_1 = Eye_Mesh.GroupOnGeom(AqueousHumor, 'AqueousHumor', SMESH.FACE)
Lamina_1 = Eye_Mesh.GroupOnGeom(Group_Lamina, 'Lamina', SMESH.FACE)
OpticNerve_1 = Eye_Mesh.GroupOnGeom(OpticNerve, 'OpticNerve', SMESH.FACE)
Cornea_1 = Eye_Mesh.GroupOnGeom(Cornea, 'Cornea', SMESH.FACE)
Sclera_1 = Eye_Mesh.GroupOnGeom(Group_Sclera, 'Sclera', SMESH.FACE)
if add_syringe:
    Syringe_1 = Eye_Mesh.GroupOnGeom(Syringe, 'Syringe', SMESH.FACE)


Done = []
for item in Others_interfaces:
    Name = item.GetName()
    if Name not in Done:
        BC_Group_Mesh = Eye_Mesh.GroupOnGeom(item, Name, SMESH.EDGE)
        print(Name, " added")
        Done.append(Name)

for interface in Interfaces:
    for item in interface:
        Name = item.GetName()
        if Name not in Done:
            if "Lamina" not in Name:
                BC_Group_Mesh = Eye_Mesh.GroupOnGeom(item, Name, SMESH.EDGE)
                print(Name, " added")
                Done.append(Name)

NETGEN_2D_Parameters = NETGEN_2D_1.Parameters()
NETGEN_2D_Parameters.SetMaxSize( 0.5 )


isDone = Eye_Mesh.Compute()
assert isDone

print(Eye_Mesh.Dump())

Eye_Mesh.ExportMED( f"EyeMesh_2d.med", 0, SMESH.MED_V2_2, 1, None ,1)





######################"
# Second mesh

Eye_AH = geompy.MakePartition([AqueousHumorPlan, syringe], [], [], [], geompy.ShapeType["FACE"], 0, [], 0)
[SyringeAH, AqueousHumorAH] = geompy.ExtractShapes(Eye_AH, geompy.ShapeType["FACE"], True)

Edges_AqueousHumorAH = geompy.ExtractShapes(AqueousHumorAH, geompy.ShapeType["EDGE"], True)
# for i, edge in enumerate(Edges_AqueousHumorAH):
#     geompy.addToStudy(edge, f"Edge_AqueousHumorAH_{i}")
Edges_SyringeAH = geompy.ExtractShapes(SyringeAH, geompy.ShapeType["EDGE"], True)
# for i, edge in enumerate(Edges_SyringeAH):
    # geompy.addToStudy(edge, f"Edge_SyringeAH_{i}")

BC_Injection_Edges = [Edges_SyringeAH[2]]
AqueousHumor_In_Edges = [Edges_AqueousHumorAH[18], Edges_AqueousHumorAH[27]]
AqueousHumor_Cornea_Edges = [Edges_AqueousHumorAH[0], Edges_AqueousHumorAH[1]]
AqueousHumor_Iris_Edges = Edges_AqueousHumorAH[6:10] + Edges_AqueousHumorAH[12:16] + [Edges_AqueousHumorAH[19], Edges_AqueousHumorAH[21], Edges_AqueousHumorAH[26], Edges_AqueousHumorAH[28]]
AqueousHumor_Lens_Edges = [Edges_AqueousHumorAH[11], Edges_AqueousHumorAH[16], Edges_AqueousHumorAH[17], Edges_AqueousHumorAH[20], Edges_AqueousHumorAH[23], Edges_AqueousHumorAH[25]]
AqueousHumor_Syringe_Edges = [Edges_AqueousHumorAH[2], Edges_AqueousHumorAH[3], Edges_AqueousHumorAH[4], Edges_AqueousHumorAH[5], Edges_AqueousHumorAH[7], Edges_AqueousHumorAH[8], Edges_AqueousHumorAH[9]]
AqueousHumor_VitreousHumor_Edges = [Edges_AqueousHumorAH[22], Edges_AqueousHumorAH[29]]
AqueousHumor_Sclera_Edges = [Edges_AqueousHumorAH[10], Edges_AqueousHumorAH[24]]

Eye_Mesh_AH = smesh.Mesh(Eye_AH)

NETGEN_2D_1_AH = Eye_Mesh_AH.Triangle(algo=smeshBuilder.NETGEN_1D2D)
smesh.SetName(Eye_Mesh_AH.GetMesh(), 'Eye_Mesh_AH')

# Set markers
Vitreous_humor_1_AH = Eye_Mesh_AH.GroupOnGeom(AqueousHumorAH, 'AqueousHumor', SMESH.FACE)
if add_syringe:
    Syringe_1_AH = Eye_Mesh_AH.GroupOnGeom(SyringeAH, 'Syringe', SMESH.FACE)
Done = []
Names = ["AqueousHumor_In", "AqueousHumor_Cornea", "AqueousHumor_Iris", "AqueousHumor_Lens", "AqueousHumor_Syringe", "AqueousHumor_VitreousHumor", "AqueousHumor_Sclera", "BC_Injection"]

for name, edges in zip(Names, [AqueousHumor_In_Edges, AqueousHumor_Cornea_Edges, AqueousHumor_Iris_Edges, AqueousHumor_Lens_Edges, AqueousHumor_Syringe_Edges, AqueousHumor_VitreousHumor_Edges, AqueousHumor_Sclera_Edges, BC_Injection_Edges]):
    if name not in Done:
        BC_Group = geompy.CreateGroup(Eye_AH, geompy.ShapeType["EDGE"], name)
        geompy.UnionList(BC_Group, edges)
        BC_Group_Mesh = Eye_Mesh_AH.GroupOnGeom(BC_Group, name, SMESH.EDGE)
        print(name, " added")
        Done.append(name)




NETGEN_2D_Parameters_AH = NETGEN_2D_1_AH.Parameters()
NETGEN_2D_Parameters_AH.SetMaxSize( 0.06 )

isDone = Eye_Mesh_AH.Compute()
assert isDone

print(Eye_Mesh_AH.Dump())

Eye_Mesh_AH.ExportMED( f"EyeMesh_AH.med", 0, SMESH.MED_V2_2, 1, None ,1)