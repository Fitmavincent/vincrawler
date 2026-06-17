<template>
  <RetailerResults
    ref="retailer"
    :is-active="isActive"
    :data-url="pricelineDataUrl"
    title="Priceline deals"
    badge="Priceline"
    empty-name="Priceline"
    placeholder="Search Priceline specials"
    kicker="Pharmacy specials"
    accent="#d81b60"
    accent-soft="#fdf2f8"
    accent-ink="#be185d"
    accent-border="rgba(216, 27, 96, 0.34)"
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
      pricelineDataUrl: import.meta.env.VITE_PRICELINE_CRAWLER_URL
    };
  },
  methods: {
    loadData() {
      this.$refs.retailer?.loadData();
    }
  }
};
</script>
