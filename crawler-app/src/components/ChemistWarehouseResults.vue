<template>
  <RetailerResults
    ref="retailer"
    :is-active="isActive"
    :data-url="chemistWarehouseDataUrl"
    title="Chemist Warehouse deals"
    badge="Chemist Warehouse"
    empty-name="Chemist Warehouse"
    placeholder="Search Chemist Warehouse specials"
    kicker="Pharmacy specials"
    accent="#1d4ed8"
    accent-soft="#eff6ff"
    accent-ink="#1e40af"
    accent-border="rgba(29, 78, 216, 0.34)"
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
      chemistWarehouseDataUrl: import.meta.env.VITE_CHEMIST_WAREHOUSE_CRAWLER_URL
    };
  },
  methods: {
    loadData() {
      this.$refs.retailer?.loadData();
    }
  }
};
</script>
