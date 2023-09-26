# Лабораторная работа № 2

## Тема: Разработка приложения «Адресная книга»

## Вариант 1

## Реализация

Главное окно:
   
   ![nonlin](images/main_window.png)

Окно добавления:
   
   ![nonlin](images/add_window.png)

Пагинация:
   
   ![nonlin](images/pagination.png)

Окно изменения:
   
   ![nonlin](images/edit_window_part1.png)
   
   ![nonlin](images/edit_window_alert.png)
   
   ![nonlin](images/edit_window_part2.png)

Окно удаления:
   
   ![nonlin](images/remove_window.png)
   
   ![nonlin](images/remove_window_alert.png)

Окно поиска:
   
   ![nonlin](images/find_window.png)
   
   ![nonlin](images/find_window_alert.png)

Сохранение:
   
   ![nonlin](images/save_alert.png)
   
   **Содержимое сохраненного файла**
   
   ```json
   [
      {
      "name": "Nikita Seleznev",
      "address": "Zhabinka city"
      }
   ]

Загрузка:
   
   ![nonlin](images/load_window.png)

Инструкция по применению:

**Заранее установленный nvm or node js (В данном случае использовалась 14.13.1, Vue 2)**

```cmd
cd task_02/src
npm i
npm run dev
