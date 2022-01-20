<template>
  <div>
    <h1 class="text-3xl font-bold">Ozb Crawl Result</h1>  
    <data-table :value="results" responsiveLayout="scroll">
      <template #header>
        <div class="table-header flex items-left">
            Products
            <Button icon="pi pi-refresh" />
        </div>
      </template>      
      <column field="name" header="Name">
        <template #body="slotProps">
            <a :href="slotProps.data.link" target="_blank" rel="noreferrer noopener">{{slotProps.data.name}}</a>
        </template>
      </column>
      <column field="price" header="Price">
      </column>
      <column field="link" header="Link">
        <template #body="slotProps">
          <a :href="slotProps.data.link" target="_blank" rel="noreferrer noopener">{{slotProps.data.link}}</a>
        </template>
      </column>
      <column field="time" header="Post time">
      </column>
    </data-table>
  </div>
</template>


<script>
export default {
  data() {
    return {
      resultUrl: import.meta.env.VITE_OZB_CRAWLER_URL,
      results: null,
    };
  },
  created() {
    
  },
  mounted() {
    this.getCrawlerResult();
  },
  methods: {
    getCrawlerResult() {
      this.axios.get(this.resultUrl).then((res) => {
        if(res.data){
          this.results = res.data.items;
        }
      });
    },
  },
};
</script>


<style lang="">
</style>