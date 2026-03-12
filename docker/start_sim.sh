#!/bin/bash
echo "=== Starting G1 Simulation ==="
echo ""
echo "This will open TWO windows:"
echo "  1. MuJoCo viewer (3D robot)"
echo "  2. This terminal becomes the control panel"
echo ""
echo "Press Enter to start..."
read

# Start simulator in background
cd ~/unitree_mujoco/simulate_python
python3 unitree_mujoco.py &
SIM_PID=$!

# Wait for simulator to initialize
sleep 3

# Start control panel
cd ~/g1_mop_project
python3 g1_team_demo.py

# Clean up
kill $SIM_PID 2>/dev/null
