<template>
  <div>
    <loading v-model:active="isLoading"
      :can-cancel="true"
      :on-cancel="onCancel"
      :is-full-page="fullPage"
    />

    <div>
      <h1 class="text-3xl font-bold">Ozb Channel</h1>  
      <data-table :resizableColumns="false" columnResizeMode="expand" :value="results" responsiveLayout="scroll">
        <template #header>
          <div class="table-header flex items-left">
              Products            
          </div>
        </template>
        <input-text type="text" placeholder="Search" v-model="search" v-debounce:500ms="searchResult" :debounce-events="['keyup', 'tab']"/>
        <column field="image" header="Image">
          <template #body="slotProps">
            <a :href="slotProps.data.link" target="_blank" rel="noreferrer noopener">
              <img class="object-contain h-24 w-24" :src="slotProps.data.image" :alt="slotProps.data.image">
            </a>
          </template>
        </column>
        <column field="name" header="Name">
          <template #body="slotProps">
              <a :href="slotProps.data.link" target="_blank" rel="noreferrer noopener">{{slotProps.data.tag ?? ''}} {{slotProps.data.name}}</a>
          </template>
        </column>
        <column field="price" header="Price">
          <template #body="slotProps">
              <a :href="slotProps.data.node_url" target="_blank" rel="noreferrer noopener">{{slotProps.data.price}}</a>
          </template>
        </column>
        <!-- <column field="link" header="Link">
          <template #body="slotProps">
            <a :href="slotProps.data.link" target="_blank" rel="noreferrer noopener">{{slotProps.data.link}}</a>
          </template>
        </column> -->
        <column field="time" header="Post time">
        </column>
      </data-table>
    </div>   
  </div>
</template>


<script>
export default {
  data() {
    return {
      resultUrl: import.meta.env.VITE_OZB_CRAWLER_URL,
      wishes: 'Nintendo, LEGO, Xiaomi',
      results: null,
      search: null,
      isLoading: false,
      fullPage: true
    };
  },
  created() {
    
  },
  mounted() {
    this.getDefaultResult();
  },
  methods: {
    getDefaultResult() {
      this.isLoading = true;
      const url = this.formatUrl(this.wishes);
      this.axios.get(url).then((res) => {        
        this.isLoading = false;

        if(!res.data) return;
        this.results = this.sortByDate(res.data.items);        
      });
    },    
    searchResult(searchText) {
      this.isLoading = true;  
      
      if(searchText && searchText != '') {        
        const url = this.formatUrl(searchText);
        this.axios.get(url).then((res) => {
          this.isLoading = false;

          if(!res.data) return;
          this.results = this.sortByDate(res.data.items);          
        })
      }
      
      if(searchText == '') {
        this.getDefaultResult();
      }
    },
    formatUrl(searchText) {
      return `${this.resultUrl}&crawl_args={"wishes":"${searchText}"}`
    },
    sortByDate(items) {
      return items.sort((a, b) => Date.parse(b.time) - Date.parse(a.time));
    }
  },
};
</script>


<style lang="">
</style>