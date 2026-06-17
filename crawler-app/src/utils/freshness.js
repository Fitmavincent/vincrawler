// Weekly-specials freshness, mirroring the lazi API server (api/services/freshness.py).
//
// Australian retail specials reset Wednesday 00:00 Australia/Sydney. Stored data
// is "stale" when it was synced before the most recent Wednesday-midnight reset.
// The server uses this exact boundary to decide whether a GET should trigger a
// background re-crawl; the frontend uses it to decide whether to keep polling
// the data endpoint until the new week's crawl lands.

const SYDNEY_TZ = 'Australia/Sydney';
const SPECIALS_WEEKDAY = 3; // Wednesday (JS getUTCDay: Sun=0 .. Wed=3)

// Minutes that Sydney is ahead of UTC at the given instant (DST-aware, +600 or +660).
function sydneyOffsetMinutes(date) {
  const dtf = new Intl.DateTimeFormat('en-US', {
    timeZone: SYDNEY_TZ,
    hour12: false,
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  });
  const p = Object.fromEntries(dtf.formatToParts(date).map((x) => [x.type, x.value]));
  // '24' can appear for midnight in some engines — normalise to 0.
  const hour = p.hour === '24' ? 0 : Number(p.hour);
  const asUTC = Date.UTC(Number(p.year), Number(p.month) - 1, Number(p.day), hour, Number(p.minute), Number(p.second));
  return Math.round((asUTC - date.getTime()) / 60000);
}

// The instant (UTC Date) of the most recent Wednesday 00:00 Sydney time.
export function lastSpecialsReset(now = new Date()) {
  const offMin = sydneyOffsetMinutes(now);
  // Sydney wall-clock represented as a Date whose UTC fields equal Sydney local fields.
  const sydWall = new Date(now.getTime() + offMin * 60000);
  const daysSinceWed = (sydWall.getUTCDay() - SPECIALS_WEEKDAY + 7) % 7;
  const resetWallUTC = Date.UTC(
    sydWall.getUTCFullYear(),
    sydWall.getUTCMonth(),
    sydWall.getUTCDate() - daysSinceWed,
    0, 0, 0, 0,
  );
  // Convert that Sydney wall instant back to a real UTC instant.
  return new Date(resetWallUTC - offMin * 60000);
}

// True when stored data (its `synced_at` ISO string) predates this week's reset,
// or when there is no/invalid timestamp.
export function isStale(syncedAt, now = new Date()) {
  if (!syncedAt) return true;
  const synced = new Date(syncedAt);
  if (Number.isNaN(synced.getTime())) return true;
  return synced.getTime() < lastSpecialsReset(now).getTime();
}
