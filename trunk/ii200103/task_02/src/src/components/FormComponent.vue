<template>
  <div class="grid-container">
    <div class="form">
      <el-form label-position="left" label-width="100px">
        <el-form-item v-if="!users.length" label="Name">
          <el-input :readonly="true"></el-input>
        </el-form-item>

        <el-form-item
          v-if="users.length"
          v-for="item in displayedData"
          label="Name"
        >
          <el-input :value="item.name" :readonly="true"></el-input>
        </el-form-item>

        <el-form-item v-if="!users.length" label="Address">
          <el-input :readonly="true" type="textarea"></el-input>
        </el-form-item>

        <el-form-item
          v-if="users.length"
          v-for="item in displayedData"
          label="Address"
        >
          <el-input
            :value="item.address"
            :readonly="true"
            type="textarea"
          ></el-input>
        </el-form-item>
      </el-form>

      <el-pagination
        background
        layout="prev, pager, next"
        prev-text="Previous"
        next-text="Next"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="pageSize"
        :total="totalItems"
        @current-change="handleCurrentChange"
      >
      </el-pagination>
    </div>
    <div class="grid-item">
      <el-button
        style="margin-bottom: 10px; margin-left: 10px"
        type="primary"
        plain
        size="mini"
        @click="openDialog('ADD')"
        >Add</el-button
      >
      <el-button
        style="margin-bottom: 10px"
        type="primary"
        plain
        size="mini"
        @click="openDialog('EDIT')"
        >Edit</el-button
      >
      <el-button
        style="margin-bottom: 10px"
        type="primary"
        plain
        size="mini"
        @click="openDialog('REMOVE')"
        >Remove</el-button
      >
      <el-button
        style="margin-bottom: 10px"
        type="primary"
        plain
        size="mini"
        @click="openDialog('FIND')"
        >Find</el-button
      >
      <el-button
        style="margin-bottom: 10px"
        type="primary"
        plain
        size="mini"
        @click="loadUsers"
        >Load</el-button
      >
      <el-button
        style="margin-bottom: 10px"
        type="primary"
        plain
        size="mini"
        @click="saveUsers"
        >Save</el-button
      >
    </div>
    <el-dialog :title="dynamicTitle" :visible.sync="dialogVisible" width="30%">
      <el-form label-position="left" label-width="100px">
        <el-form-item label="Name" prop="name">
          <el-input v-model="name"></el-input>
        </el-form-item>
        <el-form-item v-if="!isDelOrFind" label="Address" prop="address">
          <el-input v-model="address"></el-input>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="closeDialog">Cancel</el-button>
        <el-button type="primary" @click="confirmDialog">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'AddressBook',
  data() {
    return {
      users: [], // Массив пользователей
      name: '', // Поле имени
      address: '', // Поле адрес
      dialogVisible: false, // Для отображения доп модального окна
      currentPage: 1, // Текущая страница
      pageSize: 1, // Количество элементов на странице
      buttonType: '', // Тип кнопки, для переиспользования модального окна(ADD, EDIT и т.д)
      isDelOrFind: false, // Если нажимаем кнопку удалить или поиск, убираем поле адрес с диалогового окна
      dynamicTitle: '', // Динамический заголовок в диалоговом окне
    }
  },
  computed: {
    totalItems() {
      return this.users.length // Общее количество элементов
    },
    displayedData() {
      // Метод для отображения данных на текущей странице
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      return this.users.slice(startIndex, endIndex)
    },
    dialogTitle() {
      // Здесь можно использовать значение dynamicTitle для динамического заголовка
      return this.dynamicTitle
    },
  },
  methods: {
    openDialog(mode) {
      // Метод для активации диалогового окна
      if (mode === 'REMOVE' || mode === 'FIND') {
        this.isDelOrFind = true
      }
      this.dynamicTitle = mode
      this.buttonType = mode
      this.dialogVisible = true
    },

    confirmDialog() {
      // Метод для вызова функций в зависимости от типа кнопки
      switch (this.buttonType) {
        case 'ADD': {
          this.createUser()
          break
        }
        case 'EDIT': {
          this.updateUser()
          break
        }
        case 'REMOVE': {
          this.removeUser()
          this.isDelOrFind = false
          break
        }
        case 'FIND': {
          this.findUser()
          this.isDelOrFind = false
          break
        }
        default:
          break
      }
      this.dialogVisible = false
    },

    createUser() {
      // Метод для создания пользователя и добавления его в массив
      const exist = this.users.find((el) => !!(el.name === this.name)) // Проверяем, есть ли юзер с такими именем(считаем, что имя аналог id) и приводим к boolean, нам важен сам факт

      if (!exist && this.name && this.address) {
        this.users.push({ name: this.name, address: this.address })
      } else {
        this.$alert('Пользователя с таким именем не существует', 'Ошибка', {
          confirmButtonText: 'Закрыть',
        })
      }
      // Очищаем поля для ввода адресса и имени
      this.clearAttr()
    },

    updateUser() {
      // Метод для редактирования пользователя
      const user = this.users.find((el) => el.name === this.name) // Проверяем, есть ли юзер с такими именем

      if (user?.address !== this.address && this.address) {
        user.address = this.address
        this.$alert(
          `Пользователь с именем ${user.name} успешно обновлен`,
          'Успешно',
          {
            confirmButtonText: 'Закрыть',
          }
        )
      } else if (!user) {
        this.$alert('Пользователя с таким именем не существует', 'Ошибка', {
          confirmButtonText: 'Закрыть',
        })
      }
      // Очищаем поля для ввода адресса и имени
      this.clearAttr()
    },

    removeUser() {
      const userIndex = this.users.findIndex((el) => el.name === this.name)

      if (userIndex !== -1) {
        this.users.splice(userIndex, 1) // Удалить пользователя из массива
        this.$alert(`Пользователь с именем ${this.name} удалён`, 'Успешно', {
          confirmButtonText: 'Закрыть',
        })
        if (this.users.length !== 1) {
          this.currentPage = this.users.length
        }
      } else {
        this.$alert('Пользователя с таким именем не существует', 'Ошибка', {
          confirmButtonText: 'Закрыть',
        })
      }
      this.clearAttr()
    },

    findUser() {
      const userIndex = this.users.findIndex((el) => el.name === this.name)

      if (userIndex !== -1) {
        this.$alert(
          `Пользователь ${this.users[userIndex].name} найден`,
          'Успешно',
          {
            confirmButtonText: 'Закрыть',
          }
        )
        if (this.users.length !== 1) {
          this.currentPage = userIndex + 1
        }
      } else {
        this.$alert('Пользователя с таким именем не существует', 'Ошибка', {
          confirmButtonText: 'Закрыть',
        })
      }
      this.clearAttr()
    },

    saveUsers() {
      if (this.users.length) {
        this.$alert('Загрузка файла с расширением .json', 'Информация', {
          confirmButtonText: 'Ок',
        })
      } else {
        this.$alert('Данных для загрузки нет', 'Ошибка', {
          confirmButtonText: 'Закрыть',
        })
        return
      }

      const dataToSave = JSON.stringify(this.users)

      // Объект Blob для данных
      const blob = new Blob([dataToSave], { type: 'application/json' })

      // Объект URL для Blob
      const url = URL.createObjectURL(blob)

      // Элемент 'a' для скачивания файла
      const a = document.createElement('a')
      a.style.display = 'none'
      a.href = url
      a.download = 'data.json' // Имя файла для сохранения

      // Элемент 'a' на страницу и клик на нем
      document.body.appendChild(a)
      a.click()

      // Удаляем элемент 'a' и освобождаем URL объекта Blob после скачивания файла
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    },

    loadUsers() {
      // Элемент input для выбора файла
      const input = document.createElement('input')
      input.type = 'file'

      // Обработчик события изменения для выбора файла
      input.addEventListener('change', (event) => {
        const file = event.target.files[0]
        if (file) {
          // Читаем содержимое файла
          const reader = new FileReader()
          reader.onload = (e) => {
            // Парсим данные из файла формата .json(те, что сохранили)
            const data = JSON.parse(e.target.result)

            // Подгружаем данные
            this.users = data

            // Закрываем диалоговое окно выбора файла
            input.value = ''
          }

          // Читаем как с текстового для того, что бы reader работал
          reader.readAsText(file)
        }
      })

      // Кликаем на элемент input, чтобы открыть диалоговое окно выбора файла
      input.click()
    },

    handleCurrentChange(newPage) {
      // Метод для присвоения текущей страницы пагинации
      this.currentPage = newPage
    },

    clearAttr() {
      // Метод для очистки полей в диалоговом окне
      this.name = ''
      this.address = ''
    },

    closeDialog() {
      this.clearAttr()
      this.dialogVisible = false
    },
  },
}
</script>
