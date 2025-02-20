<template>
  <div class="container mx-auto">
    <TabView :activeIndex="activeTab" @tab-change="handleTabChange" class="mt-8">
      <TabPanel header="Ozbargain">
        <ozb-results ref="ozbResults" :isActive="activeTab === 0" />
      </TabPanel>
      <TabPanel header="Coles">
        <coles-results ref="colesResults" :isActive="activeTab === 1" />
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

:deep(.p-tabview) {
  padding: 0 1rem;
}

@media screen and (max-width: 640px) {
  .container {
    padding: 0;
  }

  :deep(.p-tabview-nav li) {
    margin: 0 0.25rem;
  }

  :deep(.p-tabview-nav-link) {
    padding: 0.5rem !important;
  }
}
</style>
