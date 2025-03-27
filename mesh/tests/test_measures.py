import feelpp.core as fppc
from feelpp.core.integrate  import integrate
import sys, os

TOLERANCE = 1e-10


def load_mesh(name, current_dir, use_remeshed=False):
    dir_suffix = ["", "r"][use_remeshed]
    mesh_path = os.path.join(current_dir, f"M{dir_suffix}", name, fppc.Environment.expand(f"Eye_Mesh3D_p$np.json"))
    # print(f"load mesh {mesh_path}")
    m = fppc.mesh(dim=3, realdim=3)
    mesh = fppc.load(m, mesh_path, verbose=False)

    return mesh

def compute_eye_volume(mesh):
    v = integrate(range=fppc.elements(mesh), expr="1")[0]
    return v

def compute_domain_volume(mesh, domain):
    elts = fppc.markedelements(mesh, domain)
    v = integrate(range=elts, expr="1")[0]
    return v


def test_main_meshed(current_dir):

    mesh_path = os.path.join(current_dir, "Eye_Mesh3D.msh")
    mesh_r_path = os.path.join(current_dir, "Eye_Mesh3D_r.json")

    m = fppc.mesh(dim=3, realdim=3)

    for path in [mesh_path, mesh_r_path]:

        if fppc.Environment.isMasterRank():
            print(f"Dealing with mesh {path}")

        mesh = fppc.load(m, mesh_path, verbose=True)

        v = compute_eye_volume(mesh)

        vi = 0
        for d in ["AqueousHumor", "Choroid", "Cornea", "Iris", "Lamina", "Lens", "OpticNerve", "Retina", "Sclera", "VitreousHumor"]:
            vi += compute_domain_volume(mesh, d)
        if fppc.Environment.isMasterRank():
            print(f"    Volume of mesh {path}: {v}")
            print(f"    Sum of domain volumes: {vi}")

        assert( abs(v - vi) < TOLERANCE )




def test_volumes(mesh_list, current_dir, use_remeshed=False):

    for M in mesh_list:
        if fppc.Environment.isMasterRank():
            print(f"Testing mesh {M}")
        mesh = load_mesh(M, current_dir, use_remeshed=use_remeshed)

        v = compute_eye_volume(mesh)

        vi = 0
        for d in ["AqueousHumor", "Choroid", "Cornea", "Iris", "Lamina", "Lens", "OpticNerve", "Retina", "Sclera", "VitreousHumor"]:
            vi += compute_domain_volume(mesh, d)
        if fppc.Environment.isMasterRank():
            print(f"    Volume of mesh {M}: {v}")
            print(f"    Sum of domain volumes: {vi}")

        assert( abs(v - vi) < TOLERANCE )


if __name__ == "__main__":

    argv = ["test_measures"]
    argv.append("--mesh.scale")
    argv.append("1e-3")

    current_dir = os.getcwd()

    app = fppc.Environment(argv, config=fppc.localRepository("measures"))

    mesh_list = ["M0", "M1", "M2", "M3", "M4", "M5"]
    mesh_list_r = ["M0", "M1", "M2", "M3", "M4"]

    test_main_meshed(current_dir)
    if "only_main" in sys.argv:
        sys.exit(0)

    if "Mr" in sys.argv:
        test_volumes(mesh_list_r, current_dir, use_remeshed=True)
    else:
        test_volumes(mesh_list, current_dir, use_remeshed=False)