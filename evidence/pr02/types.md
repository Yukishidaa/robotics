# Основные топики turtlesim

## `/turtle1/cmd_vel`

- Тип: `geometry_msgs/msg/Twist`.
- Назначение: команда линейной и угловой скорости черепашке.
- `linear.x`, `linear.y`, `linear.z` — линейная скорость по осям `x`, `y`, `z`;
  для движения вперёд используется `linear.x`.
- `angular.x`, `angular.y`, `angular.z` — угловая скорость вокруг осей `x`, `y`,
  `z`; для поворота в плоскости используется `angular.z`.

## `/turtle1/pose`

- Тип: `turtlesim_msgs/msg/Pose` (по выводу команды в среде ROS 2 Lyrical).
- Назначение: текущее положение, ориентация и скорости черепашки.
- Поля: `x`, `y` — координаты; `theta` — угол поворота;
  `linear_velocity` — линейная скорость; `angular_velocity` — угловая скорость.

Тип позы проверен командой:

```bash
ros2 topic list -t | grep '/turtle1/pose'
```
