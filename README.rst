Интеграция edX platform с СЦОС (Архивная версия)

*Актуальную версию можно заказать через госзакупки, примерная цена лота 130тыс руб.*


Инсталляция
------------

Склонировать в 

    /edx/app/edxapp/

Установить 

    pip install -r requrements/base.txt


Пояснения
------------

код СЦОС находится здесь
openedx/features/scos/

Виджет экспорта в СЦОС

    cms/templates/export_scos.html
    cms/djangoapps/contentstore/views/export_scos.py


В связи с тем, что требовались дополнительные атриуты курса, были добавлены

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

Поля дополнительных атриутов заполняются в 

  *Студия - Расширенные настройки*

Функция для передачи результатов в СЦОС

## update_subsection_grade_scos_for_user_v2

Асинхроннй запуск функции передачи результатов в СЦОС

*lms/djangoapps/certificates/signals.py*
строка 146

Ручной запуск функции передачи результатов в СЦОС на странице прогресса

*lms/templates/courseware/progress.html*

Дополнительнй поля справа на странице

*lms/templates/courseware/course_about.html*

Параметры настроек доступа
------------

Данные поля должн быть заполнены в соответствии с вашими ключами доступа, выданными в СЦОС

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

Файлы сертификата и ключ в папке
*openedx/features/scos/keys/bc007e88-0e4b-4a1a-975a-8aecca36542d.crt*
*openedx/features/scos/keys/bc007e88-0e4b-4a1a-975a-8aecca36542d.key*

или пропишите их сами
openedx/features/scos/conf.py
строки 20-22
SSL_CERT = MODULE_DIR + '/keys/bc007e88-0e4b-4a1a-975a-8aecca36542d.crt'
SSL_KEY = MODULE_DIR + '/keys/bc007e88-0e4b-4a1a-975a-8aecca36542d.key'


.. _Демка: https://online.fa.ru


License
-------

The code in this repository is licensed under version 3 of the AGPL
unless otherwise noted. Please see the `LICENSE`_ file for details.

.. _LICENSE: https://www.gnu.org/licenses/agpl-3.0.en.html



