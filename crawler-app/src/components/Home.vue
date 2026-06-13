<template>
  <div class="app-shell">
    <header class="hero">
      <nav class="topbar" aria-label="Application navigation">
        <div class="brand-lockup">
          <span class="brand-mark">V</span>
          <span class="brand-name">VinCrawler</span>
        </div>
        <div class="status-pill">
          <i class="pi pi-bolt"></i>
          Live deal scanner
        </div>
      </nav>

    </header>

    <main class="workspace">
      <results />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(245, 158, 11, 0.18), transparent 30rem),
    linear-gradient(180deg, #faf8f3 0%, #f3efe6 42%, #fbfaf7 100%);
}

.hero {
  color: #f8fafc;
  background:
    linear-gradient(135deg, rgba(18, 18, 20, 0.95), rgba(57, 44, 27, 0.9)),
    url("https://images.unsplash.com/photo-1557821552-17105176677c?auto=format&fit=crop&w=1800&q=80");
  background-size: cover;
  background-position: center;
  padding: 1rem clamp(1rem, 4vw, 4rem) 2.5rem;
}

.topbar {
  max-width: 1200px;
  margin: 0 auto;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.brand-lockup,
.status-pill {
  display: flex;
  align-items: center;
}

.brand-lockup {
  gap: 0.75rem;
  font-weight: 800;
}

.brand-mark {
  display: grid;
  width: 2.5rem;
  height: 2.5rem;
  place-items: center;
  border-radius: 0.75rem;
  background: #f8fafc;
  color: #141416;
}

.brand-name {
  font-size: 1.1rem;
}

.status-pill {
  gap: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 999px;
  padding: 0.55rem 0.85rem;
  color: #fde68a;
  background: rgba(20, 20, 22, 0.42);
  backdrop-filter: blur(14px);
  font-size: 0.875rem;
}

.workspace {
  max-width: 1240px;
  margin: -1.6rem auto 0;
  padding: 0 clamp(0.85rem, 3vw, 2rem) 3rem;
}

@media screen and (max-width: 860px) {
  .hero {
    padding-bottom: 2.45rem;
  }
}

@media screen and (max-width: 560px) {
  .status-pill {
    display: none;
  }

  .hero {
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .workspace {
    margin-top: -1.5rem;
  }
}
</style>
