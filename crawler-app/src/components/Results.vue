<template>
  <div>
    <TabView @tab-change="handleTabChange">
      <TabPanel header="Ozbargain">
        <ozb-results />
      </TabPanel>
      <TabPanel header="Coles">
        <coles-results ref="colesResults" />
      </TabPanel>
    </TabView>
  </div>
</template>

<script>
export default {
  methods: {
    handleTabChange(e) {
      if (e.index === 1) { // Coles tab index
        this.$refs.colesResults?.loadData();
      }
    }
  }
}
</script>

<style scoped>

</style>
