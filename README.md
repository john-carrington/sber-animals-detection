![Title Image](https://github.com/john-carrington/sber-animals-detection/blob/main/.git-images/title_repo.png)


# Разработка модели детекции млекопитающих по фото с БПЛА

[![Python](https://img.shields.io/pypi/pyversions/tensorflow.svg)](https://www.python.org/downloads/)

> Цель данного проекта — создать модель для автоматического обнаружения млекопитающих с помощью БПЛА.

## Развертывание решения
1. Клонирование репозитория
``` bash
git clone https://github.com/john-carrington/sber-animals-detection.git
cd sber-animals-detection
```
2. Соборка Docker-образ
``` bash
docker build -t sber-project .
```
3. Запуск Docker-контейнера
``` bash
docker run -d -p 5173:5173 sber-project
```
4. Перейдите по адресу 
``` bash
localhost:5173
```

## Пример использования

```

```


## Полезные ресурсы
[Ultralytics YOLO Руководство понастройке гиперпараметров](https://docs.ultralytics.com/ru/guides/hyperparameter-tuning/#default-search-space-description)
[Обучение модели с Ultralytics YOLO](https://docs.ultralytics.com/ru/modes/train/)
[Документация Gradio](https://www.gradio.app/)
[Label Studio](https://labelstud.io/)

## Авторы

- [@john-carrington](https://github.com/john-carrington)
- [@ZaplatinArtur](https://github.com/ZaplatinArtur)
- [@Desanrek](https://github.com/Desanrek)
- [@colrosezxn](https://github.com/colrosezxn)


