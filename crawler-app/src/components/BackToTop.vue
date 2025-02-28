<template>
  <Button
    v-show="visible"
    class="pi pi-arrow-up back-to-top p-button-rounded p-button-secondary"
    @click="scrollToTop"
  />
</template>

<script>
export default {
  data() {
    return {
      visible: false
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      this.visible = window.scrollY > 300
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }
}
</script>

<style scoped>
.back-to-top {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 999;
  margin-bottom: 5rem;
  font-size: x-large;
  }
</style>
