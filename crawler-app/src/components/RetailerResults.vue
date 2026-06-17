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

    <div class="channel-view" :style="themeStyle">
      <div class="channel-heading">
        <div>
          <p>{{ kicker }}</p>
          <h1>{{ title }}</h1>
        </div>
        <span class="channel-badge">{{ badge }}</span>
        <span v-if="brandStrip" class="channel-brand-strip" aria-hidden="true"></span>
      </div>

      <div class="search-row">
        <SearchInput
          v-model="search"
          :placeholder="placeholder"
          @search="searchResult"
          @clear="searchResult">
          <template #after-input>
            <div v-if="filteredResults" class="result-meta">
              <span>{{ filteredResults.length }} items</span>
              <span v-if="lastSyncTime">Synced {{ formattedSyncTime }}</span>
            </div>
          </template>
        </SearchInput>
        <label class="filter-toggle" :class="{ 'filter-toggle--active': halfPriceOnly }">
          <input v-model="halfPriceOnly" type="checkbox">
          <span class="filter-toggle-control" aria-hidden="true"></span>
          <span>Half price only</span>
        </label>
      </div>

      <div v-if="filteredResults && filteredResults.length" class="product-grid">
        <div v-for="product in filteredResults" :key="product.product_link" class="product-card">
          <a :href="product.product_link" target="_blank" rel="noreferrer noopener" class="product-link">
            <div class="product-image-frame">
              <div class="product-badge-row">
                <span v-if="discountTagLabel(product)" class="discount-ribbon" :class="discountTagClass(product)">
                  {{ discountTagLabel(product) }}
                </span>
              </div>
              <img v-if="product.image" :src="product.image" :alt="product.name">
              <div v-else class="product-image-missing">No image</div>
            </div>
            <div class="product-body">
              <h3>{{ product.name }}</h3>
              <div class="price-row">
                <p class="sale-price">${{ formatPrice(product.price) }}</p>
                <p class="was-price">Was ${{ formatPrice(product.price_was) }}</p>
              </div>
              <p v-if="product.price_per_unit" class="unit-price">{{ product.price_per_unit }}</p>
            </div>
          </a>
        </div>
      </div>

      <div v-else-if="!isLoading" class="empty-state">
        <i class="pi pi-search"></i>
        <p>No {{ emptyName }} items match these filters.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { discountTagClass, discountTagLabel, isHalfPriceItem } from '../utils/discountTags';
import { isStale } from '../utils/freshness';

// While the stored data is stale (older than this week's Wed 00:00 AEST
// specials reset), the very first GET has already asked the server to re-crawl
// in the background. We poll the same data endpoint until the new week's data
// lands, then stop. No /sync calls — the GET endpoint is the trigger.
const REFRESH_POLL_MS = 90000;       // 90s between polls
const MAX_REFRESH_POLLS = 12;        // ~18 min ceiling (server crawl ~10 min)
const FETCH_TIMEOUT_MS = 45000;      // generous for Fly cold-start

export default {
  props: {
    isActive: {
      type: Boolean,
      default: false
    },
    dataUrl: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    badge: {
      type: String,
      required: true
    },
    emptyName: {
      type: String,
      required: true
    },
    placeholder: {
      type: String,
      required: true
    },
    kicker: {
      type: String,
      default: 'Retail specials'
    },
    accent: {
      type: String,
      required: true
    },
    accentSoft: {
      type: String,
      required: true
    },
    accentInk: {
      type: String,
      required: true
    },
    accentBorder: {
      type: String,
      required: true
    },
    secondaryAccent: {
      type: String,
      default: ''
    },
    tertiaryAccent: {
      type: String,
      default: ''
    },
    brandStrip: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      allResults: null,
      results: null,
      search: null,
      halfPriceOnly: false,
      isLoading: false,
      fullPage: true,
      dataLoaded: false,
      lastSyncTime: null,
      refreshTimer: null,
      refreshPolls: 0
    };
  },
  computed: {
    themeStyle() {
      return {
        '--retailer-accent': this.accent,
        '--retailer-accent-soft': this.accentSoft,
        '--retailer-accent-ink': this.accentInk,
        '--retailer-accent-border': this.accentBorder,
        '--retailer-secondary-accent': this.secondaryAccent || this.accent,
        '--retailer-tertiary-accent': this.tertiaryAccent || this.accent
      };
    },
    filteredResults() {
      if (!this.allResults) return this.allResults;

      const searchTerms = this.search ? this.search.toLowerCase().split(' ').filter(term => term) : [];
      return this.allResults.filter(product => {
        const productName = String(product.name || '').toLowerCase();
        const matchesSearch = searchTerms.every(term => productName.includes(term));
        const matchesHalfPrice = !this.halfPriceOnly || isHalfPriceItem(product);
        return matchesSearch && matchesHalfPrice;
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
        this.loadData();
      }
    }
  },
  mounted() {
    if (this.isActive) {
      this.loadData();
    }
  },
  methods: {
    discountTagClass,
    discountTagLabel,
    formatPrice(value) {
      const numericValue = Number(value);
      return Number.isFinite(numericValue) ? numericValue.toFixed(2) : '0.00';
    },
    async getDefaultResult({ silent = false } = {}) {
      if (this.isLoading) return;

      if (!silent) this.isLoading = true;
      try {
        const res = await this.axios.get(this.dataUrl, { timeout: FETCH_TIMEOUT_MS });
        const data = Array.isArray(res.data?.data) ? res.data.data : [];

        this.allResults = data;
        this.results = data;
        this.lastSyncTime = res.data?.synced_at || null;
        this.dataLoaded = true;
      } catch (error) {
        console.error(`Error fetching ${this.badge} data:`, error);
        // On the very first (non-silent) load only — keep whatever we had on a
        // failed silent poll so the grid doesn't flash empty between cycles.
        if (!silent && !this.dataLoaded) {
          this.allResults = [];
          this.results = [];
        }
      } finally {
        if (!silent) this.isLoading = false;
        this.scheduleStaleRefresh();
      }
    },
    // If the data we just loaded is stale (before this week's Wed reset), keep
    // re-fetching in the background until the new week's crawl lands.
    scheduleStaleRefresh() {
      this.clearRefreshTimer();
      if (!isStale(this.lastSyncTime)) {
        this.refreshPolls = 0;
        return;
      }
      if (this.refreshPolls >= MAX_REFRESH_POLLS) return;
      this.refreshTimer = setTimeout(() => {
        this.refreshPolls += 1;
        this.getDefaultResult({ silent: true });
      }, REFRESH_POLL_MS);
    },
    clearRefreshTimer() {
      if (this.refreshTimer) {
        clearTimeout(this.refreshTimer);
        this.refreshTimer = null;
      }
    },
    searchResult() {
      this.results = this.filteredResults;
    },
    loadData() {
      if (!this.isActive) return;
      if (this.dataLoaded) return;
      this.getDefaultResult();
    }
  },
  unmounted() {
    this.clearRefreshTimer();
  }
};
</script>

<style scoped>
.channel-view {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.channel-heading {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  overflow: hidden;
  border: 1px solid var(--retailer-accent-border);
  border-left: 0.35rem solid var(--retailer-accent);
  border-radius: 0.85rem;
  padding: 1.1rem 1.2rem;
  background: #ffffff;
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
}

.channel-heading p {
  color: var(--retailer-accent-ink);
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
  background: var(--retailer-accent);
  font-weight: 900;
  white-space: nowrap;
}

.channel-brand-strip {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  height: 0.28rem;
  background: linear-gradient(
    90deg,
    var(--retailer-accent) 0 34%,
    var(--retailer-secondary-accent) 34% 67%,
    var(--retailer-tertiary-accent) 67% 100%
  );
}

.search-row {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
}

.filter-toggle {
  display: inline-flex;
  width: fit-content;
  max-width: 100%;
  align-items: center;
  gap: 0.55rem;
  border: 1px solid #d7deea;
  border-radius: 999px;
  padding: 0.48rem 0.7rem 0.48rem 0.55rem;
  color: #334155;
  background: #ffffff;
  font-size: 0.88rem;
  font-weight: 850;
  line-height: 1;
  cursor: pointer;
  user-select: none;
}

.filter-toggle input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.filter-toggle-control {
  position: relative;
  width: 2rem;
  height: 1.1rem;
  flex: 0 0 auto;
  border-radius: 999px;
  background: #cbd5e1;
  transition: background-color 160ms ease;
}

.filter-toggle-control::after {
  position: absolute;
  top: 0.17rem;
  left: 0.18rem;
  width: 0.76rem;
  height: 0.76rem;
  border-radius: 999px;
  background: #ffffff;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.22);
  content: '';
  transition: transform 160ms ease;
}

.filter-toggle--active {
  border-color: var(--retailer-accent-border);
  color: var(--retailer-accent-ink);
  background: var(--retailer-accent-soft);
}

.filter-toggle--active .filter-toggle-control {
  background: var(--retailer-accent);
}

.filter-toggle--active .filter-toggle-control::after {
  transform: translateX(0.88rem);
}

.filter-toggle:focus-within {
  outline: 3px solid var(--retailer-accent-border);
  outline-offset: 2px;
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
  border-color: var(--retailer-accent-border);
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
  background: var(--retailer-accent);
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

.product-image-missing {
  display: grid;
  width: 100%;
  height: 100%;
  place-items: center;
  border: 1px dashed #cbd5e1;
  border-radius: 0.75rem;
  color: #64748b;
  font-size: 0.82rem;
  font-weight: 800;
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
  color: var(--retailer-accent);
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
