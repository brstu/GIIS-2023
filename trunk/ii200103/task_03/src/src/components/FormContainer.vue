<template>
  <div class="f-layout">
    <div class="page-header">
      <p class="page-title_1" v-if="option.toString() == 'Авиабилеты'">
        Поиск дешевых авиабилетов
      </p>
      <p class="page-title_1" v-else>Лучшие предложения отелей</p>
      <p class="page-title_2" v-if="option.toString() == 'Авиабилеты'">
        16 лет помогаем вам экономить
      </p>
      <p class="page-title_2" v-else>
        Забронируйте деальный номер о лучшей цене
      </p>
      <div class="option-group">
        <el-radio-group v-model="option" @change="handleOption">
          <el-radio-button label="Авиабилеты"></el-radio-button>
          <el-radio-button label="Отели"></el-radio-button>
        </el-radio-group>
      </div>
    </div>
    <div class="form-input" v-if="option.toString() == 'Авиабилеты'">
      <div
        class="el-input"
        style="width: 200px; height: 70px; padding-right: 2px"
      >
        <input
          type="text"
          autocomplete="off"
          placeholder="Откуда"
          class="el-input__inner ddd"
        />
      </div>
      <div class="el-input" style="width: 200px; height: 70px; padding: 2px">
        <input
          type="text"
          autocomplete="off"
          placeholder="Куда"
          class="el-input__inner ddd"
        />
      </div>
      <el-date-picker
        style="width: 250px; padding: 2px; height: 70px"
        v-model="date"
        type="daterange"
        range-separator=""
        start-placeholder="Start date"
        end-placeholder="End date"
        :default-time="['00:00:00', '23:59:59']"
      >
      </el-date-picker>
      <el-dropdown
        trigger="click"
        style="width: 150px; padding: 2px"
        @command="handleCommand"
      >
        <el-button
          style="
            line-height: 3;
            background-color: white;
            width: 150px;
            height: 70px;
          "
        >
          <div class="ad">
            {{ count ? count : "Пассажиры" }}
            <i class="el-icon-arrow-down el-icon--right"></i>
          </div>
        </el-button>
        <el-dropdown-menu slot="dropdown" style="width: 300px">
          <el-dropdown-item>
            <span>Взрослые</span>
            <el-input-number
              size="mini"
              v-model="num1"
              @change="handleChange"
              :min="0"
              :max="10"
            ></el-input-number
          ></el-dropdown-item>
          <el-dropdown-item>
            <span>Дети</span>
            <el-input-number
              size="mini"
              v-model="num2"
              @change="handleChange"
              :min="0"
              :max="10"
            ></el-input-number
          ></el-dropdown-item>
          <el-dropdown-item>
            <span>Младенцы</span>
            <el-input-number
              v-model="num3"
              size="mini"
              @change="handleChange"
              :min="0"
              :max="10"
            ></el-input-number
          ></el-dropdown-item>
          <el-dropdown-item divided>
            <el-radio v-model="radio" @change="handleType" label="Эконом"
              >Эконом</el-radio
            >
          </el-dropdown-item>
          <el-dropdown-item>
            <el-radio v-model="radio" @change="handleType" label="Комфорт"
              >Комфорт</el-radio
            >
          </el-dropdown-item>
          <el-dropdown-item>
            <el-radio v-model="radio" @change="handleType" label="Бизнес"
              >Бизнес</el-radio
            >
          </el-dropdown-item>
          <el-dropdown-item>
            <el-radio v-model="radio" @change="handleType" label="Первый класс"
              >Первый класс</el-radio
            >
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <el-button
        style="
          border: #ff6f32;
          background-color: #ff6f32;
          color: white;
          width: 150px;
          height: 70px;
        "
        round
        >НАЙТИ БИЛЕТЫ</el-button
      >
    </div>
    <div class="form-input" v-else>
      <div
        class="el-input"
        style="width: 300px; height: 70px; padding-right: 2px"
      >
        <input
          type="text"
          autocomplete="off"
          placeholder="Город или отель"
          class="el-input__inner ddd"
        />
      </div>
      <el-date-picker
        style="width: 250px; padding: 2px; height: 70px"
        v-model="date"
        type="daterange"
        range-separator=""
        start-placeholder="Заезд"
        end-placeholder="Выезд"
        :default-time="['00:00:00', '23:59:59']"
      >
      </el-date-picker>
      <el-dropdown
        trigger="click"
        style="width: 150px; padding: 2px"
        @command="handleCommand"
      >
        <el-button
          style="
            line-height: 3;
            background-color: white;
            width: 150px;
            height: 70px;
          "
        >
          <div class="ad">
            {{ countGuest ? countGuest + " гостей" : "Гости" }}
            <i class="el-icon-arrow-down el-icon--right"></i>
          </div>
        </el-button>
        <el-dropdown-menu slot="dropdown" style="width: 300px">
          <el-dropdown-item>
            <span>Взрослые</span>
            <el-input-number
              size="mini"
              v-model="guest1"
              @change="handleChangeGuest"
              :min="0"
              :max="10"
            ></el-input-number
          ></el-dropdown-item>
          <el-dropdown-item>
            <span>Дети</span>
            <el-input-number
              size="mini"
              v-model="guest2"
              @change="handleChangeGuest"
              :min="0"
              :max="10"
            ></el-input-number
          ></el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <el-button
        style="
          border: #ff6f32;
          background-color: #ff6f32;
          color: white;
          width: 150px;
          height: 70px;
        "
        round
        >НАЙТИ БИЛЕТЫ</el-button
      >
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      option: "Авиабилеты",
      value: "",
      date: "",
      radio: "Эконом",
      count: "",
      num1: 0,
      num2: 0,
      num3: 0,
      num4: 0,
      guest1: 0,
      guest2: 0,
      countGuest: 0,
    };
  },
  methods: {
    handleCommand() {
      this.count = this.value + " " + this.radio;
    },
    handleChange() {
      this.value = this.num1 + this.num2 + this.num3;
    },
    handleType() {
      this.handleCommand();
    },
    handleOption() {
      this.$emit("option", {
        option: this.option,
      });
    },
    handleChangeGuest() {
      this.countGuest = this.guest1 + this.guest2;
    },
  },
};
</script>
<style scoped>
.ddd {
  height: 100%;
}

.additional-fields__label {
  /* height: auto; */
  overflow: hidden;
  white-space: nowrap;
  /* height: 60px; */
  width: 100%;
  line-height: 2.625rem;
  position: relative;
  cursor: pointer;
}

.--is-gray {
  color: #a0b0b9;
}

.additional-fields {
  z-index: 2;
  box-sizing: border-box;
  height: 60px;
  width: 100%;
  line-height: 2.625rem;
  padding: 10px 15px;
  position: relative;
  box-shadow: inset 0 0 0 2px transparent;
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  user-select: none;
  border-radius: 0 10px 10px 0;
}

.form-input {
  margin-top: 20px;
}
</style>
