<template>
  <div id="app">
    <component :is="layout">
      <router-view />
    </component>
  </div>
</template>

<script>
import MainLayout from "./layout/MainLayout.vue";
export default {
  components: {
    MainLayout,
  },
  computed: {
    layout() {
      return (this.$route.meta.layout || "Main") + "Layout";
    },
  },
};
</script>
