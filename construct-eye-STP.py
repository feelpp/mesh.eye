# -*- coding: utf-8 -*-
### This script build a new step file for the geometry of the eye.
### Input: human_eye.stp (should be in the current directory)
### Output: eye.stp, containing the right volumes

### to run the script:
###    path/to/salome [-t] construct-eye-STP.py [args:[--distance=],[--width=],[--hole=],[--shift=],[--eye_length=],[--step=]]
###    salome -t shell eye.py args:--mesh


### output:
###   STEP file of the modified geometry


import sys
import salome
import time

from eye_utils import *

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


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--distance", help="distance from retina/sclera [mm]", type=float, default=0.25)
parser.add_argument("--width", help="lamina cribosa width [mm]", type=float, default=0.2)
parser.add_argument("--hole", help="radius if the hole in in lamina cribosa [mm]", type=float, default=0.2)
parser.add_argument("--shift", help="shift hole from lamina cribosa center [mm]", type=float, default=0.3)
parser.add_argument("--eye_length", help="length of main axis of the eye [mm]", type=float, default=26.1)
parser.add_argument("--step", help="path to human_eye.stp file", type=str, default="human_eye.stp")
args = parser.parse_args()

distance_from_sclera = args.distance
hole = args.hole
depth = args.width
shift = args.shift
scale_factor = args.eye_length / 26.1


###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
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

Human_Eye = geompy.ImportSTEP(args.step, True)


geom_time = time.time()

[Cornea_h, Iris___Ciliary_Body_h, Suspensory_Ligament_h, Lens_Body_h, Vitreous_humor_h, Sclera_h, Choroid_h, Retina_h, Vein_h, Artery_h] = geompy.ExtractShapes(Human_Eye, geompy.ShapeType["SOLID"], True)
geompy.addToStudy( Human_Eye, 'Human Eye' )
geompy.addToStudyInFather( Human_Eye, Cornea_h, 'Cornea' )
geompy.addToStudyInFather( Human_Eye, Vitreous_humor_h, 'Vitreous humor' )
geompy.addToStudyInFather( Human_Eye, Iris___Ciliary_Body_h, 'Iris & Ciliary Body' )
geompy.addToStudyInFather( Human_Eye, Suspensory_Ligament_h, 'Suspensory Ligament' )
geompy.addToStudyInFather( Human_Eye, Lens_Body_h, 'Lens Body' )
geompy.addToStudyInFather( Human_Eye, Sclera_h, 'Sclera' )
geompy.addToStudyInFather( Human_Eye, Choroid_h, 'Choroid' )
geompy.addToStudyInFather( Human_Eye, Retina_h, 'Retina' )
geompy.addToStudyInFather( Human_Eye, Vein_h, 'Vein of the Retina' )
geompy.addToStudyInFather( Human_Eye, Artery_h, 'Central Artery of the Retian' )


# Solids already ok
Cornea = Cornea_h
Iris = Iris___Ciliary_Body_h
Lens = Lens_Body_h
Choroid = Choroid_h


# Build lamina
print("Building Lamina...", end=' ')
Lamina0 = build_lamina(geompy, Retina_h, Sclera_h, distance_from_sclera, depth, shift, hole)
assert Lamina0 is not None, "Lamina is None"
print("Done")

# Build new sclera
print("Building New Sclera...", end=' ')
Sclera0, _ = build_sclera(geompy, Sclera_h)
print("Done")

# Build new Retina and Pia
print("Building New Retina...", end=' ')
Retina0, Pia0, InterFaceRetina = build_retina(geompy, Retina_h, Choroid_h)
print("Done")

# translate lamina
print("Translating Lamina...", end=' ')
Lamina1 = translate_lamina(geompy, Lamina0, InterFaceRetina)
print("Done")

# fill retina
print("Filling Retina...", end=' ')
Retina = fill_retina(geompy, Retina0)
print("Done")

# fill sclera
print("Filling Sclera...", end=' ')
Sclera1 = fill_sclera(geompy, Sclera0)
print("Done")

# build Optic Nerve
print("Building Optic Nerve...", end=' ')
wholeOpticNerve, OpticNerve = build_optic_nerve(geompy, Pia0, Lamina1)
print("Done")

# modyfy sclera for optic nerve and lamina
print("Modifying Sclera...", end=' ')
Sclera2 = modify_sclera(geompy, Sclera1, wholeOpticNerve)
print("Done")

# fit lamina to optic nerve
print("Fitting Lamina to Optic Nerve...", end=' ')
Lamina = fit_lamina_to_optic_nerve(geompy, Retina, OpticNerve, wholeOpticNerve)
print("Done")

# fit sclera to lamina
print("Fitting Sclera to Lamina...", end=' ')
Sclera = fit_sclera_to_lamina(geompy, Sclera2, Lamina)
print("Done")

# glue faces
print("Glue Faces...", end=' ')
eye_partition0 = build_first_partition(geompy, Sclera, Retina, OpticNerve, Cornea, Iris, Suspensory_Ligament_h, Lens, Vitreous_humor_h, Choroid, Lamina, scale_factor)
print("Done")
[Cornea, Iris, Ligament, Lens, Vitreous_humor0, Sclera, Choroid, Retina, Lamina, OpticNerve] = geompy.ExtractShapes(eye_partition0, geompy.ShapeType["SOLID"], True)

# build aqueousHumor
print("Building aqueous humor...", end=' ')
Aqueous_humor = build_aqueous_humor(geompy, Cornea, Sclera, Iris, Lens, Ligament, Vitreous_humor0)
print("Done")

# build vitreous humor
print("Building vitreous humor...", end=' ')
Vitreous_humor = build_vitreous_humor(geompy, Lens, Aqueous_humor, Retina, Iris, Choroid)
print("Done")


eye0 = geompy.MakePartition( [Cornea, Aqueous_humor, Iris, Lens, Vitreous_humor, Sclera, Choroid, Retina, Lamina, OpticNerve], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
eye = geompy.RemoveInternalFaces( eye0 )
geompy.addToStudy(eye, "Eye")
geompy.addToStudyInFather( eye, Cornea, 'Cornea' )
geompy.addToStudyInFather( eye, Aqueous_humor, 'Aqueous Humor' )
geompy.addToStudyInFather( eye, Iris, 'Iris' )
geompy.addToStudyInFather( eye, Lens, 'Lens' )
geompy.addToStudyInFather( eye, Vitreous_humor, 'Vitreous Humor' )
geompy.addToStudyInFather( eye, Sclera, 'Sclera' )
geompy.addToStudyInFather( eye, Choroid, 'Choroid' )
geompy.addToStudyInFather( eye, Retina, 'Retina' )
geompy.addToStudyInFather( eye, Lamina, 'Lamina' )
geompy.addToStudyInFather( eye, OpticNerve, 'Optic Nerve' )

Aqueous_humor.SetColor(SALOMEDS.Color(0.5019,0.0941,0.0941))
Choroid.SetColor(SALOMEDS.Color(1,0.0784,0.5764))
Cornea.SetColor(SALOMEDS.Color(1,1,0))
Iris.SetColor(SALOMEDS.Color(0.1843,0.4588,1))
Lamina.SetColor(SALOMEDS.Color(0,1,0))
Lens.SetColor(SALOMEDS.Color(0,0.666667,0))
OpticNerve.SetColor(SALOMEDS.Color(0.666667,0,1))
Retina.SetColor(SALOMEDS.Color(0,0,0))
Sclera.SetColor(SALOMEDS.Color(1,1,1))
Vitreous_humor.SetColor(SALOMEDS.Color(1,0.6470,0))

geompy.ExportSTEP(eye0, "Eye.step", GEOM.LU_METER )
