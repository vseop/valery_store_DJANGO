## Freelance заказ
### ТЗ
Сделать магазин аддаптивный для всех устройств.
* с категориями товаров и подкатегориями (один уровень вложенности)
* наличием Flatpages c редактором
* настроить админку, чтобы было быстро и удобно добавлять новые товары
* возможностью добавлять из админки фото любого размера, чтобы они автоматически форматировались под нужный размер в jpeg
* вывод на сайте и в админке количества уникальных товаров каждой подкатегории и категории
* оптимизация запросов в БД
* удобная пагинация при большом количестве страниц.
* возможностью выбирать товары для главной страницы, а так же помечать как черновик
* наличие поиска товара
* динамический слайдер для вывода фото товара в детализации 

### Комментарии
* Для оптимизации запросов в БД добавил поле count_prod (общее количество уникальных товаров) в категории, которое будет автоматически пересчитываться при изменении или удалении товара при помощи сигналов post_save и post_delete. => store.models
* На основе Flatpages, написал свое приложение с редактором ckeditor. => flatpage_main
* Настроил  админку (ckeditor, TabularInline, вывод изображений и т.д) => store.admin.py
* Функция для обработки изображений => store.utils.py
* Написал менеджер контекста, который забирает нужные нам поля из связанных моделей, а также оптимизировал запросы во вьюхах при помощи only, select_related и prefetch_related.
* Пагинация , которая отображает по три предыдущие и следующие страницы от текущей, а также первую и последнюю => template.include.paginat.html
* Динамический слайдер => template.product_detail.html
* Docker-compose - две сборки  devop и production (инструкция ниже)

### Установка приложения
#### Разработка  
Django server, пользователь root
1) docker-compose up --build  
2) docker-compose exec web sh  
3) python manage.py makemigrations  
4) python manage.py migrate  
5) python manage.py createsuperuser  
#### Production  
Nginx, gunicorn, создаем пользователя valery и др. настройки  
1) docker-compose -f docker-compose.prod.yaml up -d --build  
2) docker-compose -f docker-compose.prod.yaml exec web sh  
3) python manage.py makemigrations  
4) python manage.py migrate  
5) python manage.py createsuperuser  
6) python manage.py collectstatic
