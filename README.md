# H5P Packager Utility / Утилита сборки H5P библиотек

## Русский

### Описание

Когда по каким-то причинам невозможно обновить H5P пакеты или библиотеки через стандартную таску Moodle (например, отсутствует доступ к интернету или к ресурсу с пакетами H5P), эта утилита поможет собрать H5P библиотеку с правильной структурой для Moodle. После этого архив можно вручную загрузить в Moodle через интерфейс импорта H5P.

Утилита автоматически:

* Читает `library.json` в каталоге библиотеки
* Формирует имя каталога по правилам H5P (`machineName` или `machineName-major.minor`)
* Создаёт `.h5p` архив с корректной структурой, который Moodle сможет импортировать без ошибок валидации

### Установка

Убедитесь, что установлен Python 3.

Склонируйте или скачайте скрипт `make_h5p.py`.

### Использование

```bash
python make_h5p.py /путь/к/библиотеке
```

Пример:

```bash
python make_h5p.py ./H5P.JoubelUI-1.3
```

По умолчанию создаётся архив рядом с исходной директорией с именем `H5P.JoubelUI-1.3.h5p`.

Дополнительно можно указать путь вывода:

```bash
python make_h5p.py ./H5P.JoubelUI-1.3 -o ./archives/H5P.JoubelUI-1.3.h5p
```

Параметр `--no-skip-hidden` позволяет включать скрытые файлы и каталоги.

---

## English

### Description

When it is not possible to update H5P packages or libraries using Moodle's standard task (for example, due to no internet access or blocked H5P resource servers), this utility helps package an H5P library with the correct structure for Moodle. The resulting archive can be manually uploaded through the H5P import interface.

The utility automatically:

* Reads `library.json` from the library folder
* Determines the correct directory name according to H5P rules (`machineName` or `machineName-major.minor`)
* Creates a `.h5p` archive with a structure Moodle can import without validation errors

### Installation

Ensure Python 3 is installed.

Clone or download the script `make_h5p.py`.

### Usage

```bash
python make_h5p.py /path/to/library
```

Example:

```bash
python make_h5p.py ./H5P.JoubelUI-1.3
```

By default, the archive will be created next to the source folder as `H5P.JoubelUI-1.3.h5p`.

You can also specify an output path:

```bash
python make_h5p.py ./H5P.JoubelUI-1.3 -o ./archives/H5P.JoubelUI-1.3.h5p
```

Use `--no-skip-hidden` to include hidden files and directories.
