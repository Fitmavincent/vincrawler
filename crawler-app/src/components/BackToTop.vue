<template>
  <button
    v-show="visible"
    class="back-to-top"
    aria-label="Back to top"
    type="button"
    @click="scrollToTop"
  >
    <i class="pi pi-arrow-up" aria-hidden="true"></i>
  </button>
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
  z-index: 1000;
  display: grid;
  width: 3rem;
  height: 3rem;
  place-items: center;
  border: 1px solid rgba(180, 83, 9, 0.2);
  border-radius: 999px;
  color: #78350f;
  background: #ffffff;
  box-shadow: 0 18px 44px rgba(15, 23, 42, 0.2);
  transition: transform 160ms ease, box-shadow 160ms ease, background-color 160ms ease;
}

.back-to-top:hover {
  background: #fffbeb;
  box-shadow: 0 22px 50px rgba(15, 23, 42, 0.24);
  transform: translateY(-2px);
}

.back-to-top:focus-visible {
  outline: 3px solid rgba(245, 158, 11, 0.35);
  outline-offset: 3px;
}

.back-to-top i {
  color: currentColor;
  font-size: 1rem;
  line-height: 1;
}

@media screen and (max-width: 640px) {
  .back-to-top {
    right: 1rem;
    bottom: 1rem;
    width: 2.75rem;
    height: 2.75rem;
  }
}
</style>
