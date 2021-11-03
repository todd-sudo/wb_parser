# Парсер для Wildberries


### Установка и запуск проекта (в ручном режиме)

1. Клонировать репозиторий:

    ```bash
    git clone https://github.com/dev2033/wb_parser.git
    ```
   
2. Перейти в директорию с проектом:

    ```bash
    cd wb_parser/
    ```

3. Установить и активировать виртуальное окружение и установить зависимости:
    
    ```bash
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```
   
4. Перейти в дирикторию `src/` и запустить файл `main.py`:
    
    ```bash
    python3 main.py
    ```
   
5. Чтобы отправить запрос с id товаров, нужно выполнить следующее:

    - **Утилита `curl`**: 
        ```bash
            curl -X 'POST' \
              'http://127.0.0.1:8000/csv-json' \
              -H 'accept: application/json' \
              -H 'Content-Type: application/json' \
              -d '{
              "id": [
                "8279056",
                 "10899304",
                 "8576622"
              ]
            }'  
        ```
    - **Утилита Postman**:
        
        Отправляем POST запрос на адрес `http://127.0.0.1:8000/csv-json`
        в панели ниже выбираем Body и вставляем json, типа:
        ```bash
          {
            "id": [
              "8279056",
              "10899304",
              "8576622"
            ]
          }
        ```
        Если в ответ вернется такой же json, значит запрос правильный и запустился
        парсинг. Если отправить запрос повторно, но парсер не закончил работу, вернется 
        ошибка, с статус кодом `405` - `Method Not Allowed`. Текст ошибки:
        ```bash
        {
          "detail": "Parsing process in progress! Please wait..."
        }  
        ```

6. Для получения результатов парсинга, нужно отправить GET 
    запрос на URL - `http://127.0.0.1:8000/get_data_json` :
    
    - Утилита `curl`:
        ```bash
          curl -X 'GET' \
            'http://127.0.0.1:8000/get_data_json' \
            -H 'accept: application/json'  
        ```
    
    В случае успеха ответом придет полученный, в результате парсинга - json:

    ```bash
       [
          {
            "8279056": {
              "price": 640,
              "sale": 51,
              "basicSale": 30,
              "basicPrice": 448,
              "promoSale": 30,
              "promoPrice": 313,
              "CustomerSale": "",
              "CustomerPrice": ""
            }
          },
          {
            "10899304": {
              "price": 3300,
              "sale": 62,
              "basicSale": 40,
              "basicPrice": 1980,
              "promoSale": 37,
              "promoPrice": 1247,
              "CustomerSale": "",
              "CustomerPrice": ""
            }
          },
      ]  
    ```
    

7. Файл `state_parsing.json` нужен для проверки состояния парсера 
    (работает / отключен), если работает (`false`), то новые POST запросы 
    не принимаются и возвращается ошибка!

<hr><hr>

### Установка и запуск проекта (с помощью скрипта)

1. Клонировать репозиторий:

    ```bash
    git clone https://github.com/dev2033/wb_parser.git
    ```
   
2. Перейти в директорию с проектом:

    ```bash
    cd wb_parser/
    ```
   

3. В файле `systemd_config/parser.service` изменить пути до 
   рабочей директории(`WorkingDirectory=`) 
   и до файла `run.sh` (`ExecStart=`)
   

4. После этого нужно скопировать файл Unit'а (`systemd_config/parser.service`) в 
   `/etc/systemd/system/`:
   
   ```bash
   sudo cp parser.service /etc/systemd/system/
   ```


5. Запускаем демон:

   ```bash
   sudo service parser start
   ```

6. Для проверки работы демона, выполнить команду:

   ```bash
   sudo service parser status
   ```

7. Чтобы остановить демон:

   ```bash
   sudo service parser stop
   ```

8. Чтобы запустить службу при загрузке системы, 
    используйте команду - `sudo systemctl enable parser.service`
   
<hr>

**Настройки nginx, если нужно слушать 80 порт**

<hr>

9. Настройка nginx (`/etc/nginx/site-available/default`): 

    ```bash
        server {
        listen 80;
        server_name localhost;
        access_log  /var/log/nginx/example.log;
     
        location / {
            proxy_pass http://127.0.0.1:8000; 
            proxy_set_header Host $server_name;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    ```

10. Перезапустить nginx командой - `sudo service nginx restart`
    

11. Проверить работоспособность nginx - `sudo service nginx status`


12. Чтобы отправить запрос с id товаров, нужно выполнить следующее:

    - **Утилита `curl`**: 
        ```bash
            curl -X 'POST' \
              'http://127.0.0.1:8000/csv-json' \
              -H 'accept: application/json' \
              -H 'Content-Type: application/json' \
              -d '{
              "id": [
                "8279056",
                 "10899304",
                 "8576622"
              ]
            }'  
        ```
    - **Утилита Postman**:
        
        Отправляем POST запрос на адрес `http://127.0.0.1:8000/csv-json`
        в панели ниже выбираем Body и вставляем json, типа:
        ```bash
          {
            "id": [
              "8279056",
              "10899304",
              "8576622"
            ]
          }
        ```
        Если в ответ вернется такой же json, значит запрос правильный и запустился
        парсинг. Если отправить запрос повторно, но парсер не закончил работу, вернется 
        ошибка, с статус кодом `405` - `Method Not Allowed`. Текст ошибки:
        ```bash
        {
          "detail": "Parsing process in progress! Please wait..."
        }  
        ```

13. Для получения результатов парсинга, нужно отправить GET 
    запрос на URL - `http://127.0.0.1:8000/get_data_json` :
    
    - Утилита `curl`:
        ```bash
          curl -X 'GET' \
            'http://127.0.0.1:8000/get_data_json' \
            -H 'accept: application/json'  
        ```
    
    В случае успеха ответом придет полученный, в результате парсинга - json:

    ```bash
       [
          {
            "8279056": {
              "price": 640,
              "sale": 51,
              "basicSale": 30,
              "basicPrice": 448,
              "promoSale": 30,
              "promoPrice": 313,
              "CustomerSale": "",
              "CustomerPrice": ""
            }
          },
          {
            "10899304": {
              "price": 3300,
              "sale": 62,
              "basicSale": 40,
              "basicPrice": 1980,
              "promoSale": 37,
              "promoPrice": 1247,
              "CustomerSale": "",
              "CustomerPrice": ""
            }
          },
      ]  
    ```
    

14. Файл `state_parsing.json` нужен для проверки состояния парсера 
    (работает / отключен), если работает (`false`), то новые POST запросы 
    не принимаются и возвращается ошибка!
    