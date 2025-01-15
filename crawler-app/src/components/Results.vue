<template>
  <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-7xl">
    <TabView :activeIndex="activeTab" @tab-change="handleTabChange" class="mt-8">
      <TabPanel header="Ozbargain">
        <ozb-results ref="ozbResults" />
      </TabPanel>
      <TabPanel header="Coles">
        <coles-results ref="colesResults" />
      </TabPanel>
    </TabView>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeTab: 0
    }
  },
  mounted() {
    // Get stored tab index or default to 0
    const storedTab = parseInt(localStorage.getItem('activeTab') || '0');
    this.activeTab = storedTab;

    // Load data for initial tab
    this.$nextTick(() => {
      if (storedTab === 0) {
        this.$refs.ozbResults?.loadData();
      } else {
        this.$refs.colesResults?.loadData();
      }
    });
  },
  methods: {
    handleTabChange(e) {
      this.activeTab = e.index;
      localStorage.setItem('activeTab', e.index.toString());

      if (e.index === 0) {
        this.$refs.ozbResults?.loadData();
      } else {
        this.$refs.colesResults?.loadData();
      }
    }
  }
}
</script>

<style scoped>
:deep(.p-tabview-nav) {
  justify-content: center;
}
</style>
