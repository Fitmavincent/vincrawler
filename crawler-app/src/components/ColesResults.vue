<template>
  <RetailerResults
    ref="retailer"
    :is-active="isActive"
    :data-url="colesDataUrl"
    title="Coles deals"
    badge="Coles"
    empty-name="Coles"
    placeholder="Search Coles specials"
    kicker="Supermarket crawler"
    accent="#e01a22"
    accent-soft="#fff1f2"
    accent-ink="#9f1239"
    accent-border="rgba(224, 26, 34, 0.34)"
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
      colesDataUrl: import.meta.env.VITE_COLES_CRAWLER_URL
    };
  },
  methods: {
    loadData() {
      this.$refs.retailer?.loadData();
    }
  }
};
</script>
