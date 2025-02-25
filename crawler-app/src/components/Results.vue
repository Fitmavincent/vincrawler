<template>
  <div class="container mx-auto">
    <TabView :activeIndex="activeTab" @tab-change="handleTabChange" class="mt-8">
      <TabPanel header="Ozbargain">
        <ozb-results ref="ozbResults" :isActive="activeTab === 0" />
      </TabPanel>
      <TabPanel header="Coles">
        <coles-results ref="colesResults" :isActive="activeTab === 1" />
      </TabPanel>
      <TabPanel header="Woolies">
        <woolies-results ref="wooliesResults" :isActive="activeTab === 2" />
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
      } else if (storedTab === 1) {
        this.$refs.colesResults?.loadData();
      } else {
        this.$refs.wooliesResults?.loadData();
      }
    });
  },
  methods: {
    handleTabChange(e) {
      this.activeTab = e.index;
      localStorage.setItem('activeTab', e.index.toString());

      if (e.index === 0) {
        this.$refs.ozbResults?.loadData();
      } else if (e.index === 1) {
        this.$refs.colesResults?.loadData();
      } else {
        this.$refs.wooliesResults?.loadData();
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
