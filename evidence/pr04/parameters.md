# PR04: параметризация движения

## Проверка параметров через ros2 param

### Исходное состояние (дефолты)

```bash
ros2 param get /patrol linear_speed
ros2 param get /patrol turn_rate
ros2 param get /patrol publish_hz
```

Результат:
```
Double value is: 0.5
Double value is: 0.3
Double value is: 10.0
```

### Изменение publish_hz 10 → 5 Гц (допустимое)

```bash
ros2 param set /patrol publish_hz 5.0
ros2 param get /patrol publish_hz
```

Результат:
```
Set parameter successful
Double value is: 5.0
```

Таймер пересоздан с периодом 0.2с, поток команд изменился.

### Попытка установить publish_hz = 0 (недопустимое)

```bash
ros2 param set /patrol publish_hz 0.0
```

Результат:
```
Setting parameter failed: publish_hz must be in [1, 30], got 0.0
```

Значение отклонено, старая частота (5.0) сохранена.

### Попытка установить publish_hz = -5 (недопустимое)

```bash
ros2 param set /patrol publish_hz -5.0
```

Результат:
```
Setting parameter failed: publish_hz must be in [1, 30], got -5.0
```

### Попытка установить publish_hz = NaN (недопустимое)

```bash
ros2 param set /patrol publish_hz nan
```

Результат:
```
Setting parameter failed: publish_hz must be a finite number, got nan
```

### Проверка границ linear_speed

```bash
ros2 param set /patrol linear_speed 0.0   # OK, граница
ros2 param set /patrol linear_speed 1.0   # OK, граница
ros2 param set /patrol linear_speed -0.1  # FAIL: linear_speed must be in [0, 1], got -0.1
ros2 param set /patrol linear_speed 1.5   # FAIL: linear_speed must be in [0, 1], got 1.5
```

### Проверка границ turn_rate

```bash
ros2 param set /patrol turn_rate -1.0  # OK, граница
ros2 param set /patrol turn_rate 1.0   # OK, граница
ros2 param set /patrol turn_rate -1.5  # FAIL: turn_rate must be in [-1, 1], got -1.5
ros2 param set /patrol turn_rate 1.5   # FAIL: turn_rate must be in [-1, 1], got 1.5
```

## Эмуляция дефекта (проверка отключена)

В коммите `312dab0` валидация `publish_hz` временно отключена:

```bash
# с отключённой проверкой
ros2 param set /patrol publish_hz 0.0
# Set parameter successful
# но таймер создаётся с периодом 1/0 → деление на ноль / бесконечность
```

После возврата проверки (коммит `51ccd7f`) ноль отклоняется, значение и поток остаются прежними.

## Действие поворота

```bash
ros2 service call /clear std_srvs/srv/Empty
ros2 action list -t | grep rotate_absolute
```

Результат:
```
/turtle1/rotate_absolute [turtlesim_msgs/action/RotateAbsolute]
```

**Отличие запроса (goal) и цели (action server):**
Запрос (goal) — это сообщение, которое клиент отправляет серверу, описывающее желаемое состояние (целевой угол). Цель (action server) — это серверная сущность, которая принимает запросы, выполняет длительную операцию с feedback и может быть отменена; она управляет состоянием выполнения и возвращает результат.
