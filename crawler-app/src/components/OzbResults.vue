<template>
  <div>
    <loading v-model:active="isLoading"
      :can-cancel="true"
      :is-full-page="fullPage"
    />

    <div>
      <h1 class="text-3xl font-bold">Ozb Channel</h1>
      <data-table :resizableColumns="false" columnResizeMode="expand" :value="results" responsiveLayout="scroll" class="result-container">
        <SearchInput
          v-model="search"
          @search="searchResult"
          @clear="getDefaultResult"
          v-debounce:500ms
        />
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
import qs from 'qs';

export default {
  data() {
    return {
      ozdataUrl: import.meta.env.VITE_OZB_CRAWLER_URL,
      wishes: '',
      results: null,
      search: null,
      isLoading: false,
      fullPage: true
    };
  },
  created() {

  },
  mounted() {
    this.loadData();
  },
  methods: {
    getDefaultResult() {
      this.isLoading = true;

      this.axios.get(this.ozdataUrl).then((res) => {
        this.isLoading = false;

        if(!res.data) return;
        this.results = this.sortByDate(res.data);
      });
    },
    searchResult(searchText) {
      this.isLoading = true;

      if(searchText && searchText != '') {
        this.axios.get(this.ozdataUrl, {
          params: {
            wish: searchText.split(' ')
          },
          paramsSerializer: params => qs.stringify(params, {arrayFormat: 'repeat'})
        }).then((res) => {
          this.isLoading = false;

          if(!res.data) return;
          this.results = this.sortByDate(res.data);
        })
      }

      if(searchText == '') {
        this.getDefaultResult();
      }
    },
    sortByDate(items) {
      return items.sort((a, b) => Date.parse(b.time) - Date.parse(a.time));
    },
    loadData() {
      if (this.results && !this.forceRefresh) return;
      this.getDefaultResult();
    }
  },
};
</script>


<style scoped>
.result-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  overflow-x: auto;
}

:deep(.p-datatable) {
  width: 100%;
  min-width: 320px; /* Ensure minimum width for mobile */
}

:deep(.p-datatable-wrapper) {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
}

:deep(.p-datatable-tbody td) {
  word-break: break-word; /* Prevent text from overflowing */
  min-width: 80px; /* Minimum column width */
}

:deep(.p-datatable-tbody td:first-child) {
  min-width: 100px; /* Minimum width for image column */
  width: 100px; /* Fixed width for image column */
}

/* Adjust image size for mobile */
:deep(.p-datatable-tbody td:first-child img) {
  max-width: 100%;
  object-fit: contain;
}

@media screen and (max-width: 640px) {
  h1 {
    font-size: 1.5rem;
    text-align: center;
  }

  :deep(.p-column-title) {
    font-size: 0.9rem;
  }

  :deep(.p-datatable-tbody) {
    font-size: 0.9rem;
  }

  :deep(.p-datatable-tbody td) {
    padding: 0.5rem; /* Reduce padding on mobile */
  }
}
</style>