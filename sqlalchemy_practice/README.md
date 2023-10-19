# Использование ORM SQLAlchemy и миргации Alembic с PostgreSQL.
## Настройка окружения:
Создаем папку с проектом и создаем проект __poetry__:
```sh
poetry new project_name
```

После чего - необходимо инициализировать проект с помощью
```sh
poetry init
```

После чего переходим в окружение poetry и обновляем __pip__
```sh
poetry shell
pip install --upgrade pip
```

Далее накатываем нужные библиотеки: __SQLAlchemy__ и __Alembic__
```sh
poetry add sqlalchemy
poetry add sqlalchemy-utils
poetry add alembic
poetry add postgres
```
Также необходимо установить __dotenv__ (для чего - будет сказано позднее)

Его устанавливаем следующим образом
```sh
poetry add python-dotenv
```

Теперь наше окружение настроено и мы готовы добавлять модели и миграции

## Создание моделей
Для создания моделей необходимо накатить следующие импорты:
```py
from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType
import uuid
from sqlalchemy.ext.declarative import declarative_base
```

Теперь объявим саму модель и объявим __metadata__ с декларативной моделью Base
```py
Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'User'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid1)
    name = Column(String(30))
```

Таким образом мы объявили модель __User__, в которой на данный момент хранится id и имя пользователя


## Настройка конфигурации проекта и объявление секретов
В папке проекта создаем файл .env, который сразу добавляем в __.gitignore__, чтобы наши данные не утекли в наш репозиторий

В .env прописываем наши секреты:
```env
DB_HOST=host
DB_USER=user
DB_PASSWORD=password
```

создаем в рабочей папке __config.py__ и туда импортируем:
```py
from dotenv import load_dotenv
import os
```
И прописывам в конфиге переменные, которые хранятся в __.env__ и выгружаем их через __load_dotenv__:
```py
load_dotenv()

DB_HOST=os.environ.get('DB_HOST')
DB_PORT=os.environ.get('DB_PORT')
DB_USER=os.environ.get('DB_USER')
DB_PASSWORD=os.environ.get('DB_PASSWORD')
```

## Миргации с помощью Alembic
Для инициализации alembic - необходимо прописать:
```sh
alembic init folder_name
```
_P.S. вместо folder_name рекомендуется использовать имя __migrations__ для соблюдения логики использования alembic_

Далее, как вы можете заметить - в папке нашего проекта также появился файл __alembic.ini__ - это конфигурационный файл alembic
В нем нас интересует __sqlalchemy.url__

В __sqlalchemy.url__ прописываем:
```ini
sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASSWORD)s@%(DB_HOST)s/%(DB_NAME)s
```
_P.S. в скобках пишем названия наших секретов_

Далее - нам необходимо передать наши секреты в alembic.ini. Для этого в папке, которую создал alembic нам нужно зайти в evn.py и видоизменить его добавив следующее:
```py
from sqlalchemy_practice.models import metadata
from sqlalchemy_practice.config import (DB_HOST,
                                        DB_NAME,
                                        DB_PASSWORD,
                                        DB_PORT,
                                        DB_USER)

config = context.config
target_metadata = metadata

section = config.config_ini_section
config.set_section_option(section, 'DB_HOST', DB_HOST)
config.set_section_option(section, 'DB_NAME', DB_NAME)
config.set_section_option(section, 'DB_PASSWORD', DB_PASSWORD)
config.set_section_option(section, 'DB_PORT', DB_PORT)
config.set_section_option(section, 'DB_USER', DB_USER)
```
_P.S. вместо __sqlalchemy_practice__ пропишите название директории, в которой у вас хранится config_

## Создание миграций

Далее, для того чтобы создать первую миграцию - необходимо прописать
```sh
alembic revision --autogenerate -m "your message"
```

после чего в папке, которую создал __alembic__ в __versions__ мы увидим нашу первую миграцию

__ВАЖНО! ALEMBIC В ФАЙЛЕ МИГРАЦИИ ПРЕДУПРЕЖДАЕТ ВАС О ТОМ, ЧТО ОНИ МОГУТ БЫТЬ НЕ ТОЧНЫМИ, ПОЭТОМУ ЖЕЛАТЕЛЬНО ВСЕГДА ПРОВЕРЯТЬ МИГРАЦИИ, КОТОРЫЕ БУДЕТ ДЕЛАТЬ ALEBMIC!!!__

Чтобы применить миграции - необходимо прописать:
```sh
alembic upgrade num_of_your_migration
```
Вместо __num_of_your_migration__ необходимо подставить номер вашей миграции - он указан в файле с миграцией в переменной __revision__
