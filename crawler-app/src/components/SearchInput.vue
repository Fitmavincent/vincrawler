<template>
  <div class="search-wrapper">
    <i class="pi pi-search search-icon"></i>
    <span class="p-input-icon-right">
      <i v-if="searchValue" class="pi pi-times clear-icon" @click="clearSearch"></i>
      <input-text
        type="text"
        :placeholder="placeholder"
        v-model="searchValue"
        class="search-input"
        :debounce-events="['keyup', 'tab']"
        @input="handleInput"
      />
    </span>
    <slot name="after-input"></slot>
  </div>
</template>

<script>
export default {
  name: 'SearchInput',
  props: {
    placeholder: {
      type: String,
      default: 'Search'
    },
    modelValue: String,
    debounce: {
      type: Number,
      default: 500
    }
  },
  emits: ['update:modelValue', 'search', 'clear'],
  data() {
    return {
      searchValue: this.modelValue
    }
  },
  watch: {
    modelValue(newValue) {
      this.searchValue = newValue;
    }
  },
  methods: {
    handleInput() {
      this.$emit('update:modelValue', this.searchValue);
      this.$emit('search', this.searchValue);
    },
    clearSearch() {
      this.searchValue = '';
      this.$emit('update:modelValue', '');
      this.$emit('clear');
    }
  }
}
</script>

<style scoped>
.search-wrapper {
  display: flex;
  width: 100%;
  align-items: center;
  gap: 1rem;
  border: 1px solid #dbe3ef;
  border-radius: 0.85rem;
  padding: 0.35rem 0.85rem;
  background: #ffffff;
  box-shadow: 0 14px 40px rgba(15, 23, 42, 0.08);
}

.search-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.p-input-icon-right {
  position: relative;
  display: block;
  flex: 1;
}

.search-icon {
  color: #64748b;
  font-size: 1rem;
}

.p-input-icon-right i {
  position: absolute;
  top: 50%;
  right: 0.75rem;
  transform: translateY(-50%);
  z-index: 1;
}

.search-input {
  width: 100%;
  border: 0;
  padding: 0.8rem 2.25rem 0.8rem 0;
  color: #0f172a;
  font-size: 0.98rem;
  box-shadow: none;
}

.search-input:focus {
  box-shadow: none;
}

.clear-icon {
  cursor: pointer;
  color: #64748b;
}

.clear-icon:hover {
  color: #0f172a;
}

@media screen and (max-width: 768px) {
  .search-wrapper {
    flex-direction: column;
    align-items: stretch;
    gap: 0.25rem;
  }

  .search-icon {
    display: none;
  }
}
</style>
