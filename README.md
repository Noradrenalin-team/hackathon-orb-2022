# Кейс #1 Творческий конкурс журналистов
## Хакатон-Оренбург-2022

### Реальзиваны модули:
- Фронт система для визуализации данных и предоставление сервисов (процессов)
- Бэк система для управления процессами предоставления сервисов и наполнением контента фронт системы
- Анализ текста на антиплагиат
- Поиск отклика читателей в сети
- Модуль народного голосования

## Установка

- Используется ос Ubuntu (22.03) 
- Установить докер
```sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin```
- Запуск контейнера с *postgres*
```
docker run --name pgName2 -p 5432:5432  -e POSTGRES_PASSWORD=1234567890 -e PGDATA=/var/lib/postgresql/data/pgdata -d -v "/absolute/path/to/directory-with-data":/var/lib/postgresql/data postgres:13.3
```

- Установка пакетов
```
git clone https://github.com/Noradrenalin-team/hackathon-orb-2022.git
cd hackathon-orb-2022

sudo apt install python3-pip
sudo apt-get install libpq-dev python3-dev
python3 -m pip install -r requirements.txt
```
- Применение миграций
```
python3 src/manage.py makemigrations
python3 src/manage.py migrate
```
- Проверка что работает
```python3 src/manage.py runserver```

## Настройка
- Создаём админа
```python3 src/manage.py createsuperuser```
- В админке (на странице http://127.0.0.1:8000/admin/main/contests/) создать contest (обязательно со статусом текщий).
Теперь на главной странице будет отображаться информация о текущем конкурсе



