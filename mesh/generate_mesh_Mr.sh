
NP=12
PWD=$(pwd)
MESH_R_NAME=Eye_Mesh3D_r

# NB: Actually, there is no need to run a realistic simulation, we just use the MeshAdaptation tool provided by the toolboxes
# But to actually obtain the adapted mesh saved on the disk, we need to run this simulation in parallel.
mpirun -np ${NP} feelpp_toolbox_heat --config-file refinement_aqueous_humor.cfg --directory ${PWD}/feelppdb/mesh


# The adapted mesh is saved in the folder ${PWD}/feelppdb/mesh/meshes/tmp
# we retreive this mesh and save it in the current folder
mv ${PWD}/feelppdb/mesh/np_${NP}/meshes/tmp/mesh_o.h5 ${PWD}/${MESH_R_NAME}.h5
mv ${PWD}/feelppdb/mesh/np_${NP}/meshes/tmp/mesh_o.json ${PWD}/${MESH_R_NAME}.json

sed -i 's/mesh_o/${MESH_R_NAME}/g' ${MESH_R_NAME}.json