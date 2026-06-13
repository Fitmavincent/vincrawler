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

      <section class="hero-content">
        <div>
          <p class="eyebrow">Ozbargain, Coles, Woolworths</p>
          <h1>Track fresh discounts from every channel.</h1>
          <p class="hero-copy">
            Search across the latest crawled deals with a cleaner workspace built for scanning prices,
            product images, and sync status quickly.
          </p>
        </div>
        <div class="hero-metrics" aria-label="Tracked channels">
          <div>
            <span>3</span>
            <small>channels</small>
          </div>
          <div>
            <span>24/7</span>
            <small>crawler feed</small>
          </div>
          <div>
            <span>AU</span>
            <small>retail focus</small>
          </div>
        </div>
      </section>
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
  padding: 1.25rem clamp(1rem, 4vw, 4rem) 6rem;
}

.topbar,
.hero-content {
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
.status-pill,
.hero-metrics,
.hero-metrics div {
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

.hero-content {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 2rem;
  align-items: end;
  padding-top: 4.5rem;
}

.eyebrow {
  margin-bottom: 0.8rem;
  color: #fbbf24;
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

h1 {
  max-width: 760px;
  font-size: clamp(2.25rem, 6vw, 5.2rem);
  line-height: 0.95;
  font-weight: 900;
}

.hero-copy {
  max-width: 650px;
  margin-top: 1.2rem;
  color: #e8e0d2;
  font-size: 1.05rem;
  line-height: 1.7;
}

.hero-metrics {
  gap: 0.75rem;
}

.hero-metrics div {
  min-width: 6.5rem;
  flex-direction: column;
  align-items: flex-start;
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 0.75rem;
  padding: 0.9rem 1rem;
  background: rgba(20, 20, 22, 0.48);
  backdrop-filter: blur(14px);
}

.hero-metrics span {
  font-size: 1.35rem;
  font-weight: 900;
}

.hero-metrics small {
  color: #e8e0d2;
}

.workspace {
  max-width: 1240px;
  margin: -3.75rem auto 0;
  padding: 0 clamp(0.85rem, 3vw, 2rem) 4rem;
}

@media screen and (max-width: 860px) {
  .hero {
    padding-bottom: 5rem;
  }

  .hero-content {
    grid-template-columns: 1fr;
    padding-top: 3.25rem;
  }

  .hero-metrics {
    flex-wrap: wrap;
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

  .hero-metrics div {
    min-width: 0;
    flex: 1;
  }
}
</style>
