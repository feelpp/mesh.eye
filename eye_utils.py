def build_lamina(geompy, retina, sclera, distance_from_sclera, depth, shift, hole):
    """Build the lamina cribrosa from the retina and the sclera

    Args:
        geompy (salome.geomBuilder): The geompy object
        retina (GEOM_Object): Retina object
        sclera (GEOM_Object): Sclera object
        distance_from_sclera (float): Distance from the sclera to the lamina
        depth (float): Depth of the lamina
        shift (float): Shift of the lamina hole
        hole (float): Hole size

    Returns:
        GEOM_Object: The lamina cribrosa built
    """
    [Face_18,Face_19,Face_20,Face_21,Face_22,Face_23,Face_24,Face_25,Face_26,Face_27,Face_28,Face_29,Face_30] = geompy.ExtractShapes(retina, geompy.ShapeType["FACE"], True)
    [Face_1,Face_2,Face_3,Face_4,Face_5,Face_6,Face_7,Face_8,Face_9,Face_10,Face_11,Face_12,Face_13,Face_14,Face_15,Face_16,Face_17] = geompy.ExtractShapes(sclera, geompy.ShapeType["FACE"], True)
    [Wire_7] = geompy.ExtractShapes(Face_13, geompy.ShapeType["WIRE"], True) # interior of the sclera (bottom)
    [Wire_8] = geompy.ExtractShapes(Face_14, geompy.ShapeType["WIRE"], True) # interior of the sclera (top)
    [Wire_3] = geompy.ExtractShapes(Face_26, geompy.ShapeType["WIRE"], True) # interior of the retine (bottom)
    [Wire_4] = geompy.ExtractShapes(Face_27, geompy.ShapeType["WIRE"], True) # interior of the retine (top)

    [Edge_1,Edge_2,Edge_3,Edge_4] = geompy.ExtractShapes(Wire_3, geompy.ShapeType["EDGE"], True)
    [Edge_5,Edge_6,Edge_7,Edge_8] = geompy.ExtractShapes(Wire_4, geompy.ShapeType["EDGE"], True)
    Base_retina = geompy.MakeFuseList([Edge_5, Edge_1], True, True)
    Base_R = geompy.MakeCDG(Base_retina)
    Top_Retina = geompy.MakeFuseList([Edge_8, Edge_4], True, True)
    Top_R = geompy.MakeCDG(Top_Retina)
    N_Base_retina = geompy.MakeVector(Base_R, Top_R)

    # Should get vector in the Base_retina plane
    [P0, P1] = geompy.ExtractShapes(Edge_5, geompy.ShapeType["VERTEX"], True)
    T0_Base_retina = geompy.MakeVector(Base_R, P0)

    [Edge_19,Edge_20,Edge_21,Edge_22] = geompy.ExtractShapes(Wire_7, geompy.ShapeType["EDGE"], True)
    [Edge_23,Edge_24,Edge_25,Edge_26] = geompy.ExtractShapes(Wire_8, geompy.ShapeType["EDGE"], True)

    Inner_Bas_sclera = geompy.MakeFuseList([Edge_19, Edge_23], True, True)
    Inner_Bas_S = geompy.MakeCDG(Inner_Bas_sclera)
    Vector_2 = geompy.MakeVector(Base_R, Inner_Bas_S)
    Translation_2 = geompy.MakeTranslationVectorDistance(Base_retina, Vector_2, distance_from_sclera)
    Lamina_Base = geompy.MakeFaceWires([Translation_2], 1)
    # geompy.addToStudy(Lamina_Base, "Lamina_Base")

    Laminia_Top = geompy.MakeTranslationVectorDistance(Lamina_Base, Vector_2, depth)
    G_Lamina_T = geompy.MakeCDG(Laminia_Top)
    Vector_3 = geompy.MakeVector(Inner_Bas_S, G_Lamina_T)

    Scaled_Lamina_w_hole_1 = None
    try:
        DZ_Hole = geompy.BasicProperties(N_Base_retina)[0]
        DR_Hole = geompy.BasicProperties(T0_Base_retina)[0]
        # should check if shift is lesser than DR_Hole-2*hole
        if shift > DR_Hole - 2*hole:
            raise Exception(f"pb with shift size ({shift})")

        Base_R_1 = geompy.MakeTranslationVectorDistance(Base_R, N_Base_retina, -0.5*DZ_Hole)
        Cylinder_1 = geompy.MakeCylinder(Base_R_1, N_Base_retina, hole, 1.5*DZ_Hole)
        Translation_Cyl = geompy.MakeTranslationVectorDistance(Cylinder_1, T0_Base_retina, shift)

        G_Lamina_Base = geompy.MakeCDG(Lamina_Base)
        Scaled_Lamina_Base = geompy.MakeScaleTransform(Lamina_Base, G_Lamina_Base, 1.2)
        p1, p2 = geompy.SubShapeAll(Vector_3, geompy.ShapeType["VERTEX"])
        Scaled_Lamina_cribosa = geompy.MakePrism(Scaled_Lamina_Base, p1, p2)

        # geompy.addToStudy( Scaled_Lamina_cribosa, 'Scaled_Lamina_cribosa' )
        # geompy.addToStudy( Translation_Cyl, 'Translation_Cyl' )
        # geompy.addToStudy( Scaled_Lamina_Base, 'Scaled_Lamina_Base' )
        # geompy.addToStudy( retina, 'retina' )

        print("Cutting Lamina...")
        Scaled_Lamina_w_hole = geompy.MakeCutList(Scaled_Lamina_cribosa, [Translation_Cyl], False)
        # geompy.addToStudy( Scaled_Lamina_w_hole, 'Scaled_Lamina_w_hole' )
        print("Cutting Lamina2...")
        Scaled_Lamina_w_hole_1 = geompy.MakeCutList(Scaled_Lamina_w_hole, [retina], True)
        print("Cutting Lamina2... done")


    except Exception as e:
        print("Failed to build Lamina :")
        print(e)
        return None

    return Scaled_Lamina_w_hole_1

def build_sclera(geompy, sclera):
    [FaceScl_1, FaceScl_2, FaceScl_3, FaceScl_4, FaceScl_5, FaceScl_6, FaceScl_7, FaceScl_8, FaceScl_9, FaceScl_10, FaceScl_11, FaceScl_12, FaceScl_13, FaceScl_14, FaceScl_15, FaceScl_16, FaceScl_17] = geompy.ExtractShapes( sclera, geompy.ShapeType["FACE"], True)
    [EdgeScl_1, EdgeScl_2, EdgeScl_3, EdgeScl_4, EdgeScl_5, EdgeScl_6] = geompy.ExtractShapes( FaceScl_11, geompy.ShapeType["EDGE"], True)
    [EdgeScl_7, EdgeScl_8, EdgeScl_9, EdgeScl_10, EdgeScl_11, EdgeScl_12] = geompy.ExtractShapes( FaceScl_12, geompy.ShapeType["EDGE"], True)
    InterFaceSclera = geompy.MakeFaces( [EdgeScl_1, EdgeScl_4, EdgeScl_8, EdgeScl_10], True ) # raises a Warning : Cannot build a planar face: required tolerance is too big. Non-planar face is built.
    Base_Scl = geompy.MakeCDG(InterFaceSclera)
    Normal_Scl = geompy.GetNormal(InterFaceSclera, Base_Scl)
    PlaneSclera = geompy.MakePlane(Base_Scl, Normal_Scl, 10)

    PartitionSclera = geompy.MakePartition([sclera], [PlaneSclera], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    [NewSclera, SolidSclera] = geompy.ExtractShapes( PartitionSclera, geompy.ShapeType["SOLID"], True)

    return NewSclera, SolidSclera

def build_retina(geompy, retina, choroid):
    [FaceChor_43, FaceChor_44, FaceChor_45, FaceChor_46, FaceChor_47, FaceChor_48, FaceChor_49, FaceChor_50, FaceChor_51, FaceChor_52, FaceChor_53, FaceChor_54, FaceChor_55, FaceChor_56] = geompy.ExtractShapes( choroid, geompy.ShapeType["FACE"], True)
    [EdgeChor_19, EdgeChor_20, EdgeChor_21, EdgeChor_22, EdgeChor_23, EdgeChor_24, EdgeChor_25, EdgeChor_26] = geompy.ExtractShapes( FaceChor_53, geompy.ShapeType["EDGE"], True)
    [EdgeChor_27, EdgeChor_28, EdgeChor_29, EdgeChor_30, EdgeChor_31, EdgeChor_32, EdgeChor_33, EdgeChor_34] = geompy.ExtractShapes( FaceChor_54, geompy.ShapeType["EDGE"], True)
    InterFaceRetina = geompy.MakeFaces( [EdgeChor_25, EdgeChor_33], True )
    PlaneRetina = geompy.MakePlaneFace(InterFaceRetina, 10)
    PartitionRetina = geompy.MakePartition([retina], [PlaneRetina], [], [], geompy.ShapeType["SOLID"], 0, [], 0)

    [NewRetina, Pia] = geompy.ExtractShapes( PartitionRetina, geompy.ShapeType["SOLID"], True)

    return NewRetina, Pia, InterFaceRetina

def translate_lamina(geompy, lamina, InterFaceRetina):
    [FaceLam_1, FaceLam_2, FaceLam_3, FaceLam_4, FaceLam_5] = geompy.ExtractShapes( lamina, geompy.ShapeType["FACE"], True)
    Base_Lamina = geompy.MakeCDG(FaceLam_2)
    Base_InterFaceRetina = geompy.MakeCDG(InterFaceRetina)
    Scaled_Lamina_w_hole_2 = geompy.MakeTranslationTwoPoints(lamina, Base_Lamina, Base_InterFaceRetina)
    return Scaled_Lamina_w_hole_2

def fill_retina(geompy, retina):
    [FaceRet_1, FaceRet_2, FaceRet_3, FaceRet_4, FaceRet_5, FaceRet_6, FaceRet_7, FaceRet_8, FaceRet_9, FaceRet_10, FaceRet_11, FaceRet_12, FaceRet_13 ] = geompy.ExtractShapes( retina, geompy.ShapeType["FACE"], True)
    [EdgeRet_1, EdgeRet_2, EdgeRet_3, EdgeRet_4] = geompy.ExtractShapes( FaceRet_9, geompy.ShapeType["EDGE"], True)
    [EdgeRet_5, EdgeRet_6, EdgeRet_7, EdgeRet_8] = geompy.ExtractShapes( FaceRet_10, geompy.ShapeType["EDGE"], True)

    FaceFillingRetina = geompy.MakeFaces([EdgeRet_3, EdgeRet_7], True )
    ShellFillingRetina = geompy.MakeShell([FaceFillingRetina, FaceRet_7, FaceRet_8, FaceRet_9, FaceRet_10] )
    FillingRetina = geompy.MakeSolid(ShellFillingRetina)
    NewRetina_1 = geompy.MakePartition([FillingRetina, retina], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    NewRetina_2 = geompy.RemoveInternalFaces( NewRetina_1 )
    return NewRetina_2

def fill_sclera(geompy, sclera):
    [FaceNewScl_1, FaceNewScl_2, FaceNewScl_3, FaceNewScl_4, FaceNewScl_5, FaceNewScl_6, FaceNewScl_7, FaceNewScl_8, FaceNewScl_9, FaceNewScl_10, FaceNewScl_11, FaceNewScl_12, FaceNewScl_13, FaceNewScl_14, FaceNewScl_15, FaceNewScl_16, FaceNewScl_17] = geompy.ExtractShapes( sclera, geompy.ShapeType["FACE"], True)
    [EdgeScl_13, EdgeScl_14, EdgeScl_15, EdgeScl_16] = geompy.ExtractShapes( FaceNewScl_13, geompy.ShapeType["EDGE"], True)
    [EdgeScl_17, EdgeScl_18, EdgeScl_19, EdgeScl_20] = geompy.ExtractShapes( FaceNewScl_14, geompy.ShapeType["EDGE"], True)
    FaceNewScl_18 = geompy.MakeFaces([EdgeScl_14 , EdgeScl_18], True)
    FaceNewScl_19 = geompy.MakeFaces([EdgeScl_15 , EdgeScl_19], True)

    ShellFillingSclera = geompy.MakeShell([FaceNewScl_13, FaceNewScl_14, FaceNewScl_18, FaceNewScl_19] )
    FillingSclera = geompy.MakeSolid(ShellFillingSclera)
    NewSclera_1 = geompy.MakePartition([FillingSclera, sclera], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    NewSclera_2 = geompy.RemoveInternalFaces( NewSclera_1 )
    return NewSclera_2

def build_optic_nerve(geompy, pia, lamina):

    [FacePia_1, FacePia_2, FacePia_3, FacePia_4, FacePia_5, FacePia_6] = geompy.ExtractShapes( pia, geompy.ShapeType["FACE"], True)
    [EdgePia_1, EdgePia_2, EdgePia_3, EdgePia_4] = geompy.ExtractShapes( FacePia_4, geompy.ShapeType["EDGE"], True)
    [EdgePia_5, EdgePia_6, EdgePia_7, EdgePia_8] = geompy.ExtractShapes( FacePia_5, geompy.ShapeType["EDGE"], True)

    BaseOpt = geompy.MakeFaces( [EdgePia_1, EdgePia_5], True )
    TopOpt = geompy.MakeFaces( [EdgePia_4, EdgePia_8], True )
    ShellOpt = geompy.MakeShell( [BaseOpt, FacePia_4, FacePia_5, TopOpt] )
    OpticNerve = geompy.MakeSolid( ShellOpt )
    OpticNerve_1 = geompy.MakeCutList(OpticNerve, [lamina], True)

    [FaceOpt_1, FaceOpt_2, FaceOpt_3, FaceOpt_4, FaceOpt_5, FaceOpt_6, FaceOpt_7, FaceOpt_8, FaceOpt_9, FaceOpt_10] = geompy.ExtractShapes( OpticNerve_1, geompy.ShapeType["FACE"], True)
    ok, closed_wires, open_wires = geompy.GetFreeBoundary(FaceOpt_5)
    # take the wire that creates a planara face
    planar_face = None
    for wire in closed_wires:
      face = geompy.MakeFace(wire, 1)
      # check that the face is planar
      kindof = geompy.KindOfShape(face)
      if kindof[0] == geompy.kind.PLANAR:
        planar_face = face
        break
    if planar_face is None:
      raise Exception("Could not find a wire that lead to a planar face")
    FaceToCutOpt = planar_face
    PlaneToCutOpt = geompy.MakePlaneFace(FaceToCutOpt, 10)
    PartitionOpt = geompy.MakePartition([OpticNerve_1], [PlaneToCutOpt], [], [], geompy.ShapeType["SOLID"], 0, [], 0)

    Plane_1 = PlaneToCutOpt

    Partition_1 = geompy.MakePartition([OpticNerve], [Plane_1], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    [_, PartOpticNerve_2] = geompy.ExtractShapes(Partition_1, geompy.ShapeType['SOLID'],True)

    [OpticCut_1, OpticCut_2, OpticCut_3] = geompy.ExtractShapes( PartitionOpt, geompy.ShapeType["SOLID"], True )
    NewOptic0 = geompy.MakePartition([OpticCut_1, PartOpticNerve_2], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    NewOptic = geompy.RemoveInternalFaces( NewOptic0 )

    [FaceNewOpt_1, FaceNewOpt_2, FaceNewOpt_3, FaceNewOpt_4, FaceNewOpt_5, FaceNewOpt_6 ] = geompy.ExtractShapes( NewOptic, geompy.ShapeType["FACE"], True) # has 12 faces
    edge_FaceNewOpt_3 = geompy.ExtractShapes( FaceNewOpt_3, geompy.ShapeType["EDGE"], True) # has 3 edges (or 2 in 9.12)

    NewFaceForOptic = geompy.MakeFaces( edge_FaceNewOpt_3, True )
    ShellForOptic = geompy.MakeShell ( [ NewFaceForOptic, FaceNewOpt_1, FaceNewOpt_2, FaceNewOpt_4, FaceNewOpt_5, FaceNewOpt_6] )
    NewOptic_3 = geompy.MakeSolid ( ShellForOptic )
    return OpticNerve, NewOptic_3

def modify_sclera(geompy, scelra, opticNerve):
    NewSclera = geompy.MakeCutList(scelra, [opticNerve], True)
    return NewSclera

def fit_lamina_to_optic_nerve(geompy, retina, opticNerve, wholeOpticNerve):
    PartitionForLamina = geompy.MakePartition([retina, opticNerve], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    NewLamina_1 = geompy.MakeCutList(wholeOpticNerve, [PartitionForLamina], True)

    return NewLamina_1

def fit_sclera_to_lamina(geompy, sclera, lamina):
    [FaceNewLam_1, FaceNewLam_2, FaceNewLam_3, FaceNewLam_4, FaceNewLam_5 ] = geompy.ExtractShapes( lamina, geompy.ShapeType["FACE"], True)
    PlaneToCutSclera =  geompy.MakePlaneFace(FaceNewLam_2, 10)
    BaseLaminaPoint = geompy.MakeCDG ( FaceNewLam_2 )
    BaseLaminaNormal = geompy.GetNormal ( FaceNewLam_2, BaseLaminaPoint )

    PlaneToCutSclera_Translated = geompy.MakeTranslationVectorDistance(PlaneToCutSclera, BaseLaminaNormal, -0.46)
    ScleraPartition_1 = geompy.MakePartition([ sclera ], [PlaneToCutSclera_Translated], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    [NewSclera_4, _] = geompy.ExtractShapes( ScleraPartition_1, geompy.ShapeType["SOLID"], True)

    return NewSclera_4

def build_first_partition(geompy, Sclera, Retina, OpticNerve, Cornea, Iris, Suspensory_Ligament_h, Lens, Vitreous_humor_h, Choroid, Lamina, scale_factor):
    Partition_RetinaSclera = geompy.MakePartition([ Sclera, Retina, OpticNerve ], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    Partition_ = geompy.MakePartition([ Cornea, Iris, Suspensory_Ligament_h, Lens, Vitreous_humor_h, Partition_RetinaSclera, Choroid, Lamina], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    Partition_glue = geompy.MakeGlueFaces(Partition_, 1e-09)
    Partition_scaled = geompy.MakeScaleTransform(Partition_glue, None, scale_factor)
    return Partition_scaled

def build_aqueous_humor(geompy, cornea, sclera, iris, lens, ligament, vitreousHumor):
    [geomObj_313,geomObj_314,Interfaces_Cornea0,Interfaces_Cornea1,geomObj_315,geomObj_316] = geompy.ExtractShapes(cornea, geompy.ShapeType["FACE"], True)
    [Interfaces_Iris0,Interfaces_Iris1,Interfaces_Iris2,Interfaces_Iris3,Interfaces_Iris4,Interfaces_Iris5,Interfaces_Iris6,Interfaces_Iris7,geomObj_317,geomObj_318,Interfaces_Iris8,geomObj_319,geomObj_320,Interfaces_Iris9,geomObj_321,geomObj_322,Interfaces_Iris10,geomObj_323,geomObj_324,geomObj_325,geomObj_326,Interfaces_Iris11,geomObj_327,geomObj_328,geomObj_329,geomObj_330,Interfaces_Iris12,Interfaces_Iris13,geomObj_331,geomObj_332,Interfaces_Iris14,Interfaces_Iris15,Interfaces_Iris16,geomObj_333,geomObj_334,geomObj_335,Interfaces_Iris17,geomObj_336,Interfaces_Iris18,Interfaces_Iris19,Interfaces_Iris20,geomObj_337,geomObj_338,geomObj_339,geomObj_340,Interfaces_Iris21,Interfaces_Iris22,geomObj_341,geomObj_342,Interfaces_Iris23,geomObj_343,geomObj_344,Interfaces_Iris24,Interfaces_Iris25,geomObj_345,geomObj_346,geomObj_347,geomObj_348,geomObj_349,geomObj_350,Interfaces_Iris26,Interfaces_Iris27,Interfaces_Iris28,Interfaces_Iris29,Interfaces_Iris30,Interfaces_Iris31,geomObj_351,geomObj_352,geomObj_353,geomObj_354,Interfaces_Iris32,Interfaces_Iris33,Interfaces_Iris34,Interfaces_Iris35,geomObj_355,geomObj_356,geomObj_357,geomObj_358,Interfaces_Iris36,Interfaces_Iris37,Interfaces_Iris38,Interfaces_Iris39,geomObj_359,geomObj_360,geomObj_361,geomObj_362,Interfaces_Iris40,Interfaces_Iris41,geomObj_363,Interfaces_Iris42,geomObj_364,Interfaces_Iris43,Interfaces_Iris44,Interfaces_Iris45,Interfaces_Iris46,Interfaces_Iris47,geomObj_365,geomObj_366,Interfaces_Iris48,geomObj_367,geomObj_368,geomObj_369,geomObj_370,Interfaces_Iris49,Interfaces_Iris50,geomObj_371,geomObj_372,Interfaces_Iris51,Interfaces_Iris52,geomObj_373,geomObj_374,Interfaces_Iris53,Interfaces_Iris54,geomObj_375,geomObj_376,geomObj_377,Interfaces_Iris55,geomObj_378,geomObj_379,Interfaces_Iris56,Interfaces_Iris57,geomObj_380,geomObj_381,geomObj_382] = geompy.ExtractShapes(iris, geompy.ShapeType["FACE"], True)
    [geomObj_383,Interfaces_Ligament0,Interfaces_Ligament1,Interfaces_Ligament2,Interfaces_Ligament3,Interfaces_Ligament4,Interfaces_Ligament5,Interfaces_Ligament6,Interfaces_Ligament7,Interfaces_Ligament8,Interfaces_Ligament9,geomObj_384,Interfaces_Ligament10,Interfaces_Ligament11,Interfaces_Ligament12,Interfaces_Ligament13,Interfaces_Ligament14,Interfaces_Ligament15,geomObj_385,geomObj_386,geomObj_387,geomObj_388,geomObj_389,geomObj_390,Interfaces_Ligament16,Interfaces_Ligament17,Interfaces_Ligament18,Interfaces_Ligament19,geomObj_391,geomObj_392,geomObj_393,geomObj_394,Interfaces_Ligament20,Interfaces_Ligament21,geomObj_395,Interfaces_Ligament22,geomObj_396,Interfaces_Ligament23,geomObj_397,geomObj_398,Interfaces_Ligament24,Interfaces_Ligament25,Interfaces_Ligament26,Interfaces_Ligament27,geomObj_399,geomObj_400,Interfaces_Ligament28,geomObj_401,geomObj_402,Interfaces_Ligament29,Interfaces_Ligament30,Interfaces_Ligament31,geomObj_403,Interfaces_Ligament32,Interfaces_Ligament33,geomObj_404,Interfaces_Ligament34,Interfaces_Ligament35,geomObj_405,geomObj_406,Interfaces_Ligament36,geomObj_407,Interfaces_Ligament37,geomObj_408,Interfaces_Ligament38,Interfaces_Ligament39,geomObj_409,geomObj_410,Interfaces_Ligament40,geomObj_411,Interfaces_Ligament41,geomObj_412,geomObj_413,geomObj_414,geomObj_415,geomObj_416,geomObj_417,geomObj_418,Interfaces_Ligament42,Interfaces_Ligament43,geomObj_419,Interfaces_Ligament44,Interfaces_Ligament45,geomObj_420,geomObj_421,geomObj_422,Interfaces_Ligament46,geomObj_423,Interfaces_Ligament47,geomObj_424,geomObj_425,geomObj_426,Interfaces_Ligament48,Interfaces_Ligament49,geomObj_427,geomObj_428,geomObj_429,geomObj_430,Interfaces_Ligament50,Interfaces_Ligament51,geomObj_431,geomObj_432,geomObj_433,geomObj_434,Interfaces_Ligament52,geomObj_435,Interfaces_Ligament53,geomObj_436,Interfaces_Ligament54,Interfaces_Ligament55,geomObj_437,geomObj_438,Interfaces_Ligament56,Interfaces_Ligament57,Interfaces_Ligament58,Interfaces_Ligament59,geomObj_439,geomObj_440,geomObj_441,geomObj_442,geomObj_443,geomObj_444,geomObj_445,geomObj_446] = geompy.ExtractShapes(ligament, geompy.ShapeType["FACE"], True)
    [Interfaces_Lens0,Interfaces_Lens1,Interfaces_Lens2,Interfaces_Lens3,Interfaces_Lens4,Interfaces_Lens5,Interfaces_Lens6,Interfaces_Lens7,Interfaces_Lens8,Interfaces_Lens9,Interfaces_Lens10,Interfaces_Lens11,Interfaces_Lens12,Interfaces_Lens13,Interfaces_Lens14,Interfaces_Lens15,Interfaces_Lens16,Interfaces_Lens17,Interfaces_Lens18,Interfaces_Lens19,Interfaces_Lens20,Interfaces_Lens21,Interfaces_Lens22,Interfaces_Lens23,Interfaces_Lens24,Interfaces_Lens25,geomObj_447,geomObj_448,geomObj_449,geomObj_450] = geompy.ExtractShapes(lens, geompy.ShapeType["FACE"], True)
    [Interfaces_VitreousHumor0,Interfaces_VitreousHumor1,Interfaces_VitreousHumor2,Interfaces_VitreousHumor3,Interfaces_VitreousHumor4,Interfaces_VitreousHumor5,Interfaces_VitreousHumor6,Interfaces_VitreousHumor7,Interfaces_VitreousHumor8,Interfaces_VitreousHumor9,Interfaces_VitreousHumor10,Interfaces_VitreousHumor11,Interfaces_VitreousHumor12,Interfaces_VitreousHumor13,Interfaces_VitreousHumor14,Interfaces_VitreousHumor15,Interfaces_VitreousHumor16,Interfaces_VitreousHumor17,Interfaces_VitreousHumor18,Interfaces_VitreousHumor19,Interfaces_VitreousHumor20,Interfaces_VitreousHumor21,Interfaces_VitreousHumor22,Interfaces_VitreousHumor23,Interfaces_VitreousHumor24,Interfaces_VitreousHumor25,Interfaces_VitreousHumor26,geomObj_451,Interfaces_VitreousHumor27,Interfaces_VitreousHumor28,Interfaces_VitreousHumor29,Interfaces_VitreousHumor30,Interfaces_VitreousHumor31,Interfaces_VitreousHumor32,Interfaces_VitreousHumor33,Interfaces_VitreousHumor34,Interfaces_VitreousHumor35,Interfaces_VitreousHumor36,Interfaces_VitreousHumor37,Interfaces_VitreousHumor38,Interfaces_VitreousHumor39,Interfaces_VitreousHumor40,Interfaces_VitreousHumor41,geomObj_452,geomObj_453,geomObj_454,geomObj_455,geomObj_456,geomObj_457,geomObj_458,geomObj_459,geomObj_460,geomObj_461,geomObj_462,geomObj_463,geomObj_464,geomObj_465,geomObj_466] = geompy.ExtractShapes(vitreousHumor, geompy.ShapeType["FACE"], True)
    [geomObj_467,geomObj_468,Interfaces_Sclera0,Interfaces_Sclera1,geomObj_469,geomObj_470,geomObj_471,geomObj_472,geomObj_473,geomObj_474,geomObj_475,geomObj_476,geomObj_477,geomObj_478,geomObj_479,geomObj_480,geomObj_481,geomObj_482,geomObj_483,geomObj_484] = geompy.ExtractShapes(sclera, geompy.ShapeType["FACE"], True)

    Shell_1 = geompy.MakeShell([Interfaces_Cornea0, Interfaces_Cornea1, Interfaces_Sclera0, Interfaces_Sclera1, Interfaces_Iris0, Interfaces_Iris2, Interfaces_Iris1, Interfaces_Iris4, Interfaces_Iris6, Interfaces_Iris3, Interfaces_Iris5, Interfaces_Iris7, Interfaces_Iris8, Interfaces_Iris9, Interfaces_Iris10, Interfaces_Iris11, Interfaces_Iris12, Interfaces_Iris13, Interfaces_Iris14, Interfaces_Iris15, Interfaces_Iris16, Interfaces_Iris17, Interfaces_Iris18, Interfaces_Iris19, Interfaces_Iris20, Interfaces_Iris21, Interfaces_Iris22, Interfaces_Iris23, Interfaces_Iris24, Interfaces_Iris25, Interfaces_Iris26, Interfaces_Iris27, Interfaces_Iris28, Interfaces_Iris29, Interfaces_Iris30, Interfaces_Iris31, Interfaces_Iris32, Interfaces_Iris33, Interfaces_Iris34, Interfaces_Iris35, Interfaces_Iris36, Interfaces_Iris37, Interfaces_Iris38, Interfaces_Iris39, Interfaces_Iris40, Interfaces_Iris41, Interfaces_Iris42, Interfaces_Iris43, Interfaces_Iris44, Interfaces_Iris45, Interfaces_Iris46, Interfaces_Iris47, Interfaces_Iris48, Interfaces_Iris49, Interfaces_Iris50, Interfaces_Iris51, Interfaces_Iris52, Interfaces_Iris53, Interfaces_Iris54, Interfaces_Iris55, Interfaces_Iris56, Interfaces_Iris57, Interfaces_Lens0, Interfaces_Lens1, Interfaces_Lens2, Interfaces_Lens3, Interfaces_Lens4, Interfaces_Lens5, Interfaces_Lens6, Interfaces_Lens7, Interfaces_Lens8, Interfaces_Lens9, Interfaces_Lens10, Interfaces_Lens11, Interfaces_Lens12, Interfaces_Lens13, Interfaces_Lens14, Interfaces_Lens15, Interfaces_Lens16, Interfaces_Lens17, Interfaces_Lens18, Interfaces_Lens19, Interfaces_Lens20, Interfaces_Lens21, Interfaces_Lens22, Interfaces_Lens23, Interfaces_Lens24, Interfaces_Lens25, Interfaces_Ligament0, Interfaces_Ligament1, Interfaces_Ligament2, Interfaces_Ligament3, Interfaces_Ligament4, Interfaces_Ligament5, Interfaces_Ligament6, Interfaces_Ligament7, Interfaces_Ligament8, Interfaces_Ligament9, Interfaces_Ligament10, Interfaces_Ligament11, Interfaces_Ligament12, Interfaces_Ligament13, Interfaces_Ligament14, Interfaces_Ligament15, Interfaces_Ligament16, Interfaces_Ligament17, Interfaces_Ligament18, Interfaces_Ligament19, Interfaces_Ligament20, Interfaces_Ligament21, Interfaces_Ligament22, Interfaces_Ligament23, Interfaces_Ligament24, Interfaces_Ligament25, Interfaces_Ligament26, Interfaces_Ligament27, Interfaces_Ligament28, Interfaces_Ligament29, Interfaces_Ligament30, Interfaces_Ligament31, Interfaces_Ligament32, Interfaces_Ligament33, Interfaces_Ligament34, Interfaces_Ligament35, Interfaces_Ligament36, Interfaces_Ligament37, Interfaces_Ligament38, Interfaces_Ligament39, Interfaces_Ligament40, Interfaces_Ligament41, Interfaces_Ligament42, Interfaces_Ligament43, Interfaces_Ligament44, Interfaces_Ligament45, Interfaces_Ligament46, Interfaces_Ligament47, Interfaces_Ligament48, Interfaces_Ligament49, Interfaces_Ligament50, Interfaces_Ligament51, Interfaces_Ligament52, Interfaces_Ligament53, Interfaces_Ligament54, Interfaces_Ligament55, Interfaces_Ligament56, Interfaces_Ligament57, Interfaces_Ligament58, Interfaces_Ligament59, Interfaces_VitreousHumor0, Interfaces_VitreousHumor1, Interfaces_VitreousHumor2, Interfaces_VitreousHumor3, Interfaces_VitreousHumor4, Interfaces_VitreousHumor5, Interfaces_VitreousHumor6, Interfaces_VitreousHumor7, Interfaces_VitreousHumor8, Interfaces_VitreousHumor9, Interfaces_VitreousHumor10, Interfaces_VitreousHumor11, Interfaces_VitreousHumor12, Interfaces_VitreousHumor13, Interfaces_VitreousHumor14, Interfaces_VitreousHumor15, Interfaces_VitreousHumor16, Interfaces_VitreousHumor17, Interfaces_VitreousHumor18, Interfaces_VitreousHumor19, Interfaces_VitreousHumor20, Interfaces_VitreousHumor21, Interfaces_VitreousHumor22, Interfaces_VitreousHumor23, Interfaces_VitreousHumor24, Interfaces_VitreousHumor25, Interfaces_VitreousHumor26, Interfaces_VitreousHumor27, Interfaces_VitreousHumor28, Interfaces_VitreousHumor29, Interfaces_VitreousHumor30, Interfaces_VitreousHumor31, Interfaces_VitreousHumor32, Interfaces_VitreousHumor33, Interfaces_VitreousHumor34, Interfaces_VitreousHumor35, Interfaces_VitreousHumor36, Interfaces_VitreousHumor37, Interfaces_VitreousHumor38, Interfaces_VitreousHumor39, Interfaces_VitreousHumor40, Interfaces_VitreousHumor41])
    Solid_1 = geompy.MakeSolid([Shell_1])
    return Solid_1

def build_vitreous_humor(geompy, lens, aqueousHumor, retina, iris, choroid):

    Faces_lens = geompy.ExtractShapes(lens, geompy.ShapeType["FACE"], True)
    Faces_aqueousHumor = geompy.ExtractShapes(aqueousHumor, geompy.ShapeType["FACE"], True)
    Faces_iris = geompy.ExtractShapes(iris, geompy.ShapeType["FACE"], True)
    Faces_choroid = geompy.ExtractShapes(choroid, geompy.ShapeType["FACE"], True)
    Faces_retina = geompy.ExtractShapes(retina, geompy.ShapeType["FACE"], True)

    print(len(Faces_lens) + len(Faces_aqueousHumor) + len(Faces_iris) + len(Faces_choroid) + len(Faces_retina))

    ShellNewVitreousHumor = geompy.MakeShell( [Faces_lens[26], Faces_lens[27], Faces_lens[28], Faces_lens[29],
        Faces_aqueousHumor[99], Faces_aqueousHumor[101], Faces_aqueousHumor[102], Faces_aqueousHumor[105], Faces_aqueousHumor[106], Faces_aqueousHumor[111], Faces_aqueousHumor[112], Faces_aqueousHumor[113], Faces_aqueousHumor[114], Faces_aqueousHumor[123], Faces_aqueousHumor[124], Faces_aqueousHumor[127], Faces_aqueousHumor[129], Faces_aqueousHumor[144], Faces_aqueousHumor[145], Faces_aqueousHumor[146], Faces_aqueousHumor[147], Faces_aqueousHumor[151], Faces_aqueousHumor[153], Faces_aqueousHumor[154], Faces_aqueousHumor[155], Faces_aqueousHumor[156], Faces_aqueousHumor[157], Faces_aqueousHumor[162], Faces_aqueousHumor[163], Faces_aqueousHumor[165], Faces_aqueousHumor[167], Faces_aqueousHumor[174], Faces_aqueousHumor[175], Faces_aqueousHumor[177], Faces_aqueousHumor[178], Faces_aqueousHumor[179], Faces_aqueousHumor[180], Faces_aqueousHumor[181], Faces_aqueousHumor[182], Faces_aqueousHumor[183], Faces_aqueousHumor[184], Faces_aqueousHumor[185], Faces_aqueousHumor[186], Faces_aqueousHumor[187], Faces_aqueousHumor[188], Faces_aqueousHumor[189],
        Faces_iris[114], Faces_iris[122],
        Faces_choroid[1], Faces_choroid[2], Faces_choroid[3], Faces_choroid[5], # 1,5 ??
        Faces_retina[2], Faces_retina[3], Faces_retina[6], Faces_retina[7]
        ] )
    VitreousHumor = geompy.MakeSolid([ShellNewVitreousHumor])

    return VitreousHumor
