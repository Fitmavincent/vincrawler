<template>
  <RetailerResults
    ref="retailer"
    :is-active="isActive"
    :data-url="wooliesDataUrl"
    title="Woolworths deals"
    badge="Woolies"
    empty-name="Woolworths"
    placeholder="Search Woolworths specials"
    kicker="Supermarket crawler"
    accent="#178841"
    accent-soft="#ecfdf5"
    accent-ink="#047857"
    accent-border="rgba(23, 136, 65, 0.34)"
  />
</template>

<script>
export default {
  props: {
    isActive: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      wooliesDataUrl: import.meta.env.VITE_WOOLIES_CRAWLER_URL
    };
  },
  methods: {
    loadData() {
      this.$refs.retailer?.loadData();
    }
  }
};
</script>
