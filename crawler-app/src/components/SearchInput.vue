<template>
  <div class="search-wrapper">
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
input {
  padding: 10px;
  margin: 10px 0;
  width: 20%;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.p-input-icon-right {
  position: relative;
  display: inline-block;
}

.p-input-icon-right i {
  position: absolute;
  top: 50%;
  right: 0.75rem;
  transform: translateY(-50%);
  z-index: 1;
}

.search-input {
  width: 300px;
}

.clear-icon {
  cursor: pointer;
  color: #666;
}

.clear-icon:hover {
  color: #333;
}

@media screen and (max-width: 768px) {
  .search-input {
    width: 100%;
  }
}
</style>
