FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV CYCLONEDDS_HOME=/usr/local

RUN apt-get update && apt-get install -y \
    python3.10 python3.10-venv python3.10-dev python3-pip \
    cmake g++ git libgl1-mesa-glx libgl1-mesa-dri \
    libglfw3 libglfw3-dev libegl1-mesa-dev \
    libxrandr2 libxinerama1 libxcursor1 libxi6 \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

WORKDIR /root

RUN git clone https://github.com/eclipse-cyclonedds/cyclonedds.git && \
    cd cyclonedds && mkdir build && cd build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local && \
    make -j$(nproc) && make install && \
    cd /root && rm -rf cyclonedds

RUN git clone https://github.com/unitreerobotics/unitree_sdk2_python.git && \
    cd unitree_sdk2_python && pip3 install -e .

RUN pip3 install mujoco pygame numpy

RUN git clone https://github.com/unitreerobotics/unitree_mujoco.git

# Create fixed scene (robot bolted to ground)
RUN cp /root/unitree_mujoco/unitree_robots/g1/g1_29dof.xml \
       /root/unitree_mujoco/unitree_robots/g1/g1_29dof_fixed.xml && \
    sed -i '/<joint name="floating_base_joint"/d' \
       /root/unitree_mujoco/unitree_robots/g1/g1_29dof_fixed.xml

COPY scene_fixed.xml /root/unitree_mujoco/unitree_robots/g1/scene_fixed.xml
COPY config.py /root/unitree_mujoco/simulate_python/config.py
COPY g1_team_demo.py /root/g1_mop_project/g1_team_demo.py
COPY start_sim.sh /root/start_sim.sh
RUN chmod +x /root/start_sim.sh

WORKDIR /root
CMD ["/bin/bash"]
