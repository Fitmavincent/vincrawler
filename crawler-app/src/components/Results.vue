<template>
  <section class="results-panel" :class="panelClass">
    <div class="panel-header">
      <div>
        <p class="panel-kicker">Crawler workspace</p>
        <h2>Deal channels</h2>
      </div>
    </div>

    <TabView :activeIndex="activeTab" @tab-change="handleTabChange" class="channel-tabs">
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
  </section>
  <BackToTop />
</template>

<script>
import BackToTop from './BackToTop.vue'

export default {
  components: {
    BackToTop
  },
  data() {
    return {
      activeTab: 0
    }
  },
  computed: {
    panelClass() {
      const channelClasses = ['channel-ozb', 'channel-coles', 'channel-woolies'];
      return channelClasses[this.activeTab] || 'channel-generic';
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
.results-panel {
  --channel-accent: #f59e0b;
  --channel-accent-soft: #fff7ed;
  --channel-accent-border: rgba(245, 158, 11, 0.28);
  overflow: hidden;
  border: 1px solid rgba(148, 163, 184, 0.28);
  border-radius: 1rem;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 24px 80px rgba(15, 23, 42, 0.14);
  backdrop-filter: blur(18px);
}

.results-panel.channel-ozb {
  --channel-accent: #f37021;
  --channel-accent-soft: #fff3e8;
  --channel-accent-border: rgba(243, 112, 33, 0.3);
}

.results-panel.channel-coles {
  --channel-accent: #e01a22;
  --channel-accent-soft: #fff1f2;
  --channel-accent-border: rgba(224, 26, 34, 0.28);
}

.results-panel.channel-woolies {
  --channel-accent: #178841;
  --channel-accent-soft: #ecfdf5;
  --channel-accent-border: rgba(23, 136, 65, 0.28);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.4rem 1.5rem 0.75rem;
}

.panel-kicker {
  color: #b45309;
  font-size: 0.78rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

h2 {
  color: #0f172a;
  font-size: 1.65rem;
  font-weight: 900;
}

:deep(.p-tabview-nav) {
  justify-content: flex-start;
  border: 0;
  gap: 0.5rem;
  padding: 0 1.5rem 0.7rem;
  background: transparent;
}

:deep(.p-tabview-nav-container) {
  overflow-x: auto;
  overflow-y: visible;
  scrollbar-width: none;
}

:deep(.p-tabview-nav-container::-webkit-scrollbar) {
  display: none;
}

:deep(.p-tabview) {
  padding: 0;
}

:deep(.p-tabview-nav li) {
  width: auto;
  margin: 0;
}

:deep(.p-tabview-nav-link) {
  border: 1px solid #dbe3ef !important;
  border-radius: 999px !important;
  padding: 0.72rem 1rem !important;
  color: #49545f !important;
  background: #f8fafc !important;
  font-weight: 800 !important;
}

:deep(.p-tabview-panels) {
  padding: 1rem 1.5rem 1.5rem;
  background: transparent;
}

:deep(li.p-highlight .p-tabview-nav-link) {
  border-color: var(--channel-accent) !important;
  color: #ffffff !important;
  background: var(--channel-accent) !important;
  box-shadow: 0 10px 24px var(--channel-accent-border);
}

@media screen and (max-width: 640px) {
  .panel-header {
    align-items: flex-start;
    flex-direction: column;
    padding: 1rem 1rem 0.65rem;
  }

  :deep(.p-tabview-nav) {
    gap: 0.4rem;
    overflow: visible;
    padding: 0 0.75rem 0.85rem;
  }

  :deep(.p-tabview-nav-container) {
    overflow-x: auto;
    overflow-y: visible;
  }

  :deep(.p-tabview-nav-link) {
    min-width: max-content;
    padding: 0.58rem 0.78rem !important;
    font-size: 0.86rem;
    white-space: nowrap;
  }

  :deep(.p-tabview-panels) {
    padding: 0.6rem 1rem 1rem;
  }

  :deep(li.p-highlight .p-tabview-nav-link) {
    box-shadow: 0 6px 14px var(--channel-accent-border);
  }
}
</style>
