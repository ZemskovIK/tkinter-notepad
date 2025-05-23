# Блокнот AmTCD+

**Блокнот AmTCD+** — это приложение для работы с зашифрованными текстовыми файлами. Программа использует алгоритм шифрования XOR для защиты данных, при этом ключи шифрования генерируются динамически и передаются вместе с зашифрованным текстом. Это приложение ориентировано на создание, открытие и сохранение зашифрованных файлов.

## Особенности

- **Прозрачное шифрование**: все данные, введённые в приложение, автоматически шифруются с использованием ключа шифрования.
- **Гибкость в управлении ключами**: первый ключ хранится в конфигурационном файле, а новый ключ генерируется автоматически при шифровании.
- **Поддержка зашифрованных файлов**: приложение работает с файлами с расширением `.txtx`, которые содержат зашифрованный текст.
- **Модульный интерфейс**: включает поддержку изменения шрифта, цвета текста и другие параметры интерфейса.

## Как работает шифрование

Программа использует **алгоритм XOR** для шифрования и расшифровки текста. Когда пользователь шифрует текст, создаётся новый случайный ключ (простое число), который используется для шифрования текста. Этот новый ключ, вместе с первоначальным ключом, передаётся как произведение двух простых чисел. Для расшифровки используется только новый ключ, который можно получить путём деления произведённого значения на известный начальный ключ.

### Пример шифрования:

1. Пользователь открывает файл, содержащий текст для шифрования.
2. Программа генерирует новый ключ и шифрует текст с использованием XOR.
3. Новый ключ передаётся вместе с зашифрованным текстом.
4. Для расшифровки используется новый ключ, который можно извлечь из произведения переданных значений.

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/zemskovik/tkinter-notepad.git
2. Установите зависимости (если они требуются):
   ```bash
   pip install -r requirements.txt
3. Запустите программу:
   ```bash
   python notepad.py
   
## Файл конфигурации
Программа использует конфигурационный файл AmTCD.ini, в котором хранится ключ шифрования.
Пример содержимого конфигурационного файла:
```ini
[main]
keyuser = 496fd2da03559bb5a0c914e28f98902c
```
Если файл конфигурации отсутствует или в нём не задан ключ, используется значение по умолчанию, заданное в коде.

## Основные функции
- **Открытие файлов**: возможность загрузки зашифрованных файлов.
- **Сохранение файлов**: зашифрованные файлы можно сохранить с помощью алгоритма XOR.
- **Выбор шрифта и цвета текста**: интерфейс поддерживает изменение шрифта и цвета текста.
- **Отображение состояния**: информация о положении курсора, количестве символов и других параметрах отображается в строке состояния.

## Пример использования
1. **Шифрование файла**: откройте файл с текстом, измените его и сохраните в формате .txtx.
2. **Расшифровка файла**: откройте зашифрованный файл, и он автоматически будет расшифрован с использованием соответствующего ключа.
