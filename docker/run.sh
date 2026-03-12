#!/bin/bash
echo "=== G1 Mop Project - Docker Launch ==="
echo ""

# Allow Docker to access your display
xhost +local:docker 2>/dev/null

# Check for NVIDIA GPU
if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA GPU detected - using GPU acceleration"
    GPU_FLAGS="--gpus all --runtime=nvidia -e NVIDIA_DRIVER_CAPABILITIES=all"
else
    echo "No NVIDIA GPU detected - using software rendering"
    GPU_FLAGS=""
fi

docker run -it --rm \
    --name g1_sim \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    $GPU_FLAGS \
    --network host \
    g1_mop_project

# Revoke display access when done
xhost -local:docker 2>/dev/null
