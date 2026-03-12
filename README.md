# G1 Mop Project

Unitree G1 humanoid robot simulation and control for floor mopping task.

## Setup

### 1. Install base software (one-time)
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev cmake g++ git

python3.10 -m venv ~/unitree_env
source ~/unitree_env/bin/activate

cd ~
git clone https://github.com/eclipse-cyclonedds/cyclonedds.git
cd cyclonedds && mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
make -j$(nproc) && sudo make install
echo 'export CYCLONEDDS_HOME=/usr/local' >> ~/.bashrc
export CYCLONEDDS_HOME=/usr/local

cd ~
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git
cd unitree_sdk2_python && pip install -e .

pip install mujoco pygame
cd ~
git clone https://github.com/unitreerobotics/unitree_mujoco.git
```

### 2. Clone this repo and run setup
```bash
cd ~
git clone https://github.com/shayanitami/g1_mop_project.git
cd g1_mop_project
./setup_simulation.sh
```

### 3. Run
Terminal 1 - Simulator:
```bash
source ~/unitree_env/bin/activate
cd ~/unitree_mujoco/simulate_python
python unitree_mujoco.py
```

Terminal 2 - Control Panel:
```bash
source ~/unitree_env/bin/activate
python ~/g1_mop_project/g1_team_demo.py
```

## Commands
| Command | Description |
|---------|-------------|
| `zero` | Default pose |
| `arms_up` | Both arms raised |
| `arms_forward` | Arms reaching forward |
| `mop_hold` | Mop holding posture |
| `wave_left` | Left arm wave position |
| `look_left` / `look_right` | Turn waist |
| `bow` | Bow forward |
| `mop` | Continuous sweep animation |
| `wave` | Continuous wave animation |
| `stop` | Stop animation |
| `joint <name> <degrees>` | Set one joint |
| `joints` | Show all joint angles |
