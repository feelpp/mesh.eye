import feelpp.core as fppc
from feelpp.core.integrate  import integrate
import sys, os
from .make_measures import load_mesh, compute_eye_volume, compute_domain_volume


if "Mr" in sys.argv:
    use_remeshed = True
else:
    use_remeshed = False

argv = ["measures"]
argv.append("--mesh.scale")
argv.append("1e-3")

current_dir = os.getcwd()

app = fppc.Environment(argv, config=fppc.localRepository("measures"))



def display_mesh_information(mesh):
    nelt = mesh.numGlobalElements()
    hmin = mesh.hMin()
    hmax = mesh.hMax()
    havg = mesh.hAverage()

    if fppc.Environment.isMasterRank():
        print(f"Number of elements: {nelt}")
        print(f"Min element size: {hmin}")
        print(f"Max element size: {hmax}")
        print(f"Avg element size: {havg}")

    return nelt, hmin, hmax, havg


Nelt = []
l = []

infos = []


for m in ["M0", "M1", "M2", "M3", "M4", "M5"]:
    mesh = load_mesh(m, current_dir, use_remeshed=use_remeshed)

    if True:

        Nelt.append(mesh.numGlobalElements())

        v = compute_eye_volume(mesh)
        l.append(v)

        vi = 0
        for d in ["AqueousHumor", "Choroid", "Cornea", "Iris", "Lamina", "Lens", "OpticNerve", "Retina", "Sclera", "VitreousHumor"]:
            vi += compute_domain_volume(mesh, d)

        if fppc.Environment.isMasterRank():
            print(f"Mesh: {m}")
            print(f"    Volume: {v}")
            print(f"    Sum of domain volumes: {vi}")
            print(f"    Error: {vi - v}")

    if False:
        mesh_infos = display_mesh_information(mesh)
        infos.append(mesh_infos)

dir_suffix = ["", "_r"][use_remeshed]

if fppc.Environment.isMasterRank():
    import pandas as pd
    print("Nelt:", Nelt)
    print("Volume:", l)
    df = pd.DataFrame({"Nelt": Nelt, "Volume": l})
    df.to_csv(f"volumes{dir_suffix}.csv", index=False)

if fppc.Environment.isMasterRank():
    import pandas as pd
    df = pd.DataFrame(infos, columns=["Nelt", "hmin", "hmax", "havg"])
    df.to_csv(f"mesh_infos{dir_suffix}.csv", index=False)
    print(df)