import sys, os
import feelpp.core as fppc
from colorama import Fore, Style

def load_mesh(mesh_file, dim=3):
    m = fppc.mesh(dim=dim, realdim=dim)
    mesh = fppc.load(m, mesh_file)
    return mesh

def remesh(old_mesh, metric):
    mesh, cpt = fppc.remesh(old_mesh, metric=metric)
    if fppc.Environment.isMasterRank(): print("Remeshing done in %d iterations" % cpt)
    return mesh

if __name__ == "__main__":

    cwd = os.getcwd()

    # sys.argv.append("--mesh.scale=1e-3")
    e = fppc.Environment(sys.argv, config=fppc.localRepository("remesh"))

    mesh = load_mesh("Eye_Mesh3D.msh", dim=3)

    for idx, r in enumerate(["10", "5", "1", "0.5", "0.25", "0.125"]):
        mesh_r = remesh(mesh, r)

        if fppc.Environment.isMasterRank():
            print(Fore.BLUE, f"M{idx} with metric {r}", Style.RESET_ALL)
            print(f"       hMin          hAverage      hMax")
            print(f"  Mesh {mesh.hMin():e}, {mesh.hAverage():e}, {mesh.hMax():e}")
            print(f"ReMesh {mesh_r.hMin():e}, {mesh_r.hAverage():e}, {mesh_r.hMax():e}")

        export_dir = os.path.join(cwd, "M", f"M{idx}")
        if fppc.Environment.isMasterRank() and not os.path.exists(export_dir):
            os.makedirs(export_dir)
        mesh_r.saveHDF5(os.path.join(export_dir, "Eye_Mesh3D.json"))
