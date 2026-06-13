<template>
  <div>
    <loading
      v-model:active="isLoading"
      :can-cancel="true"
      :is-full-page="fullPage"
      background-color="#f7f8f5"
      :opacity="0.86"
      blur="6px"
    >
      <div class="vc-loading-card" role="status" aria-live="polite">
        <span class="vc-loading-ring" aria-hidden="true"></span>
        <span>Loading deals</span>
      </div>
    </loading>

    <div class="channel-view">
      <div class="channel-heading">
        <div>
          <p>Community deals</p>
          <h1>Ozbargain feed</h1>
        </div>
        <span class="channel-badge">Ozbargain</span>
      </div>

      <SearchInput
        v-model="search"
        placeholder="Search Ozbargain deals"
        @search="searchResult"
        @clear="getDefaultResult"
        v-debounce:500ms
      >
        <template #after-input>
          <div v-if="results" class="result-meta">
            <span>{{ results.length }} deals</span>
          </div>
        </template>
      </SearchInput>

      <data-table :resizableColumns="false" columnResizeMode="expand" :value="results" responsiveLayout="scroll" class="result-container">
        <column field="image" header="Image">
          <template #body="slotProps">
            <a class="deal-image" :href="slotProps.data.link" target="_blank" rel="noreferrer noopener">
              <img :src="slotProps.data.image" :alt="slotProps.data.image">
            </a>
          </template>
        </column>
        <column field="name" header="Name">
          <template #body="slotProps">
            <a class="deal-title" :href="slotProps.data.link" target="_blank" rel="noreferrer noopener">
              <span v-if="slotProps.data.tag" class="deal-tag">{{ slotProps.data.tag }}</span>
              {{ slotProps.data.name }}
            </a>
          </template>
        </column>
        <column field="price" header="Price">
          <template #body="slotProps">
            <a class="deal-price" :href="slotProps.data.node_url" target="_blank" rel="noreferrer noopener">{{slotProps.data.price}}</a>
          </template>
        </column>
        <!-- <column field="link" header="Link">
          <template #body="slotProps">
            <a :href="slotProps.data.link" target="_blank" rel="noreferrer noopener">{{slotProps.data.link}}</a>
          </template>
        </column> -->
        <column field="time" header="Post time">
          <template #body="slotProps">
            <span class="deal-time">{{ slotProps.data.time }}</span>
          </template>
        </column>
      </data-table>

      <div v-if="results && !results.length && !isLoading" class="empty-state">
        <i class="pi pi-search"></i>
        <p>No Ozbargain deals match this search.</p>
      </div>
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
.channel-view {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.channel-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  border-radius: 0.85rem;
  padding: 1.1rem 1.2rem;
  background: linear-gradient(135deg, #ecfdf5, #ffffff 58%);
}

.channel-heading p {
  color: #0f766e;
  font-size: 0.78rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

h1 {
  color: #111827;
  font-size: 1.75rem;
  font-weight: 900;
}

.channel-badge {
  border-radius: 999px;
  padding: 0.55rem 0.85rem;
  color: #ffffff;
  background: #0f766e;
  font-weight: 900;
}

.result-meta {
  color: #0f172a;
  font-size: 0.86rem;
  font-weight: 800;
  white-space: nowrap;
}

.result-container {
  width: 100%;
  overflow-x: auto;
  border: 1px solid #e2e8f0;
  border-radius: 0.85rem;
  background: #ffffff;
  box-shadow: 0 16px 38px rgba(15, 23, 42, 0.08);
}

:deep(.p-datatable) {
  width: 100%;
  min-width: 320px;
}

:deep(.p-datatable-wrapper) {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

:deep(.p-datatable-thead > tr > th) {
  border: 0;
  border-bottom: 1px solid #e2e8f0;
  padding: 0.9rem 1rem;
  color: #475569;
  background: #f8fafc;
  font-size: 0.78rem;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

:deep(.p-datatable-tbody td) {
  min-width: 80px;
  border-color: #edf2f7;
  padding: 0.85rem 1rem;
  color: #334155;
  word-break: break-word;
}

:deep(.p-datatable-tbody td:first-child) {
  min-width: 100px;
  width: 100px;
}

.deal-image {
  display: grid;
  width: 5.5rem;
  height: 5.5rem;
  place-items: center;
  border: 1px solid #e2e8f0;
  border-radius: 0.7rem;
  background: #f8fafc;
}

.deal-image img {
  max-width: 4.75rem;
  max-height: 4.75rem;
  object-fit: contain;
}

.deal-title {
  color: #0f172a;
  font-weight: 850;
  line-height: 1.35;
}

.deal-title:hover {
  color: #0f766e;
}

.deal-tag {
  display: inline-flex;
  margin-right: 0.35rem;
  border-radius: 999px;
  padding: 0.2rem 0.45rem;
  color: #0f766e;
  background: #ccfbf1;
  font-size: 0.74rem;
  font-weight: 900;
}

.deal-price {
  color: #0f766e;
  font-size: 1.02rem;
  font-weight: 950;
}

.deal-time {
  color: #64748b;
  font-size: 0.9rem;
}

.empty-state {
  display: grid;
  min-height: 16rem;
  place-items: center;
  border: 1px dashed #cbd5e1;
  border-radius: 0.85rem;
  color: #64748b;
  background: #f8fafc;
  text-align: center;
}

.empty-state i {
  color: #94a3b8;
  font-size: 1.5rem;
}

@media screen and (max-width: 640px) {
  .channel-heading {
    align-items: flex-start;
    flex-direction: column;
  }

  h1 {
    font-size: 1.55rem;
  }

  :deep(.p-column-title) {
    font-size: 0.9rem;
  }

  :deep(.p-datatable-tbody) {
    font-size: 0.9rem;
  }

  :deep(.p-datatable-tbody td) {
    padding: 0.65rem;
  }
}
</style>
