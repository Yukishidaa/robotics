# Дерево tf2 — PR06

Каждая строка описывает одну связь: `родитель → ребёнок` (тип соединения, владелец публикации).

| Родитель | Ребёнок | Тип соединения | Владелец публикации | Ожидаемое преобразование |
|----------|---------|----------------|---------------------|--------------------------|
| base_link | camera_link | fixed | robot_state_publisher | xyz=(0.25, 0.0, 0.12), rpy=(0, 0, 0) |
| base_link | lidar_link | fixed | robot_state_publisher | xyz=(0.15, 0.0, 0.22), rpy=(0, 0, 0) |
| base_link | imu_link | fixed | robot_state_publisher | xyz=(0.0, 0.0, 0.18), rpy=(0, 0, 0) |
| base_link | wheel_left_front_link | continuous | joint_states (опционально) | xyz=(0.25, 0.225, -0.08), rpy=(0, 1.5708, 0) |
| base_link | wheel_right_front_link | continuous | joint_states (опционально) | xyz=(0.25, -0.225, -0.08), rpy=(0, 1.5708, 0) |
| base_link | wheel_left_rear_link | continuous | joint_states (опционально) | xyz=(-0.25, 0.225, -0.08), rpy=(0, 1.5708, 0) |
| base_link | wheel_right_rear_link | continuous | joint_states (опционально) | xyz=(-0.25, -0.225, -0.08), rpy=(0, 1.5708, 0) |

## Выводы
- Все фиксированные звенья публикуются `robot_state_publisher` в `/tf_static`.
- Каждая связь имеет ровно одного владельца публикации.
- Дерево связное и ацикличное, корень — `base_link`.
