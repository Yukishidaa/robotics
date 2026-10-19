# PR03: первая нода `patrol`

## Запуск

В трёх терминалах подключается ROS 2 Lyrical и workspace:

```bash
source /opt/ros/lyrical/setup.bash
source install/setup.bash
```

В терминале A запускается симулятор:

```bash
ros2 run turtlesim turtlesim_node
```

В терминале B сначала запускается нода с намеренной ошибкой:

```bash
ros2 run patrol patrol
```

Затем исправный вариант запускается с remap:

```bash
ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel
```

## Что сделано в ноде

`Patrol.__init__` выполняет инициализацию ROS-ноды, создаёт подписку на
`/turtle1/pose`, publisher `geometry_msgs/msg/Twist` и таймер с периодом
`0.1` секунды. Подписка сохранена в поле `pose_subscription`, поэтому она
остаётся активной всё время жизни объекта.

`pose_callback` вызывается при каждом сообщении позы и сохраняет последнее
сообщение в `last_pose`. Сам callback не вычисляет движение и не публикует
команду.

`timer_callback` вызывается таймером и публикует результат чистой функции
`command_for_pose`. Пока поза ещё не пришла, публикуется нулевой `Twist`.
После получения позы публикуются `linear.x = 0.5` и `angular.z = 0.3`; остальные
поля остаются нулевыми.

`rclpy.spin(node)` запускает обработку событий: сообщений позы, срабатываний
таймера и других callback. При `Ctrl+C` управление выходит из `spin`, затем в
`finally` публикуется нулевой `Twist`, уничтожается нода и вызывается
`rclpy.shutdown()`.

## До ошибки

Команда публикует в относительный topic `cmd_vel`. Для ноды с namespace `/`
это имя `/cmd_vel`, а `turtlesim` слушает `/turtle1/cmd_vel`.

```text
ros2 topic info /cmd_vel --verbose
Type: geometry_msgs/msg/Twist
Publisher count: 1
Subscription count: 0
```

Тип сообщения правильный, но полного совпадения имени topic нет, поэтому
команда до `turtlesim` не доходит.

## После исправления

Remap `cmd_vel:=/turtle1/cmd_vel` соединяет publisher с подписчиком симулятора:

```text
ros2 topic info /turtle1/cmd_vel --verbose
Type: geometry_msgs/msg/Twist
Publisher count: 1
Subscription count: 1
Node name: turtlesim
```

Проверка частоты за несколько секунд дала:

```text
average rate: 9.998
average rate: 9.997
min: 0.099s max: 0.101s
```

Это соответствует требуемому периоду `0.1` секунды и примерно `10 Гц`.

