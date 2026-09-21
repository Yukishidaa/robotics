## Пункт 2
### ros2 node list --no-daemon --spin-time 2
Ничего не выводит
### ros2 topic list -t
/parameter_events [rcl_interfaces/msg/ParameterEvent]
/rosout [rcl_interfaces/msg/Log]
/turtle1/cmd_vel [geometry_msgs/msg/Twist]
/turtle1/color_sensor [turtlesim_msgs/msg/Color]
/turtle1/pose [turtlesim_msgs/msg/Pose]
### os2 node info /turtlesim
/turtlesim
  Subscribers:
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /turtle1/cmd_vel: geometry_msgs/msg/Twist
  Publishers:
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /rosout: rcl_interfaces/msg/Log
    /turtle1/color_sensor: turtlesim_msgs/msg/Color
    /turtle1/pose: turtlesim_msgs/msg/Pose
  Service Servers:
    /clear: std_srvs/srv/Empty
    /kill: turtlesim_msgs/srv/Kill
    /reset: std_srvs/srv/Empty
    /spawn: turtlesim_msgs/srv/Spawn
    /turtle1/set_pen: turtlesim_msgs/srv/SetPen
    /turtle1/teleport_absolute: turtlesim_msgs/srv/TeleportAbsolute
    /turtle1/teleport_relative: turtlesim_msgs/srv/TeleportRelative
    /turtlesim/describe_parameters: rcl_interfaces/srv/DescribeParameters
    /turtlesim/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
    /turtlesim/get_parameters: rcl_interfaces/srv/GetParameters
    /turtlesim/get_type_description: type_description_interfaces/srv/GetTypeDescription
    /turtlesim/list_parameters: rcl_interfaces/srv/ListParameters
    /turtlesim/set_parameters: rcl_interfaces/srv/SetParameters
    /turtlesim/set_parameters_atomically: rcl_interfaces/srv/SetParametersAtomically
  Service Clients:

  Action Servers:
    /turtle1/rotate_absolute: turtlesim_msgs/action/RotateAbsolute
  Action Clients:
### ros2 topic type /turtle1/pose
turtlesim_msgs/msg/Pose
### POSE_TYPE=$(ros2 topic type /turtle1/pose)
Ничего не выводит, создаёт перменную
### ros2 topic echo /turtle1/pose --once
x: 5.820490837097168
y: 1.8031871318817139
theta: 2.6656293869018555
linear_velocity: 0.0
angular_velocity: 0.0
### ros2 topic hz /turtle1/pose
average rate: 62.496
	min: 0.015s max: 0.017s std dev: 0.00048s window: 61
average rate: 62.495
	min: 0.015s max: 0.017s std dev: 0.00048s window: 124
average rate: 62.491
	min: 0.015s max: 0.017s std dev: 0.00047s window: 186
average rate: 62.491
	min: 0.015s max: 0.017s std dev: 0.00047s window: 249
average rate: 62.503
	min: 0.015s max: 0.017s std dev: 0.00047s window: 311
average rate: 62.498
	min: 0.015s max: 0.017s std dev: 0.00047s window: 374
average rate: 62.502
	min: 0.015s max: 0.017s std dev: 0.00047s window: 437
average rate: 62.497
	min: 0.015s max: 0.017s std dev: 0.00048s window: 499
average rate: 62.501
	min: 0.015s max: 0.017s std dev: 0.00048s window: 562
average rate: 62.501
	min: 0.015s max: 0.017s std dev: 0.00048s window: 624
average rate: 62.497
	min: 0.015s max: 0.017s std dev: 0.00047s window: 687
average rate: 62.498
	min: 0.015s max: 0.017s std dev: 0.00048s window: 749
average rate: 62.501
	min: 0.015s max: 0.017s std dev: 0.00048s window: 812
average rate: 62.498
	min: 0.015s max: 0.017s std dev: 0.00048s window: 874
average rate: 62.500
	min: 0.015s max: 0.017s std dev: 0.00048s window: 937
average rate: 62.499
	min: 0.015s max: 0.017s std dev: 0.00048s window: 999
average rate: 62.500
	min: 0.015s max: 0.017s std dev: 0.00048s window: 1062
average rate: 62.500
	min: 0.015s max: 0.017s std dev: 0.00048s window: 1125
average rate: 62.499
	min: 0.015s max: 0.017s std dev: 0.00048s window: 1187
average rate: 62.500
	min: 0.015s max: 0.017s std dev: 0.00048s window: 1250

**Замер длился 20 секунд, в среднем частота 62.5 гц.**
## Пункт 3
### До
Во всех трёх окнах домен был равен 16.
Код возврата был 0, потому что черепаха корректно записывала данные в топик и timeout не успел вмешаться в работу команды.
### Сбой
Терминал A был в домене 16, B C в 17.
Код возврата был 124, потому что черепаха записывала данные в другом домене, то есть subscriber не видел эти данные и завершился с помощью timeout.
### После
Все терминалы снова стали находиться в одном домене, в следствие чего код возврата снова стал равен 0, то есть команда успешно завершилась, приняв данные в топике от черепашки.


Перезапуск turtle_teleop_key потребовался, так как эта нода является активным Издателем (Publisher), который напрямую считывает ввод с клавиатуры и может терять фокус или «залипать» в определенном состоянии.
Перезапуск симулятора  не требовался, потому что благодаря архитектуре Pub/Sub (Издатель/Подписчик) нода-симулятор полностью изолирована от источника команд. Ей неважно, кто публикует данные в топик /turtle1/cmd_vel, поэтому сбои или перезапуски пульта управления никак не влияют на её работу. Настройка ROS является фоновой переменной окружения и не требует перезапуска при работе с нодами.
