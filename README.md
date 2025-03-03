# fileMan1

Консольный файловый менеджер с базовыми операциями и анализом файловой системы.

## Установка

```bash
git clone https://github.com/yourusername/fileMan1.git
cd fileMan1
pip install -e .
```
## Основные команды:

#### Копировать файл
```bash
manager copy source.txt destination/
```
#### Удалить файл/папку
```bash
manager delete path/to/target
```
#### Подсчет файлов в директории
```bash
manager count path/to/dir
```
#### Поиск файлов по regex
```bash
manager search path/to/dir ".*\.txt"
```
#### Добавить дату создания в имена файлов
```bash
manager add-date path/to/dir --recursive
```
#### Анализ размера папки
```bash
manager analyse path/to/dir
```

## Запуск тестов
```bash
python -m unittest discover tests
```

##  Запуск GUI
```bash
manager gui
```