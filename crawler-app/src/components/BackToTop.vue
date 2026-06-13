<template>
  <Button
    v-show="visible"
    class="pi pi-arrow-up back-to-top p-button-rounded"
    aria-label="Back to top"
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
  right: 1.25rem;
  bottom: 1.25rem;
  z-index: 999;
  width: 3rem;
  height: 3rem;
  border: 0;
  background: #0f172a;
  box-shadow: 0 18px 44px rgba(15, 23, 42, 0.28);
  font-size: 1rem;
}
</style>
