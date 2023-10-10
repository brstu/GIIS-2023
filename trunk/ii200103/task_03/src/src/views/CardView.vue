<template>
  <div>
    <div class="f-layout-card">
      <div class="form-input">
        <div
          class="el-input"
          style="width: 200px; height: 70px; padding-right: 2px"
        >
          <input
            value="Нью-Йорк"
            type="text"
            autocomplete="off"
            placeholder="Откуда"
            class="el-input__inner ddd"
          />
        </div>
        <div class="el-input" style="width: 200px; height: 70px; padding: 2px">
          <input
            value="Санто-Доминго"
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
              <el-radio
                v-model="radio"
                @change="handleType"
                label="Первый класс"
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
    </div>
    <el-card class="box-card" style="height: 80px">
      <div class="tag-group">
        <el-tag
          style="width: 150px; height: 45px"
          v-for="item in items"
          :key="item.label"
          :type="item.type"
          effect="plain"
        >
          <div class="cost-first" style="color: black; height: 15px">
            {{ item.label }}
          </div>
          <div class="date" style="color: black">{{ item.date }}</div>
        </el-tag>
        <el-button
          type="primary"
          style="position: absolute; height: 45px; margin-left: 10px"
        >
          Показать<i class="el-icon-arrow-down el-icon--right"></i>
        </el-button>
      </div>
    </el-card>
    <div class="boxs">
      <el-card class="box-card-left">
        <div slot="header" class="clearfix">
          <span class="checkboxs-title">Пересадки</span>
        </div>
        <div class="checkboxs">
          <el-checkbox style="padding: 10px"
            ><span class="checkboxs-text">Без пересадок</span></el-checkbox
          >
          <el-checkbox style="padding: 10px"
            ><span class="checkboxs-text">1 пересадка</span></el-checkbox
          >
          <el-checkbox style="padding: 10px"
            ><span class="checkboxs-text">2 пересадки</span></el-checkbox
          >
          <el-checkbox style="padding: 10px"
            ><span class="checkboxs-text">3 пересадки</span></el-checkbox
          >
        </div>
        <div style="margin-top: 20px">
          <span class="checkboxs-title">Длительность пересадки</span>
          <el-steps :active="active" align-center style="margin-top: 20px">
            <el-step title="4 часа"></el-step>
            <el-step title="8 часов"></el-step>
            <el-step title="12 часов"></el-step>
          </el-steps>
          <el-button size="small" style="margin-top: 12px" @click="next"
            >Увеличить</el-button
          >
        </div>
        <div style="margin-top: 20px">
          <span class="checkboxs-title">Если комфорт важнее</span>
          <div style="margin-top: 20px; display: grid">
            <span class="el-dropdown-link checkboxs-text">
              Вылет в Санто-Доминго<i
                class="el-icon-arrow-down el-icon--right"
              ></i>
            </span>
            <span class="el-dropdown-link checkboxs-text">
              Обратно в Нью-Йорк<i
                class="el-icon-arrow-down el-icon--right"
              ></i>
            </span>
            <span class="el-dropdown-link checkboxs-text">
              Багаж<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <span class="el-dropdown-link checkboxs-text">
              Авиакомпании<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <span class="el-dropdown-link checkboxs-text">
              Альянсы<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <span class="el-dropdown-link checkboxs-text">
              Время в пути<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <span class="el-dropdown-link checkboxs-text">
              Аэропорты пересадок<i
                class="el-icon-arrow-down el-icon--right"
              ></i>
            </span>
            <span class="el-dropdown-link checkboxs-text">
              Аэропорты в Нью-Йорке<i
                class="el-icon-arrow-down el-icon--right"
              ></i>
            </span>
            <span class="el-dropdown-link checkboxs-text">
              Аэропорты в Санто-Доминго<i
                class="el-icon-arrow-down el-icon--right"
              ></i>
            </span>
            <span class="el-dropdown-link checkboxs-text">
              Стоимость<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <span class="el-dropdown-link checkboxs-text">
              Агенства<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <span class="el-dropdown-link checkboxs-text">
              Способ оплаты<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <span class="el-dropdown-link checkboxs-text">
              Сортировка<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
          </div>
        </div>
      </el-card>
      <div class="boxs-card-center">
        <el-card class="box-card-center">
          <div class="text item">
            <span class="card-center-title">Прямые рейсы</span>
            <div class="box-card-center-drop">
              <div>
                <span class="el-dropdown-link" style="display: flex">
                  <img
                    alt="B6"
                    class="image-drop"
                    src="//mpics.avs.io/al_square/36/36/B6.png" /><span
                    class="name-air"
                    >JetBlue Airways</span
                  ><i class="el-icon-arrow-right" style="margin-left: auto"></i
                ></span>
              </div>
              <div class="available">
                <span class="date">10 окт</span
                ><span class="time">06:05 09:30 12:00 20:40 22:59</span>
              </div>
              <div class="available2">
                <span class="date">15 окт</span
                ><span class="time">01:40 06:05 11:08 14:28 17:15</span>
              </div>
              <div>
                <span class="el-dropdown-link" style="display: flex">
                  <img
                    alt="UA"
                    class="image-drop"
                    src="//mpics.avs.io/al_square/36/36/UA.png" /><span
                    class="name-air"
                    >United Airlines</span
                  ><i class="el-icon-arrow-right" style="margin-left: auto"></i
                ></span>
              </div>
              <div class="available">
                <span class="date">10 окт</span
                ><span class="time">08:08 10:00 21:47</span>
              </div>
              <div>
                <span class="date">15 окт</span
                ><span class="time">06:00 13:05 15:05</span>
              </div>
            </div>
          </div>
        </el-card>
        <el-card class="box-card-center">
          <div class="card-routes">
            <div class="price-block">
              <span class="price">$419</span>
              <span class="baggage">Без багажа</span>
              <el-button type="warning" style="margin-top: 15px; height: 50px"
                >Выбрать билет</el-button
              >
              <span class="count-ticket">Осталось 7 билетов по этой цене</span>
            </div>
            <div class="detail">
              <div>
                <span
                  class="el-dropdown-link"
                  style="display: flex"
                  @click="dialogVisible = true"
                >
                  <img
                    alt="B6"
                    class="image-detail"
                    src="//mpics.avs.io/al_square/36/36/B6.png" /><span
                    class="name-air"
                    >JetBlue Airways</span
                  ><i class="el-icon-upload2" style="margin-left: auto"></i
                ></span>
              </div>
              <div class="more-detail">
                <div class="departure">
                  <div class="d-time">
                    <i
                      class="el-icon-edit-outline"
                      style="font-size: 25px; color: gray; padding-right: 10px"
                    ></i
                    >20:40
                  </div>
                  <span class="d-port">Нью-Йорк</span>
                  <span class="d-date">10 окт, вт</span>
                </div>
                <div class="picker">
                  <el-slider v-model="value" range :marks="marks1"> </el-slider>
                </div>
                <div class="arrival">
                  <div class="a-time">00:37</div>
                  <span class="a-port">Санто-Доминго</span>
                  <span class="a-date">11 окт, ср</span>
                </div>
              </div>
              <div class="more-detail" style="border: none">
                <div class="departure">
                  <div class="d-time">
                    <i
                      class="el-icon-edit-outline"
                      style="font-size: 25px; color: gray; padding-right: 10px"
                    ></i
                    >11:08
                  </div>
                  <span class="d-port">Санто-Доминго</span>

                  <span class="d-date">15 окт, вс</span>
                </div>
                <div class="picker">
                  <el-slider v-model="value" range :marks="marks2"> </el-slider>
                </div>
                <div class="arrival">
                  <div class="a-time">14:59</div>
                  <span class="a-port">Нью-Йорк</span>
                  <span class="a-date">15 окт, вс</span>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </div>
    <el-dialog :visible.sync="dialogVisible" width="70%">
      <div class="dialog-content">
        <div class="dialog-content-left">
          <el-button style="width: 100%; margin-bottom: 30px">
            Багаж оплачивается отдельно
          </el-button>
          <div class="dialog-content-text">
            <span class="path-to">Нью-Йорк - Санто-Доминго</span>
            <span>в пути 3ч. 59мин. </span>
          </div>
          <el-card class="box-card" style="margin-bottom: 30px">
            <span class="el-dropdown-link" style="display: flex">
              <img
                alt="B6"
                class="image-card"
                src="//mpics.avs.io/al_square/36/36/B6.png"
              /><span class="dialog-name-air">JetBlue Airways</span
              ><el-button size="mini" style="margin-left: auto">
                Подробнее
              </el-button></span
            >
            <div class="content-card">
              <div class="timespicker">
                <el-timeline
                  :reverse="reverse"
                  style="margin-top: 30px; padding-left: 0px"
                >
                  <el-timeline-item
                    v-for="(activity, index) in activities1"
                    :key="index"
                    :timestamp="activity.timestamp"
                  >
                    {{ activity.content }}
                  </el-timeline-item>
                </el-timeline>
              </div>
              <div class="name-routes">
                <span class="route-city">Нью-Йорк</span>
                <span class="route-airport">Кеннеди, JFK</span>

                <span class="route-city">Санто-Доминго</span>
                <span class="route-airport">Лас-Америкас, SDQ</span>
              </div>
            </div>
          </el-card>
          <div class="dialog-content-text">
            <span class="path-to">Нью-Йорк - Санто-Доминго</span>
            <span>в пути 4ч. </span>
          </div>
          <el-card class="box-card">
            <span class="el-dropdown-link" style="display: flex">
              <img
                alt="B6"
                class="image-card"
                src="//mpics.avs.io/al_square/36/36/B6.png"
              /><span class="dialog-name-air">JetBlue Airways</span
              ><el-button size="mini" style="margin-left: auto">
                Подробнее
              </el-button></span
            >
            <div class="content-card">
              <div class="timespicker">
                <el-timeline
                  :reverse="reverse"
                  style="margin-top: 30px; padding-left: 0px"
                >
                  <el-timeline-item
                    v-for="(activity, index) in activities2"
                    :key="index"
                    :timestamp="activity.timestamp"
                  >
                    {{ activity.content }}
                  </el-timeline-item>
                </el-timeline>
              </div>
              <div class="name-routes">
                <span class="route-city">Санто-Доминго</span>
                <span class="route-airport">Лас-Америкас, SDQ</span>
                <span class="route-city">Нью-Йорк</span>
                <span class="route-airport">Кеннеди, JFK</span>
              </div>
            </div>
          </el-card>
        </div>
        <div class="dialog-content-right">
          <el-card class="box-card">
            <div class="actual-prices">
              <img
                class="price-image"
                src="https://pics.aviasales.com/as_gates_square/us/72/72/74.png"
                alt=""
              />
              <div class="actual-price">
                <span class="cost">$214,2</span>
                <span class="where">на сайте Expedia</span>
              </div>
              <el-button style="width: 100px; margin-left: auto" type="danger"
                >Купить</el-button
              >
            </div>
            <div class="actual-prices">
              <img
                class="price-image"
                src="https://pics.aviasales.com/as_gates_square/us/72/72/203.png"
                alt=""
              />
              <div class="actual-price">
                <span class="cost">$214,2</span>
                <span class="where">на сайте Expedia</span>
              </div>
              <el-button style="width: 100px; margin-left: auto" type="danger"
                >Купить</el-button
              >
            </div>
            <div class="actual-prices">
              <img
                class="price-image"
                src="https://pics.aviasales.com/as_gates_square/us/72/72/308.png"
                alt=""
              />
              <div class="actual-price">
                <span class="cost">$214,2</span>
                <span class="where">на сайте Expedia</span>
              </div>
              <el-button style="width: 100px; margin-left: auto" type="danger"
                >Купить</el-button
              >
            </div>
          </el-card>
        </div>
      </div>
    </el-dialog>
  </div>
</template>
<script>
export default {
  data() {
    return {
      option: "Авиабилеты",
      date: "",
      radio: "Эконом",
      count: "",
      num1: 0,
      num2: 0,
      num3: 0,
      num4: 0,
      guest1: 0,
      guest2: 0,
      active: 0,
      countGuest: 0,
      reverse: true,
      activities1: [
        {
          content: "20:24",
          timestamp: "6 янв, сб",
        },
        {
          content: "01:23",
          timestamp: "7 янв, вс",
        },
      ],
      activities2: [
        {
          content: "05:40",
          timestamp: "24 янв, ср",
        },
        {
          content: "08:40",
          timestamp: "24 янв, ср",
        },
      ],
      dialogVisible: false,
      value: [0, 100],
      marks1: {
        50: "в пути 3ч 57мин",
      },
      marks2: {
        50: "в пути 3ч 51мин",
      },
      items: [
        { type: "", label: "$274", date: "12" },
        { type: "", label: "$326", date: "12" },
        { type: "", label: "$393", date: "12" },
        { type: "", label: "$237", date: "12" },
        { type: "", label: "$213", date: "12" },
        { type: "", label: "$333", date: "12" },
      ],
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
    next() {
      if (this.active++ > 2) this.active = 0;
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
.s__WaWgAuCv1vslQpx27wX1.s__mlYQnUrIb9V10lJFDIrT {
  width: 60px;
}
.s__WaWgAuCv1vslQpx27wX1 {
  flex-shrink: 0;
  position: relative;
  top: 2px;
  width: 30px;
}
.s__jiLviG4Pt5t3kC2y1PCf:last-child {
  margin-right: 0;
}
.s__jiLviG4Pt5t3kC2y1PCf:first-child {
  box-shadow: none;
}

img {
  max-width: 100%;
}
</style>
