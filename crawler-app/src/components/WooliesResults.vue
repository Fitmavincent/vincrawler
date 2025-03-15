<template>
  <div>
    <loading v-model:active="isLoading"
      :can-cancel="true"
      :is-full-page="fullPage"/>

    <div class="container mx-auto px-4 md:px-6 lg:px-8">
      <h1 class="text-3xl font-bold mb-4">Woolies Channel</h1>
      <div class="flex items-center justify-center mb-4 gap-4">
        <SearchInput
          v-model="search"
          @search="searchResult"
          @clear="searchResult">
          <template #after-input>
            <div v-if="filteredResults" class="text-gray-600 flex items-center gap-2">
              <span>Found: {{ filteredResults.length }} items</span>
              <span v-if="lastSyncTime" class="text-sm">
                (Last sync: {{ formattedSyncTime }})
              </span>
            </div>
          </template>
        </SearchInput>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <div v-for="product in filteredResults" :key="product.product_link"
          class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow relative"
          :class="{'border-l-4 border-b-4 border-woolies-green': product.retailer === 'Woolworths'}">
          <div class="absolute top-2 right-2 bg-woolies-green text-white px-2 py-1 rounded-full text-xs font-bold">
            {{ product.discount }}
          </div>
          <a :href="product.product_link" target="_blank" rel="noreferrer noopener">
            <img :src="product.image" :alt="product.name" class="w-full h-48 object-contain p-4">
            <div class="p-4">
              <h3 class="text-lg font-semibold">{{ product.name }}</h3>
              <div class="mt-2">
                <p class="text-2xl font-bold text-woolies-green">${{ product.price.toFixed(2) }}</p>
                <p class="text-sm text-gray-500 line-through">Was ${{ product.price_was.toFixed(2) }}</p>
                <p class="text-sm text-gray-600">{{ product.price_per_unit }}</p>
              </div>
            </div>
          </a>
        </div>
      </div>
    </div>
  </div>
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
      wooliesDataUrl: import.meta.env.VITE_WOOLIES_CRAWLER_URL,
      allResults: null,
      results: null,
      search: null,
      isLoading: false,
      fullPage: true,
      syncInProgress: false,
      dataLoaded: false,
      lastSyncTime: null
    };
  },
  computed: {
    filteredResults() {
      if (!this.search || !this.allResults) return this.allResults;

      const searchTerms = this.search.toLowerCase().split(' ').filter(term => term);
      return this.allResults.filter(product => {
        const productName = product.name.toLowerCase();
        return searchTerms.every(term => productName.includes(term));
      });
    },
    formattedSyncTime() {
      if (!this.lastSyncTime) return '';
      const date = new Date(this.lastSyncTime);

      const pad = (num) => String(num).padStart(2, '0');

      const year = date.getFullYear();
      const month = pad(date.getMonth() + 1);
      const day = pad(date.getDate());
      const hours = pad(date.getHours());
      const minutes = pad(date.getMinutes());
      const seconds = pad(date.getSeconds());

      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }
  },
  watch: {
    isActive(newVal) {
      if (newVal && !this.dataLoaded) {
        console.log('Loading Woolies data');
        this.loadData();
      }
    }
  },
  methods: {
    async getDefaultResult() {
      if (this.isLoading || this.syncInProgress) return;

      this.isLoading = true;
      try {
        const res = await this.axios.get(this.wooliesDataUrl);
        if (!res.data?.data || res.data.data.length === 0) {
          await this.forceSyncData();
          // Always fetch data after sync completes
          return this.getDefaultResult();
        }

        this.allResults = res.data.data;
        this.lastSyncTime = res.data.synced_at;
        this.results = this.allResults;
        this.dataLoaded = true;
      } catch (error) {
        if (error.response?.status === 404) {
          await this.forceSyncData();
          // Retry fetching data after 404 and sync
          return this.getDefaultResult();
        } else {
          console.error('Error fetching Woolies data:', error);
        }
      } finally {
        this.isLoading = false;
      }
    },

    async forceSyncData() {
      if (this.syncInProgress) return;

      this.syncInProgress = true;
      try {
        const syncRes = await this.axios.post(`${this.wooliesDataUrl}/sync`);
        if (syncRes.status !== 200) {
          throw new Error('Sync failed');
        }
        // Add a small delay to allow backend sync to complete
        await new Promise(resolve => setTimeout(resolve, 1000));
      } catch (error) {
        console.error('Error syncing Woolies data:', error);
        throw error;
      } finally {
        this.syncInProgress = false;
      }
    },

    searchResult() {
      // Now just triggers the computed property to update
      this.results = this.filteredResults;
    },

    loadData() {
      console.log(`${this.isActive}, ${this.dataLoaded}, ${this.forceRefresh}`);
      if (!this.isActive) return;
      if (this.dataLoaded && !this.forceRefresh) return;
      this.getDefaultResult();
    }
  }
};
</script>

<style scoped>
@media screen and (max-width: 768px) {
  input {
    width: 70%;
  }
}

.container {
  margin-top: 1rem;
}

/* Add Woolies brand color */
:deep(.border-woolies-green) {
  border-color: #178841;
}

:deep(.bg-woolies-green) {
  background-color: #178841;
}

:deep(.text-woolies-green) {
  color: #178841;
}
</style>
