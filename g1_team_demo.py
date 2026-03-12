import time
import numpy as np
import threading
from unitree_sdk2py.core.channel import ChannelPublisher, ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.default import unitree_hg_msg_dds__LowCmd_
from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowCmd_, LowState_
from unitree_sdk2py.utils.crc import CRC

G1_NUM_MOTOR = 29

JOINTS = {
    "left_hip_pitch": 0, "left_hip_roll": 1, "left_hip_yaw": 2,
    "left_knee": 3, "left_ankle_pitch": 4, "left_ankle_roll": 5,
    "right_hip_pitch": 6, "right_hip_roll": 7, "right_hip_yaw": 8,
    "right_knee": 9, "right_ankle_pitch": 10, "right_ankle_roll": 11,
    "waist_yaw": 12, "waist_roll": 13, "waist_pitch": 14,
    "left_shoulder_pitch": 15, "left_shoulder_roll": 16,
    "left_shoulder_yaw": 17, "left_elbow": 18,
    "left_wrist_roll": 19, "left_wrist_pitch": 20, "left_wrist_yaw": 21,
    "right_shoulder_pitch": 22, "right_shoulder_roll": 23,
    "right_shoulder_yaw": 24, "right_elbow": 25,
    "right_wrist_roll": 26, "right_wrist_pitch": 27, "right_wrist_yaw": 28,
}

target_q = np.zeros(G1_NUM_MOTOR)
Kp = np.array([
    60,60,60,100,40,40, 60,60,60,100,40,40,
    60,40,40,
    40,40,40,40,40,40,40, 40,40,40,40,40,40,40
], dtype=float)
Kd = np.array([
    1.5,1.5,1.5,2,1,1, 1.5,1.5,1.5,2,1,1,
    1.5,1,1,
    1,1,1,1,1,1,1, 1,1,1,1,1,1,1
], dtype=float)

def _set_joints(joint_dict):
    pose = np.zeros(G1_NUM_MOTOR)
    for name, val in joint_dict.items():
        pose[JOINTS[name]] = val
    return pose

POSES = {
    "zero": np.zeros(G1_NUM_MOTOR),
    "arms_up": lambda: _set_joints({"left_shoulder_pitch": -1.5, "right_shoulder_pitch": -1.5}),
    "arms_forward": lambda: _set_joints({"left_shoulder_pitch": -1.0, "right_shoulder_pitch": -1.0,
                                          "left_elbow": -0.5, "right_elbow": -0.5}),
    "wave_left": lambda: _set_joints({"left_shoulder_pitch": -1.5, "left_shoulder_roll": 0.5,
                                       "left_elbow": -1.0}),
    "mop_hold": lambda: _set_joints({"left_shoulder_pitch": -0.6, "right_shoulder_pitch": -0.6,
                                      "left_elbow": -0.8, "right_elbow": -0.8,
                                      "left_shoulder_roll": 0.2, "right_shoulder_roll": -0.2}),
    "look_left": lambda: _set_joints({"waist_yaw": 0.5}),
    "look_right": lambda: _set_joints({"waist_yaw": -0.5}),
    "bow": lambda: _set_joints({"waist_pitch": 0.3,
                                 "left_shoulder_pitch": 0.3, "right_shoulder_pitch": 0.3}),
}

animation_active = False
animation_func = None

def mop_sweep_animation(t):
    sweep = 0.4 * np.sin(2.0 * np.pi * 0.5 * t)
    return _set_joints({
        "left_shoulder_pitch": -0.6, "right_shoulder_pitch": -0.6,
        "left_elbow": -0.8, "right_elbow": -0.8,
        "left_shoulder_roll": 0.2 + sweep * 0.3,
        "right_shoulder_roll": -0.2 + sweep * 0.3,
        "waist_yaw": sweep * 0.3,
        "left_wrist_yaw": sweep * 0.5,
        "right_wrist_yaw": sweep * 0.5,
    })

def wave_animation(t):
    wave = 0.5 * np.sin(2.0 * np.pi * 2.0 * t)
    return _set_joints({
        "left_shoulder_pitch": -1.5,
        "left_shoulder_roll": 0.5,
        "left_elbow": -1.0 + wave * 0.3,
        "left_wrist_yaw": wave,
    })

ANIMATIONS = {"mop": mop_sweep_animation, "wave": wave_animation}

def control_loop(pub, low_state, cmd, crc):
    global target_q, animation_active, animation_func
    anim_start = time.time()
    while True:
        if low_state[0] is None:
            time.sleep(0.01)
            continue
        if animation_active and animation_func:
            t = time.time() - anim_start
            target_q = animation_func(t)
        cmd.mode_pr = 0
        cmd.mode_machine = low_state[0].mode_machine
        for i in range(G1_NUM_MOTOR):
            cmd.motor_cmd[i].mode = 1
            cmd.motor_cmd[i].tau = 0.0
            cmd.motor_cmd[i].kp = Kp[i]
            cmd.motor_cmd[i].kd = Kd[i]
            cmd.motor_cmd[i].dq = 0.0
            cmd.motor_cmd[i].q = float(target_q[i])
        cmd.crc = crc.Crc(cmd)
        pub.Write(cmd)
        time.sleep(0.002)

if __name__ == "__main__":
    ChannelFactoryInitialize(0, "lo")
    pub = ChannelPublisher("rt/lowcmd", LowCmd_)
    pub.Init()
    low_state = [None]
    sub = ChannelSubscriber("rt/lowstate", LowState_)
    sub.Init(lambda msg: low_state.__setitem__(0, msg), 10)
    cmd = unitree_hg_msg_dds__LowCmd_()
    crc = CRC()

    print("Waiting for simulator connection...")
    while low_state[0] is None:
        time.sleep(0.1)
    print("Connected!\n")

    ctrl_thread = threading.Thread(target=control_loop, args=(pub, low_state, cmd, crc), daemon=True)
    ctrl_thread.start()

    print("=" * 50)
    print("  G1 TEAM CONTROL PANEL")
    print("=" * 50)
    print()
    print("POSES:  zero | arms_up | arms_forward | mop_hold")
    print("        wave_left | look_left | look_right | bow")
    print()
    print("ANIMATIONS:  mop | wave | stop")
    print()
    print("CUSTOM:  joint <name> <degrees>")
    print("         Example: joint left_elbow -45")
    print()
    print("OTHER:   joints (list all) | quit")
    print("=" * 50)

    while True:
        try:
            user = input("\n> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break
        if user == "quit":
            break
        elif user == "stop":
            animation_active = False
            print("Animation stopped.")
        elif user == "joints":
            for name, idx in sorted(JOINTS.items(), key=lambda x: x[1]):
                current = low_state[0].motor_state[idx].q if low_state[0] else 0
                print(f"  [{idx:2d}] {name:25s} = {np.degrees(current):7.1f} deg")
        elif user in POSES:
            animation_active = False
            val = POSES[user]
            target_q = val() if callable(val) else val.copy()
            print(f"Pose: {user}")
        elif user in ANIMATIONS:
            animation_func = ANIMATIONS[user]
            animation_active = True
            print(f"Animation: {user} (type 'stop' to end)")
        elif user.startswith("joint "):
            parts = user.split()
            if len(parts) == 3 and parts[1] in JOINTS:
                try:
                    angle_deg = float(parts[2])
                    animation_active = False
                    target_q[JOINTS[parts[1]]] = np.radians(angle_deg)
                    print(f"Set {parts[1]} to {angle_deg} deg")
                except ValueError:
                    print("Invalid angle")
            else:
                print(f"Unknown joint. Type 'joints' to see all names.")
        else:
            print("Unknown command. Type a pose name, animation, or 'joints'.")
