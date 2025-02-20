<template>
  <div>
    <loading v-model:active="isLoading"
      :can-cancel="true"
      :on-cancel="onCancel"
      :is-full-page="fullPage"/>

    <div class="container mx-auto px-4 md:px-6 lg:px-8">
      <h1 class="text-3xl font-bold mb-4">Coles Channel</h1>
      <div class="flex items-center justify-center mb-4 gap-4">
        <input-text type="text"
          placeholder="Search"
          v-model="search"
          @input="searchResult"
          :debounce-events="['keyup', 'tab']"/>
        <span v-if="filteredResults" class="text-gray-600">
          Found: {{ filteredResults.length }} items
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <div v-for="product in filteredResults" :key="product.product_link"
          class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow relative"
          :class="{'border-l-4 border-b-4 border-red-500': product.retailer === 'Coles'}">
          <div class="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded-full text-xs font-bold">
            {{ product.discount }}
          </div>
          <a :href="product.product_link" target="_blank" rel="noreferrer noopener">
            <img :src="product.image" :alt="product.name" class="w-full h-48 object-contain p-4">
            <div class="p-4">
              <h3 class="text-lg font-semibold">{{ product.name }}</h3>
              <div class="mt-2">
                <p class="text-2xl font-bold text-red-600">${{ product.price.toFixed(2) }}</p>
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
import qs from 'qs';

export default {
  data() {
    return {
      colesDataUrl: import.meta.env.VITE_COLES_CRAWLER_URL,
      allResults: null,
      results: null,
      search: null,
      isLoading: false,
      fullPage: true,
      syncInProgress: false,
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
    }
  },
  mounted() {
    // Remove the automatic data loading\
    this.loadData();
  },
  methods: {
    async getDefaultResult() {
      this.isLoading = true;
      try {
        const res = await this.axios.get(this.colesDataUrl);
        if (!res.data?.data || res.data.data.length === 0) {
          // If no data, attempt force sync
          await this.forceSyncData();
          // Retry getting data after sync
          const newRes = await this.axios.get(this.colesDataUrl);
          this.allResults = newRes.data?.data || [];
        } else {
          this.allResults = res.data.data;
        }
        this.results = this.allResults;
      } catch (error) {
        if (error.response?.status === 404) {
          await this.forceSyncData();
          if (!this.syncInProgress) {
            await this.getDefaultResult();
          }
        } else {
          console.error('Error fetching Coles data:', error);
        }
      } finally {
        this.isLoading = false;
      }
    },

    async forceSyncData() {
      if (this.syncInProgress) return;

      this.syncInProgress = true;
      try {
        const syncRes = await this.axios.post(`${this.colesDataUrl}/sync`);
        if (syncRes.status !== 200) {
          throw new Error('Sync failed');
        }
      } catch (error) {
        console.error('Error syncing Coles data:', error);
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
      if (this.allResults && !this.forceRefresh) return;
      this.getDefaultResult();
    }
  },
};
</script>

<style scoped>
input {
  padding: 10px;
  margin: 10px 0;
  width: 20%;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

@media screen and (max-width: 768px) {
  input {
    width: 70%;
  }
}

.container {
  margin-top: 1rem;
}
</style>