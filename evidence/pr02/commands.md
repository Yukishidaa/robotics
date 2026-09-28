# PR02: разбор команд Linux

## Основные команды

### `mkdir -p`

```bash
mkdir -p src/turtle_bringup/launch
ls -R src
```

Создаёт всю цепочку каталогов; `-p` не сообщает об ошибке, если каталог уже
существует.

### `>`, `2>&1`

```bash
colcon build > build.txt 2>&1
```

`>` направляет stdout в файл и заменяет его содержимое, а `2>&1` направляет
stderr туда же. Поэтому сохраняется полный вывод сборки.

### `|`, `tee`

```bash
colcon build 2>&1 | tee build.txt
```

`|` передаёт вывод следующей команде, а `tee` одновременно показывает его в
терминале и записывает в файл.

### `>` и `|`

`ls > files.txt` записывает результат в файл без показа в терминале; `ls | wc -l`
передаёт результат другой команде и считает строки.

### `source`

```bash
source /opt/ros/lyrical/setup.bash
export ROS_DOMAIN_ID=16
printenv ROS_DOMAIN_ID ROS_DISTRO
```

`source` выполняет setup в текущем shell, поэтому окружение ROS сохраняется.
`bash setup.bash` запускает дочерний shell, и его изменения после завершения
теряются.

## Проверка launch

```bash
ros2 launch turtle_bringup sim.launch.py
ros2 node list --no-daemon --spin-time 2
```

Ожидаемый узел: `/turtlesim`. Запуск останавливается сочетанием `Ctrl+C`.

## Ошибка имени topic

### До: проверка топиков и их типов

```bash
ros2 topic list -t
ros2 interface show geometry_msgs/msg/Twist
ros2 interface list | grep -E 'turtlesim(_msgs)?/msg/Pose'
```

Результат для запущенного `turtlesim`:

```text
/turtle1/cmd_vel [geometry_msgs/msg/Twist]
/turtle1/pose    [turtlesim_msgs/msg/Pose]
```

### Сбой: правильный тип, неправильное имя

```bash
ros2 topic pub --rate 1 --wait-matching-subscriptions 0 \
  /cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 1.0}, angular: {z: 0.5}}'
ros2 topic info /cmd_vel --verbose
```

Существенный вывод:

```text
Type: geometry_msgs/msg/Twist
Publisher count: 1
Subscription count: 0
```

Публикация технически создана, но у `/cmd_vel` нет подписчика `turtlesim`.
Поэтому черепашка не получает команду и не движется.

### После: исправлено имя topic

```bash
ros2 topic pub --rate 1 --wait-matching-subscriptions 0 \
  /turtle1/cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 1.0}, angular: {z: 0.5}}'
ros2 topic info /turtle1/cmd_vel --verbose
```

Существенный вывод:

```text
Type: geometry_msgs/msg/Twist
Publisher count: 1
Subscription count: 1
Subscription: /turtlesim
```

После исправления имя и тип совпадают с подпиской `turtlesim`, поэтому команда
скорости доходит до узла и черепашка движется.

### Почему одного правильного типа недостаточно

Тип `geometry_msgs/msg/Twist` определяет только структуру сообщения: поля
`linear` и `angular`, каждое из которых содержит `x`, `y` и `z`. Соединение в
ROS 2 происходит по полному имени topic и типу одновременно. В публикации на
`/cmd_vel` тип был правильным, но имя отличалось от `/turtle1/cmd_vel`, поэтому
подписчик `turtlesim` не был найден. Правильны должны быть и имя topic, и тип
сообщения (а также совместимые QoS).
