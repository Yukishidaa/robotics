# Robotics course

## PR01

### Environment

```bash
source /opt/ros/lyrical/setup.bash
export ROS_DOMAIN_ID=16
```

### Run

In terminal A:

```bash
ros2 run turtlesim turtlesim_node
```

In terminal B:

```bash
ros2 run turtlesim turtle_teleop_key
```

In terminal C, run the observation commands documented in
`evidence/pr01/graph.md`.

The PR01 evidence contains the graph inspection, pose frequency measurement,
ROS domain failure reproduction, recovery check, and environment report.

### Checker

```bash
python3 .course-kit/v1/tools/check_practice.py PR01 --submission .
```
