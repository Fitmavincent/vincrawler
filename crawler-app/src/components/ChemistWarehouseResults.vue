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
    accent="#0054a6"
    accent-soft="#eef6ff"
    accent-ink="#003f7d"
    accent-border="rgba(0, 84, 166, 0.34)"
    secondary-accent="#e31e24"
    tertiary-accent="#ffd200"
    brand-strip
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
