<template>
  <div>
    <FormContainer @option="onOption" />
    <div>
      <div data-selene-widget="seo_who_we_are">
        <section class="section" v-if="option.toString() == 'Авиабилеты'">
          <header class="header-text">
            <p class="first-text" data-test-id="text">
              Мы не&nbsp;продаём авиабилеты, а&nbsp;помогаем найти самые
              дешёвые. Бесплатно.
              <el-button
                v-if="!textMore"
                @click="textMore = true"
                type="text"
                style="font-size: 18px"
                >Читать полностью</el-button
              >
            </p>
          </header>
          <div class="second-text" v-if="textMore">
            <p>
              Aviasales&nbsp;— лучший поисковик авиабилетов. Мы&nbsp;сравниваем
              все доступные варианты перелётов по&nbsp;вашему запросу,
              а&nbsp;потом направляем вас для покупки на&nbsp;официальные сайты
              авиакомпаний и&nbsp;агентств.
            </p>
            <p>
              Стоимость авиабилета, которую вы&nbsp;видите
              на&nbsp;Aviasales&nbsp;— финальная. Мы&nbsp;убрали все скрытые
              услуги и&nbsp;галочки.
            </p>
          </div>
        </section>
      </div>
      <div class="popular-routes">
        <div class="icon">
          <img
            data-src="https://static.aviasales.com/helios-assets/home_popular_directions/title_icon.svg"
            src="https://static.aviasales.com/helios-assets/home_popular_directions/title_icon.svg"
            data-loaded="true"
            alt="icon_image"
          />
        </div>
        <div class="popular-route-text">
          <p>Популярные направления</p>
        </div>
        <div class="popular-route-dropdown">
          <div class="main-popular-directions__destinations">
            <div class="main-popular-directions__destination">
              <div class="main-popular-directions__destination-header">
                <div class="main-popular-directions__destination-flag">
                  <div class="flag">
                    <img
                      data-src="https://static.aviasales.com/helios-assets/flag/do.png"
                      src="https://static.aviasales.com/helios-assets/flag/do.png"
                      data-loaded="true"
                      alt="flag_image"
                    />
                  </div>
                </div>
                <el-dropdown trigger="click" style="width: 200px">
                  <el-button>
                    Доминиканская Республика<i
                      class="el-icon-arrow-down el-icon--right"
                    ></i>
                  </el-button>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item
                      ><div class="main-popular-directions__destination-route">
                        <router-link
                          to="/search"
                          class="main-popular-directions__destination-route-link"
                          data-goal="route"
                          target="_blank"
                          title="Авиабилеты Нью-Йорк — Санто-Доминго"
                        >
                          <span
                            class="main-popular-directions__destination-route-name"
                          >
                            Нью-Йорк - Санто-Доминго</span
                          >
                          <span
                            class="main-popular-directions__destination-route-price"
                          >
                            от
                            <span
                              class="currency-element"
                              data-role="currency-element"
                              data-value="24163"
                              ><span class="currency-font --usd">$</span
                              >243</span
                            ></span
                          ></router-link
                        >
                      </div></el-dropdown-item
                    >
                    <el-dropdown-item
                      ><div class="main-popular-directions__destination-route">
                        <a
                          class="main-popular-directions__destination-route-link"
                          data-goal="route"
                          href="/search/MIA0309SDQ06091"
                          target="_blank"
                          title="Авиабилеты Майами — Санто-Доминго туда-обратно"
                        >
                          <span
                            class="main-popular-directions__destination-route-name"
                          >
                            Майами - Санто-Доминго</span
                          >
                          <span
                            class="main-popular-directions__destination-route-price"
                          >
                            от
                            <span
                              class="currency-element"
                              data-role="currency-element"
                              data-value="15145"
                              ><span class="currency-font --usd">$</span
                              >152</span
                            ></span
                          ></a
                        >
                      </div></el-dropdown-item
                    >
                    <el-dropdown-item
                      ><div class="main-popular-directions__destination-route">
                        <a
                          class="main-popular-directions__destination-route-link"
                          data-goal="route"
                          href="/search/ORL1110SDQ23101"
                          target="_blank"
                          title="Авиабилеты Орландо — Санто-Доминго туда-обратно"
                        >
                          <span
                            class="main-popular-directions__destination-route-name"
                          >
                            Орландо - Санто-Доминго</span
                          >
                          <span
                            class="main-popular-directions__destination-route-price"
                          >
                            от
                            <span
                              class="currency-element"
                              data-role="currency-element"
                              data-value="16164"
                              ><span class="currency-font --usd">$</span
                              >162</span
                            ></span
                          ></a
                        >
                      </div></el-dropdown-item
                    >
                  </el-dropdown-menu>
                </el-dropdown>
              </div>
            </div>
            <div
              class="main-popular-directions__destination"
              style="margin-left: 45px"
            >
              <div class="main-popular-directions__destination-header">
                <div class="main-popular-directions__destination-flag">
                  <div class="flag">
                    <img
                      data-src="https://static.aviasales.com/helios-assets/flag/fr.png"
                      src="https://static.aviasales.com/helios-assets/flag/fr.png"
                      data-loaded="true"
                      alt="flag_image_second"
                    />
                  </div>
                </div>
                <el-dropdown trigger="click" style="width: 200px">
                  <el-button style="width: 100%">
                    Франция<i class="el-icon-arrow-down el-icon--right"></i>
                  </el-button>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item
                      ><div class="main-popular-directions__destination-route">
                        <a
                          class="main-popular-directions__destination-route-link"
                          data-goal="route"
                          href="/search/NYC1303PAR17031"
                          target="_blank"
                          title="Авиабилеты Нью-Йорк — Париж туда-обратно"
                        >
                          <span
                            class="main-popular-directions__destination-route-name"
                          >
                            Нью-Йорк - Париж</span
                          >
                          <span
                            class="main-popular-directions__destination-route-price"
                          >
                            от
                            <span
                              class="currency-element"
                              data-role="currency-element"
                              data-value="35823"
                              ><span class="currency-font --usd">$</span
                              >360</span
                            ></span
                          ></a
                        >
                      </div></el-dropdown-item
                    >
                    <el-dropdown-item
                      ><div class="main-popular-directions__destination-route">
                        <a
                          class="main-popular-directions__destination-route-link"
                          data-goal="route"
                          href="/search/LAX0411PAR20111"
                          target="_blank"
                          title="Авиабилеты Лос-Анджелес — Париж туда-обратно"
                        >
                          <span
                            class="main-popular-directions__destination-route-name"
                          >
                            Лос-Анджелес - Париж</span
                          >
                          <span
                            class="main-popular-directions__destination-route-price"
                          >
                            от
                            <span
                              class="currency-element"
                              data-role="currency-element"
                              data-value="49154"
                              ><span class="currency-font --usd">$</span
                              >495</span
                            ></span
                          ></a
                        >
                      </div></el-dropdown-item
                    >
                    <el-dropdown-item
                      ><div class="main-popular-directions__destination-route">
                        <a
                          class="main-popular-directions__destination-route-link"
                          data-goal="route"
                          href="/search/SFO1303PAR17031"
                          target="_blank"
                          title="Авиабилеты Сан-Франциско — Париж туда-обратно"
                        >
                          <span
                            class="main-popular-directions__destination-route-name"
                          >
                            Сан-Франциско - Париж</span
                          >
                          <span
                            class="main-popular-directions__destination-route-price"
                          >
                            от
                            <span
                              class="currency-element"
                              data-role="currency-element"
                              data-value="43566"
                              ><span class="currency-font --usd">$</span
                              >439</span
                            ></span
                          ></a
                        >
                      </div></el-dropdown-item
                    >
                  </el-dropdown-menu>
                </el-dropdown>
              </div>
            </div>
            <div class="main-popular-directions__destination">
              <div class="main-popular-directions__destination-header">
                <div class="main-popular-directions__destination-flag">
                  <div class="flag">
                    <img
                      data-src="https://static.aviasales.com/helios-assets/flag/pr.png"
                      src="https://static.aviasales.com/helios-assets/flag/pr.png"
                      data-loaded="true"
                      alt="flag_image_third"
                    />
                  </div>
                </div>
                <el-dropdown trigger="click" style="width: 200px">
                  <el-button style="width: 100%">
                    Пуэрто-Рико<i class="el-icon-arrow-down el-icon--right"></i>
                  </el-button>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item
                      ><div class="main-popular-directions__destination-route">
                        <a
                          class="main-popular-directions__destination-route-link"
                          data-goal="route"
                          href="/search/NYC2110SJU25101"
                          target="_blank"
                          title="Авиабилеты Нью-Йорк — Сан-Хуан туда-обратно"
                        >
                          <span
                            class="main-popular-directions__destination-route-name"
                          >
                            Нью-Йорк - Сан-Хуан</span
                          >
                          <span
                            class="main-popular-directions__destination-route-price"
                          >
                            от
                            <span
                              class="currency-element"
                              data-role="currency-element"
                              data-value="12898"
                              ><span class="currency-font --usd">$</span
                              >129</span
                            ></span
                          ></a
                        >
                      </div></el-dropdown-item
                    >
                    <el-dropdown-item
                      ><div class="main-popular-directions__destination-route">
                        <a
                          class="main-popular-directions__destination-route-link"
                          data-goal="route"
                          href="/search/ORL0709SJU12091"
                          target="_blank"
                          title="Авиабилеты Орландо — Сан-Хуан туда-обратно"
                        >
                          <span
                            class="main-popular-directions__destination-route-name"
                          >
                            Орландо - Сан-Хуан</span
                          >
                          <span
                            class="main-popular-directions__destination-route-price"
                          >
                            от
                            <span
                              class="currency-element"
                              data-role="currency-element"
                              data-value="10579"
                              ><span class="currency-font --usd">$</span
                              >106</span
                            ></span
                          ></a
                        >
                      </div></el-dropdown-item
                    >
                    <el-dropdown-item
                      ><div class="main-popular-directions__destination-route">
                        <a
                          class="main-popular-directions__destination-route-link"
                          data-goal="route"
                          href="/search/PHL0610SJU12101"
                          target="_blank"
                          title="Авиабилеты Филадельфия — Сан-Хуан туда-обратно"
                        >
                          <span
                            class="main-popular-directions__destination-route-name"
                          >
                            Филадельфия - Сан-Хуан</span
                          >
                          <span
                            class="main-popular-directions__destination-route-price"
                          >
                            от
                            <span
                              class="currency-element"
                              data-role="currency-element"
                              data-value="9175"
                              ><span class="currency-font --usd">$</span
                              >92</span
                            ></span
                          ></a
                        >
                      </div></el-dropdown-item
                    >
                  </el-dropdown-menu>
                </el-dropdown>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="footer --small" data-goal-category="footer">
      <div class="footer__bottom">
        <div class="footer__inner">
          <div class="footer__side-spaces">
            <ul
              class="footer__links-list --about"
              data-goal-category="footer_links"
            >
              <li><a href="/terms-of-use" rel="">Правила</a></li>
              <li><a data-goal="help" href="/faq" rel="">Поддержка</a></li>
              <li>
                <a data-goal="privacy" href="/privacy" rel=""
                  >Политика конфиденциальности</a
                >
              </li>
              <li>
                <a data-goal="cookie" href="/cookie" rel=""
                  >Политика в отношении файлов cookie</a
                >
              </li>
            </ul>

            <div class="footer__copy">© 2007–2023, Aviasales</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FormContainer from "@/components/FormContainer.vue";

export default {
  data() {
    return {
      option: "Авиабилеты",
      textMore: false,
    };
  },
  components: {
    FormContainer,
  },
  methods: {
    onOption(data) {
      this.option = data.option;
    },
  },
};
</script>
<style scoped>
.section {
  border-radius: 14px;
  margin-bottom: 40px;
  margin-left: 20px;
  margin-right: 20px;
  max-width: 800px;
  padding: 16px;
  /* margin: 0 auto 40px; */
  padding-left: 24px;
  padding-right: 24px;
}
.second-text {
  padding-bottom: 12px;
  /* font-family: black; */
  font-weight: 400;
  font-size: 17px;
  line-height: 22px;
}
.first-text {
  font-size: 19px;
  line-height: 25px;
  margin-bottom: 0;
  margin-top: 0;
  text-align: center;
}
.header-text {
  display: grid;
  grid-template-columns: auto;
  grid-template-rows: auto auto;
}
</style>
