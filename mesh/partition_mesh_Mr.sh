#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

PWD=$(pwd)

for MESH_INDEX in M0 M1 M2 M3 M4 M5
do
    echo "Partitioning mesh ${MESH_INDEX}..."
    echo "PWD: ${PWD}"

    feelpp_mesh_partitioner --ifile ${PWD}/Mr/${MESH_INDEX}/Eye_Mesh3D.json \
        --odir ${PWD}/Mr/${MESH_INDEX} \
        --json ${PWD}/meshpartitionner_Mr.json
done
