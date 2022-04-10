# Проектная работа 10 спринта
Задачи можно посмотреть в /tasks

## Ссылка на репозиторий с проектом:
https://github.com/AlexanderNkn/notifications_sprint_1

## Описание
Сервис нотификации оповещает пользователя о событиях посредством email рассылки. Возможно расширение для sms и push уведомлений. События могут быть как мгновенными, например приветственное письмо при регистрации нового пользователя, так и периодическими, например статистика в конце каждого месяца по просмотренным пользователем фильмам.

## Архитектурные решения
- описание диаграмм в формате plantUML представлено в docs/architecture/

### Работа в 10 спринте
![Архитектура сервисов нотификации](docs/architecture/notifications_architecture.png)

## Установка
- склонируйте проект с репозитория GitHub
    ```
    git clone https://github.com/AlexanderNkn/notifications_sprint_1.git
    ```
- переименуйте файл с переменными окружения для тестирования
    ```
    mv email/envs/.email.env.sample email/envs/.email.env
    mv email/envs/mailhog-auth.sample email/envs/mailhog-auth
    ```
- соберите образ
    ```
    docker-compose build --no-cache
    ```
- запустите проект
    ```
    docker-compose up -d
    ```

## Использование
### Тестовая отправка данных через RabbitMQ
- Перейдите в браузере на страницу
    ```
    http://localhost:15672/#/exchanges/%2F/test-exchange
    ```
- Введите тестовое сообщение в разделе **Publish message**
  ![Отправка тестового сообщения](docs/images/push_msg.jpg)
- Для просмотра отправленных писем перейдите на страницу (логин:пароль = test:test ) 
    ```
    http://localhost:8025/
    ```
  ![mailhog_UI](docs/images/mailhog_UI.jpg)
