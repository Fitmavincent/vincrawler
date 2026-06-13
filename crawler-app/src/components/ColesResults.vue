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
      <div class="channel-heading coles-heading">
        <div>
          <p>Supermarket crawler</p>
          <h1>Coles deals</h1>
        </div>
        <span class="channel-badge">Coles</span>
      </div>

      <div class="search-row">
        <SearchInput
          v-model="search"
          placeholder="Search Coles specials"
          @search="searchResult"
          @clear="searchResult">
          <template #after-input>
            <div v-if="filteredResults" class="result-meta">
              <span>{{ filteredResults.length }} items</span>
              <span v-if="lastSyncTime">Synced {{ formattedSyncTime }}</span>
            </div>
          </template>
        </SearchInput>
      </div>

      <div v-if="filteredResults && filteredResults.length" class="product-grid">
        <div v-for="product in filteredResults" :key="product.product_link"
          class="product-card coles-card">
          <a :href="product.product_link" target="_blank" rel="noreferrer noopener" class="product-link">
            <div class="product-image-frame">
              <div class="product-badge-row">
                <span v-if="discountTagLabel(product)" class="discount-ribbon" :class="discountTagClass(product)">
                  {{ discountTagLabel(product) }}
                </span>
              </div>
              <img :src="product.image" :alt="product.name">
            </div>
            <div class="product-body">
              <h3>{{ product.name }}</h3>
              <div class="price-row">
                <p class="sale-price">${{ product.price.toFixed(2) }}</p>
                <p class="was-price">Was ${{ product.price_was.toFixed(2) }}</p>
              </div>
              <p class="unit-price">{{ product.price_per_unit }}</p>
            </div>
          </a>
        </div>
      </div>

      <div v-else-if="!isLoading" class="empty-state">
        <i class="pi pi-search"></i>
        <p>No Coles items match this search.</p>
      </div>
    </div>
  </div>
</template>

<script>
import qs from 'qs';
import { discountTagClass, discountTagLabel } from '../utils/discountTags';

export default {
  props: {
    isActive: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      colesDataUrl: import.meta.env.VITE_COLES_CRAWLER_URL,
      allResults: null,
      results: null,
      search: null,
      isLoading: false,
      fullPage: true,
      syncInProgress: false,
      dataLoaded: false,  // Replace initialLoadDone with more descriptive name
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
        console.log('Loading Coles data');
        this.loadData();
      }
    }
  },
  mounted() {
    // Remove the automatic data loading
  },
  methods: {
    discountTagClass,
    discountTagLabel,
    async getDefaultResult() {
      if (this.isLoading || this.syncInProgress) return;

      this.isLoading = true;
      try {
        const res = await this.axios.get(this.colesDataUrl);
        if (!res.data?.data || res.data.data.length === 0) {
          await this.forceSyncData();
          // Always fetch data after sync completes
          return this.getDefaultResult();
        }

        this.allResults = res.data.data;
        this.lastSyncTime = res.data.synced_at; // Store the sync time
        this.results = this.allResults;
        this.dataLoaded = true;
      } catch (error) {
        if (error.response?.status === 404) {
          await this.forceSyncData();
          // Retry fetching data after 404 and sync
          return this.getDefaultResult();
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
        // Add a small delay to allow backend sync to complete
        await new Promise(resolve => setTimeout(resolve, 1000));
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
      console.log(`${this.isActive}, ${this.dataLoaded}, ${this.forceRefresh}`);
      if (!this.isActive) return;
      if (this.dataLoaded && !this.forceRefresh) return;
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
  border: 1px solid rgba(224, 26, 34, 0.16);
  border-left: 0.35rem solid #e01a22;
  border-radius: 0.85rem;
  padding: 1.1rem 1.2rem;
  background: #ffffff;
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
}

.channel-heading p {
  color: #9f1239;
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
  background: #e01a22;
  font-weight: 900;
}

.search-row {
  width: 100%;
}

.result-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  color: #64748b;
  font-size: 0.86rem;
  white-space: nowrap;
}

.result-meta span:first-child {
  color: #0f172a;
  font-weight: 800;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 230px), 1fr));
  gap: 1rem;
}

.product-card {
  position: relative;
  min-width: 0;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  border-radius: 0.85rem;
  background: #ffffff;
  box-shadow: 0 16px 38px rgba(15, 23, 42, 0.08);
  transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
}

.product-card:hover {
  border-color: rgba(224, 26, 34, 0.45);
  transform: translateY(-3px);
  box-shadow: 0 24px 48px rgba(15, 23, 42, 0.14);
}

.product-link {
  display: flex;
  min-width: 0;
  height: 100%;
  flex-direction: column;
}

.discount-ribbon {
  display: inline-flex;
  max-width: 100%;
  min-height: 1.6rem;
  align-items: center;
  border-radius: 999px;
  padding: 0.4rem 0.65rem;
  color: #ffffff;
  background: #e01a22;
  font-size: 0.76rem;
  font-weight: 900;
  line-height: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.discount-ribbon--half {
  color: #111827;
  background: #fbbf24;
  box-shadow: 0 10px 24px rgba(251, 191, 36, 0.28);
}

.discount-ribbon--higher {
  background: #7c2d12;
  box-shadow: 0 10px 24px rgba(124, 45, 18, 0.24);
}

.product-image-frame {
  position: relative;
  box-sizing: border-box;
  display: grid;
  height: 13rem;
  overflow: hidden;
  place-items: center;
  padding: 3.1rem 1.25rem 1.25rem;
  background: #f8fafc;
}

.product-badge-row {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  left: 0.75rem;
  z-index: 1;
  display: flex;
  justify-content: flex-end;
  pointer-events: none;
}

.product-image-frame img {
  display: block;
  max-width: 100%;
  max-height: calc(13rem - 4.35rem);
  object-fit: contain;
}

.product-body {
  display: flex;
  min-width: 0;
  flex: 1;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
}

h3 {
  color: #0f172a;
  font-size: 0.98rem;
  font-weight: 850;
  line-height: 1.35;
  overflow-wrap: anywhere;
}

.price-row {
  margin-top: auto;
}

.sale-price {
  color: #e01a22;
  font-size: 1.85rem;
  font-weight: 950;
  line-height: 1;
}

.was-price {
  margin-top: 0.25rem;
  color: #94a3b8;
  font-size: 0.9rem;
  text-decoration: line-through;
}

.unit-price {
  color: #64748b;
  font-size: 0.88rem;
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

@media screen and (max-width: 768px) {
  .channel-heading {
    align-items: flex-start;
    flex-direction: column;
  }

  .result-meta {
    white-space: normal;
  }
}
</style>
