# PR01: окружение и граф ROS 2

## Запуск

В каждом из трёх терминалов:

```bash
source /opt/ros/lyrical/setup.bash
export ROS_DOMAIN_ID=16
```

Терминал A, симулятор:

```bash
ros2 run turtlesim turtlesim_node
```

Терминал B, управление:

```bash
ros2 run turtlesim turtle_teleop_key
```

Терминал C, наблюдение:

```bash
ros2 node list --no-daemon --spin-time 2
ros2 topic list -t
ros2 node info /turtlesim
ros2 topic type /turtle1/pose
POSE_TYPE=$(ros2 topic type /turtle1/pose)
ros2 topic echo /turtle1/pose --once
ros2 topic hz /turtle1/pose
```

Измерение частоты выполнялось 20 секунд. Средняя частота публикации
`/turtle1/pose` составила 62.5 Гц.

## Проверка разрыва связи

Симулятор оставался в домене 16. После перезапуска `turtle_teleop_key` и
наблюдения в домене 17 симулятор не обнаруживался, поза не приходила, а
команда завершалась с кодом 124 по таймауту. Результат сохранён в
`pose-broken.txt`.

После возврата teleop и наблюдения в домен 16 поза снова стала доступна, а
команда завершилась с кодом 0. Результат сохранён в `pose-fixed.txt`.

Подробные команды, вывод графа и объяснение причины находятся в `graph.md`.
Сведения об окружении находятся в `environment.json` и `doctor.txt`.

## Проверка checker

```bash
python3 .course-kit/v1/tools/check_practice.py PR01 --submission .
```
