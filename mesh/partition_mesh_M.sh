#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

PWD=$(pwd)

for MESH_INDEX in M0 M1 M2 M3 M4 M5
do
    echo "Partitioning mesh ${MESH_INDEX}..."
    echo "PWD: ${PWD}"

    feelpp_mesh_partitioner --ifile ${PWD}/M/${MESH_INDEX}/Eye_Mesh3D.json \
        --odir ${PWD}/M/${MESH_INDEX} \
        --part 1 2 4 8 12
done
