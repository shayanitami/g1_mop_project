#!/bin/bash
echo "=== G1 Mop Project - Simulation Setup ==="

cp ~/unitree_mujoco/unitree_robots/g1/g1_29dof.xml ~/unitree_mujoco/unitree_robots/g1/g1_29dof_fixed.xml
sed -i '/<joint name="floating_base_joint"/d' ~/unitree_mujoco/unitree_robots/g1/g1_29dof_fixed.xml

cat > ~/unitree_mujoco/unitree_robots/g1/scene_fixed.xml << 'EOF'
<mujoco model="g1_29dof fixed scene">
  <include file="g1_29dof_fixed.xml"/>
  <statistic center="0 0 0.5" extent="2.0"/>
  <visual>
    <headlight diffuse="0.6 0.6 0.6" ambient="0.3 0.3 0.3" specular="0 0 0"/>
    <rgba haze="0.15 0.25 0.35 1"/>
    <global azimuth="-130" elevation="-20"/>
  </visual>
  <asset>
    <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512" height="3072"/>
    <texture type="2d" name="groundplane" builtin="checker" mark="edge" rgb1="0.2 0.3 0.4" rgb2="0.1 0.2 0.3"
      markrgb="0.8 0.8 0.8" width="300" height="300"/>
    <material name="groundplane" texture="groundplane" texuniform="true" texrepeat="5 5" reflectance="0.2"/>
  </asset>
  <worldbody>
    <light pos="0 0 3" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
  </worldbody>
</mujoco>
EOF

cat > ~/unitree_mujoco/simulate_python/config.py << 'EOF'
ROBOT = "g1"
ROBOT_SCENE = "../unitree_robots/" + ROBOT + "/scene_fixed.xml"
DOMAIN_ID = 0
INTERFACE = "lo"

USE_JOYSTICK = 0
JOYSTICK_TYPE = "xbox"
JOYSTICK_DEVICE = 0

PRINT_SCENE_INFORMATION = True
ENABLE_ELASTIC_BAND = False

SIMULATE_DT = 0.005
VIEWER_DT = 0.02
EOF

echo ""
echo "=== Setup complete! ==="
echo "Terminal 1: source ~/unitree_env/bin/activate && cd ~/unitree_mujoco/simulate_python && python unitree_mujoco.py"
echo "Terminal 2: source ~/unitree_env/bin/activate && python ~/g1_mop_project/g1_team_demo.py"
