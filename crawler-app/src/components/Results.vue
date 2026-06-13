<template>
  <section class="results-panel" :class="panelClass">
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

:deep(.p-tabview-nav) {
  justify-content: flex-start;
  border: 0;
  gap: 0.5rem;
  padding: 1rem 1.5rem 0.7rem;
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
  opacity: 1 !important;
  filter: none !important;
}

:deep(.p-tabview-nav-link) {
  border: 1px solid #dbe3ef !important;
  border-radius: 999px !important;
  padding: 0.72rem 1rem !important;
  color: #334155 !important;
  background: #ffffff !important;
  font-weight: 800 !important;
  opacity: 1 !important;
  filter: none !important;
  box-shadow: none;
}

:deep(.p-tabview-nav li:not(.p-highlight) .p-tabview-nav-link) {
  border-color: #d7deea !important;
  color: #334155 !important;
  background: #ffffff !important;
  opacity: 1 !important;
}

:deep(.p-tabview-panels) {
  padding: 1rem 1.5rem 1.5rem;
  background: transparent;
}

:deep(li.p-highlight .p-tabview-nav-link) {
  border-color: var(--channel-accent) !important;
  color: #ffffff !important;
  background: var(--channel-accent) !important;
  opacity: 1 !important;
  filter: none !important;
  box-shadow: 0 10px 22px rgba(15, 23, 42, 0.14);
}

@media screen and (max-width: 640px) {
  :deep(.p-tabview-nav) {
    gap: 0.4rem;
    overflow: visible;
    padding: 0.85rem 0.75rem 0.85rem;
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
    box-shadow: 0 6px 14px rgba(15, 23, 42, 0.12);
  }
}
</style>
