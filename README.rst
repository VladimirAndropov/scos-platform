Платформа дистанционного обучения с интеграцией с  Государственной информационной системой Современная Цифровая Образовательная Среда

* для бесплатной установки в российских вузах*

*stack: см картинку

![Preview](https://github.com/VladimirAndropov/scos-platform/blob/master/architecture.png?raw=true)

Описание архитектуры см. в документации

Быстрая инсталляция
------------

Склонировать в 

    /edx/app/edxapp/

Установить 

    pip install -r requrements/base.txt


Пояснения
------------

отдельная интеграция с СЦОС находится здесь
https://github.com/VladimirAndropov/scos-platform/tree/master/openedx/features/scos

Виджет экспорта в СЦОС

    https://github.com/VladimirAndropov/scos-platform/tree/master/cms/templates/export_scos.html
    https://github.com/VladimirAndropov/scos-platform/tree/master/cms/djangoapps/contentstore/views/export_scos.py


 Атрибуты объекта курс, необходимые для передачи в СЦОС

> competences = serializers.CharField(max_length=255)
> 
> accreditated = serializers.CharField()
> 
> assessment_description = serializers.CharField()
> 
>   duration = serializers.BooleanField()
> 
> estimation_tools = serializers.CharField()
> 
> hours = serializers.BooleanField()
> 
>    hours_per_week = serializers.BooleanField()
> 
>  proctoring_service = serializers.CharField()
>
>  proctoring_type = serializers.CharField()
> 
> requirements = serializers.CharField()
> 
> business_version = serializers.BooleanField()

Поля атрибутов заполняются в 

  *Студия - Расширенные настройки*

Функция для передачи результатов в СЦОС

## update_subsection_grade_scos_for_user_v2
смотри
 https://github.com/VladimirAndropov/scos-platform/tree/master/lms/djangoapps/grades/tasks.py

Асинхроннй запуск функции передачи результатов в СЦОС

 https://github.com/VladimirAndropov/scos-platform/tree/master/lms/djangoapps/certificates/signals.py
от строки 146

Ручной запуск функции передачи результатов в СЦОС на странице прогресса

 https://github.com/VladimirAndropov/scos-platform/tree/master/lms/templates/courseware/progress.html

Дополнительные поля 

 https://github.com/VladimirAndropov/scos-platform/tree/master/lms/templates/courseware/course_about.html

Параметры настроек доступа
------------

Данные поля должн быть заполнены в соответствии с вашими ключами доступа, выданными в СЦОС

обычно, заполняются в файлах:
   *lms.envs.json*
   *cms.envs.json*


    "SSO_BASE_URL": "https://auth-test.online.edu.ru/realms/portfolio",
    "PLATFORM_ID": "39************8a6db466",
    "INSTITUTION_ID": "7************9ff5",
    "DOMAIN": "test.online.edu.ru",
    "API_URL": "https://test.online.edu.ru/api/",
    "API_USER": "****y",
    "API_USER_ID": "****y",
    "API_PASSWORD": "2*****",
    "PORTFOLIO_API_URL": "https://portfolio.edu.ru/api/",
    "CLIENT_ID" : "*****y",
    "CLIENT_SECRET_KEY" : "2*******",

Файлы сертификата и ключи кидайте в файлы
*openedx/features/scos/keys/bc007e88-0e4b-4a1a-975a-8aecca36542d.crt*
*openedx/features/scos/keys/bc007e88-0e4b-4a1a-975a-8aecca36542d.key*

остальные настройки смотри в
openedx/features/scos/conf.py


Как выглядит в итоге?
-------

`Демка`_ 

.. _Демка: https://online.fa.ru



_донаты
-------

Помочь проекту в Юмани:
https://yoomoney.ru/fundraise/I3gROgPkbhU.230625

License
-------

The code in this repository is licensed under version 3 of the AGPL
unless otherwise noted. Please see the `LICENSE`_ file for details.

.. _LICENSE: https://www.gnu.org/licenses/agpl-3.0.en.html



