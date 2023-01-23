# Welcome-project

## Описание

В данном репозитории реализован алгоритм, который преобразует входные данные в
виде списка кортежей из строк с методом и путем HTTP-запроса в древовидный
словарь, который строит иерархию методов API. Кодовая база также покрыта
тестами.

*Принцип работы следующий*:
1. Функциональность алгоритма обернута в класс `WelcomeProject`, в котором есть
метод `run` для запуска алгоритма. Также он содержит поле со словарем `data`.
2. Метод `run` проверяет данные, и если данные корректные, то вызывается метод
`handle` для обработки данных.
3. Метод `handle`, предварительно создав словарь `current_dict`, итерируется по
всем элементам списка кортежей, делит кортеж на метод и путь. Из пути удаляются
лишние части - параметры в фигурных скобках, а также версия API.
4. Далее, из данной строки с токенами, разделенными слэшами, древовидная
структура вложенных словарей. Для этого, чтобы не городить много кода,
воспользовался библиотекой `dpath` и методом `new` из нее.
5. Обновляю словарь `data` - если запуск первый, то просто копируем данные из
обработчика в словарь, если последующий запуск, то происходит глубокое
обновление `data` текущим словарём.


## Использование

Для того, чтобы запустить программу, можно ее развернуть локально, или с
помощью Docker.

### Локально

```bash
python3 -m venv venv
source $WELCOME_PROJECT/venv/bin/activate
pip install pytest dpath
python $WELCOME_PROJECT/main.py
```

### В Docker

```bash
bash run.sh
```


## Запуск тестов:

### Локально

```bash
cd $WELCOME_PROJECT
pytest -v
```

### В Docker

```bash
bash run_tests.sh
```