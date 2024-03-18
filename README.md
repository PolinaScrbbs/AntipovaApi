## AntipovaApi Initial Version
> Команды для запуска в файле setup_commands.txt
___

### Поддерживаемые функции:
* #### Регистрация пользователя:
    * Email(Login)
    * Password
    * Full_name
    * Phone_number(Null=True)
* #### Авторизация:
    * Login
    * Password

    > После авторизации возвращается Token

* #### Получение списка объявлений

* #### Работа с отдельными объявлениями по id:
    * GET
    * POST
    * PUT
    * DELETE
_______

### Для работы с запросами:
* #### Регистрация (http://127.0.0.1:8000/AntipovaApi/auth-signup/):
    * ##### Передать все нужные параметры, номер телефона не обязательный
* #### Авторизация (http://127.0.0.1:8000/AntipovaApi/auth-login/):
    * ##### Передать все нужные параметры
* #### Получение списка объявлений (http://127.0.0.1:8000/AntipovaApi/advertisements/?token=user_token):
    ```json
    {
        "token": "user_token",
    }
    ```
* #### Создание объявления (http://127.0.0.1:8000/AntipovaApi/advertisements/?token=user_token):
    ```json
    {
        "token": "user_token",
    }
    ```
    > Дальше все поля для создания объявления
* #### Запросы для отдельных объявлений:
    * #### GET(http://127.0.0.1:8000/AntipovaApi/advertisement/?token=user_token):
        ```json
        {
            "token": "user_token",
            "id": "advertisement_id"
        }
        ```
    * #### PUT(http://127.0.0.1:8000/AntipovaApi/advertisement/?token=user_token):
        ```json
        {
            "token": "user_token",
            "id": "advertisement_id"
        }
        ```
        > Дальше вы в таком же формате вводите название поля, которое хотите изменить и его значение
        ```json
        {
            "token": "user_token",
            "id": "advertisement_id",
            "price": 2500
        }
        ```
    * #### DELETE(http://127.0.0.1:8000/AntipovaApi/advertisement/?token=user_token):
        ```json
        {
            "token": "user_token",
            "id": "advertisement_id"
        }
        ```




