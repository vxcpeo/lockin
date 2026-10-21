<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import {
  ArrowDownRight,
  ArrowUpRight,
  ChevronDown,
  KeyRound,
  LockKeyhole,
  Menu,
  X
} from 'lucide-vue-next'
import DocsPage from './Docs.vue'

const DOCS_ROUTE = '#/docs'

// Hash routing keeps the docs reachable on any static host: /#/docs, /#/docs/contracts.
function readRoute() {
  const path = window.location.hash.replace(/^#/, '').replace(/^\/+/, '')
  if (path === 'docs' || path.startsWith('docs/')) {
    return { name: 'docs', section: path.slice(4).replace(/^\/+/, '') }
  }
  return { name: 'home', section: path }
}

// Old /docs links (bookmarks, shared posts) are rewritten to the hash route before the app reads it.
function legacyDocsTarget() {
  const { pathname, hash } = window.location
  if (!/\/docs\/?$/.test(pathname)) return null
  const legacySection = hash.replace(/^#/, '').replace(/^\/+/, '')
  const section = legacySection === 'docs' || legacySection.startsWith('docs/') ? '' : legacySection
  return `${pathname.replace(/docs\/?$/, '')}${DOCS_ROUTE}${section ? `/${section}` : ''}`
}

const legacyTarget = legacyDocsTarget()
if (legacyTarget) window.history.replaceState(null, '', legacyTarget)

const route = ref(readRoute())
const isDocs = computed(() => route.value.name === 'docs')

const menuOpen = ref(false)
const unlocked = ref(false)
const discount = ref(25)
const poolDepth = ref(20)
const bagValue = ref(5)
const lockLength = ref('7d')
let accordionMediaQuery
let accordionCompact = false

const navItems = [
  ['Rail', '#rail'],
  ['Time lock', '#time-lock'],
  ['Combination', '#combination'],
  ['Keys', '#keys'],
  ['Master key', '#master-key']
]

const listings = [
  { coin: 'AAA', discount: 31, lock: '7 days', eth: '0.80' },
  { coin: 'BBB', discount: 12, lock: '24 hours', eth: '0.25' },
  { coin: 'CCC', discount: 44, lock: '30 days', eth: '2.10' },
  { coin: 'DDD', discount: 19, lock: '3 days', eth: '0.42' },
  { coin: 'EEE', discount: 26, lock: '7 days', eth: '1.35' },
  { coin: 'FFF', discount: 8, lock: '24 hours', eth: '0.12' }
]

const flowSteps = [
  ['01', 'Escrow takes the bag', 'A seller lists tokens with a price in ETH and a lock length. The whole amount moves into the market contract the moment the listing is created.'],
  ['02', 'A buyer pays the listed price', 'The ETH reaches the seller in the same transaction. 2% goes to the burner, which buys $LORH and burns it.'],
  ['03', 'Each fill cuts a key', 'The fill creates a position: the right to claim those tokens after the unlock time. It is a transferable token of its own.'],
  ['04', 'That key can change hands', 'A holder who cannot wait sells the position for ETH. The tokens stay where they are; only the right to claim them moves.'],
  ['05', 'On the date, the lock opens', 'Whoever holds the position claims the full amount. Anyone may trigger the release; the tokens can only go to the holder.']
]

const oldLocks = [
  ['You lock tokens you already own and get nothing for it up front', 'The lock is the price of a discount: you pay less on day one'],
  ['Rewards show up only if someone else leaves early', 'The saving is fixed at the fill and depends on no one else leaving'],
  ['A locked position cannot be sold', 'A locked position is yours to sell at any time, at your own price'],
  ['The rest of an early exit reaches the pool', 'Tokens move wallet to wallet, never to the pool'],
  ['Locks of months or years on coins that trend for days', 'Locks of 24 hours to 30 days, sized for how these coins trade'],
  ['Empty until many people lock at the same time', 'One seller with one bag is enough to open a market']
]

const oldLockIssues = [
  ['A bag bigger than its pool', 'Selling a large bag at market takes the slippage and hands every other holder a red candle.'],
  ['Size is hard to buy, too', 'A buyer who wants size meets the same pool from the other side: the price runs before the order is filled.'],
  ['Nothing on day one', 'Lockers ask holders to give up liquidity and offer nothing at the moment of locking.'],
  ['A lock that cannot move', 'Where a locked position cannot change hands, the only way out is a penalty.'],
  ['Deals in direct messages', 'No escrow, no public price, and one side always has to send first.']
]

const pickProof = [
  ['Fill your own listing to look sold out', 'The 2% fee is real ETH, and it is burned'],
  ['Dust fills to collect badges', 'Badges count positions of at least 0.05 ETH'],
  ['Pass a position between two wallets', 'The streak breaks, and every pass pays 1%'],
  ['List above the pool to fake depth', 'Labelled “above market” and left off every discount board'],
  ['Push the pool for a minute to inflate a discount', 'The reference is the 1-hour average, never the last trade'],
  ['Swap the listing price while a buyer signs', 'A fill carries the buyer’s maximum price'],
  ['Fund a wallet to fill your own listing', 'Marked linked on the listing page'],
  ['List a coin that taxes transfers', 'Refused when the deposit cannot deliver the exact amount']
]

const specs = [
  ['Chain', 'Robinhood Chain, EVM, chainId 4663'],
  ['Launchpad', 'Pons curve, then a Uniswap V4 pool'],
  ['Positions', 'ERC-721, one per fill'],
  ['Frontend', 'Vue 3, Vite, viem-ready wallet boundary'],
  ['Read side', 'A lens contract and the chain’s own past blocks'],
  ['Review', 'Source verified on the explorer before the first listing']
]

const workshopPhases = [
  ['Phase 1 · on the bench now', 'A seller can list a bag and a buyer can fill it', ['Market and burner contracts on a fork with live Pons coins', 'Rail, listing page, buy flow, positions and claim', 'Sell flow, resale of positions, coin pages and unlock calendar']],
  ['Phase 2 · launch and growth', '$LORH launches and listing #1 opens the same day', ['External review of the market contract', 'Ten coin teams with bags larger than their pools', 'The wallet record, badges and listing widget']],
  ['Phase 3 · upgrade', 'More ways to price a locked bag', ['Falling-price listings', 'Bids on positions', 'Fee payable in $LORH, 25% cheaper, burned directly']],
  ['Phase 4 · ecosystem', 'Other apps start quoting the discount', ['Hold seasons across two coins', 'Lending against positions through a partner market', 'Positions shown by wallets and terminals']]
]

const specDecisions = [
  ['The lock is sold as a discount', 'A buyer is paid on day one; nothing depends on someone else leaving'],
  ['No early exit; the position is sold instead', 'A penalty sends tokens to the pool; a resale does not'],
  ['Fixed-price listings first', 'No auction logic to review; falling price comes later'],
  ['Fee 2% primary, 1% resale', 'Resale stays cheaper so the position remains liquid'],
  ['No price feed on the chain', 'The contract compares two numbers typed by the two sides'],
  ['Immutable contracts', 'The safeguard is a missing function anyone can verify']
]

const weakPoints = [
  ['A coin can fall further than its discount', 'A discount is fixed at fill time; the token can still fall to zero.'],
  ['A position may have no buyer', 'The only early exit is a resale another wallet chooses to buy.'],
  ['Without sellers there is no market', 'One seller is enough to open the rail, but supply still has to arrive.'],
  ['Smart contracts can contain errors', 'A review reduces that risk; it does not remove it.'],
  ['Unlocks still create liquid supply', 'The calendar shows when tokens move; it cannot stop market risk.']
]

const unlockDate = computed(() => {
  const days = lockLength.value === '24h' ? 1 : lockLength.value === '3d' ? 3 : lockLength.value === '30d' ? 30 : 7
  const date = new Date(Date.now() + days * 86_400_000)
  return new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit', timeZone: 'UTC' }).format(date) + ' UTC'
})

const sellerPool = computed(() => Math.max(0, (Number(bagValue.value) * Number(poolDepth.value) / (Number(poolDepth.value) + Number(bagValue.value || 1))) * 0.99))
const listedValue = computed(() => Math.max(0, Number(bagValue.value) * (1 - Number(discount.value) / 100) * 0.98))
const filledValue = computed(() => Math.max(0, Number(bagValue.value) * (1 - Number(discount.value) / 100)))
const burnValue = computed(() => filledValue.value * 0.02)
const poolDrop = computed(() => Math.max(0, 1 - Math.pow(Number(poolDepth.value) / (Number(poolDepth.value) + Number(bagValue.value || 1)), 2)))
const poolBuy = computed(() => Number(bagValue.value) < Number(poolDepth.value) ? (Number(bagValue.value) * Number(poolDepth.value) / (Number(poolDepth.value) - Number(bagValue.value))) * 1.01 : null)
const breakEven = computed(() => Math.max(0, Math.min(60, (1 - (0.99 * Number(poolDepth.value)) / (Math.max(0.01, Number(poolDepth.value) + Number(bagValue.value || 1)) * 0.98)) * 100)))

function closeMenu() {
  menuOpen.value = false
}

function scrollPageToTop() {
  const root = document.documentElement
  root.style.scrollBehavior = 'auto'
  window.scrollTo(0, 0)
  requestAnimationFrame(() => { root.style.scrollBehavior = '' })
}

function scrollToSection(section, instant = false) {
  const target = document.getElementById(section)
  if (!target) return
  const root = document.documentElement
  if (instant) root.style.scrollBehavior = 'auto'
  target.scrollIntoView({ block: 'start' })
  if (instant) requestAnimationFrame(() => { root.style.scrollBehavior = '' })
}

function applyRoute() {
  const previous = route.value
  const next = readRoute()
  if (previous.name === next.name && previous.section === next.section) return
  route.value = next
  const pageChanged = previous.name !== next.name
  nextTick(() => {
    if (next.name === 'docs') {
      if (next.section) scrollToSection(next.section, pageChanged)
      else if (pageChanged) scrollPageToTop()
      return
    }
    // Home page anchors are handled by the browser; only a page switch loses the target element.
    if (!pageChanged) return
    if (next.section) scrollToSection(next.section, true)
    else scrollPageToTop()
  })
}

function handleMenuKeydown(event) {
  if (event.key === 'Escape') closeMenu()
}

watch(menuOpen, (open) => {
  if (open) {
    document.addEventListener('keydown', handleMenuKeydown)
    document.body.style.overflow = 'hidden'
  } else {
    document.removeEventListener('keydown', handleMenuKeydown)
    document.body.style.overflow = ''
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleMenuKeydown)
  document.body.style.overflow = ''
  window.removeEventListener('hashchange', applyRoute)
  accordionMediaQuery?.removeEventListener?.('change', syncAccordionViewport)
})

function setLock(value) {
  lockLength.value = value
}

function syncAccordionViewport() {
  const compact = accordionMediaQuery?.matches ?? window.matchMedia('(max-width: 767px)').matches
  if (compact === accordionCompact && accordionMediaQuery) return
  accordionCompact = compact
  document.querySelectorAll('.section-accordion').forEach((details) => {
    if (compact) details.removeAttribute('open')
    else details.setAttribute('open', '')
  })
}

onMounted(() => {
  accordionMediaQuery = window.matchMedia('(max-width: 767px)')
  syncAccordionViewport()
  accordionMediaQuery.addEventListener?.('change', syncAccordionViewport)
  window.addEventListener('hashchange', applyRoute)
  if (isDocs.value && route.value.section) nextTick(() => scrollToSection(route.value.section, true))
})
</script>

<template>
  <DocsPage v-if="isDocs" />
  <template v-else>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="#top" aria-label="Latchera home">
        <span class="brand-mark" aria-hidden="true"></span>
        <span class="brand-word">Latchera</span>
      </a>
      <nav class="desktop-nav" aria-label="Sections">
        <a v-for="item in navItems" :key="item[0]" :href="item[1]">{{ item[0] }}</a>
        <a href="#/docs">Docs</a>
      </nav>
      <div class="header-actions">
        <span class="live-pill"><i></i> Market live</span>
        <button class="icon-button menu-button" aria-label="Open the section list" aria-haspopup="dialog" @click="menuOpen = true"><Menu :size="20" /></button>
      </div>
    </div>
  </header>

  <div v-if="menuOpen" class="mobile-menu" role="dialog" aria-modal="true" aria-label="Sections">
    <div class="mobile-menu-top">
      <a class="brand" href="#top" @click="closeMenu"><span class="brand-mark" aria-hidden="true"></span><span class="brand-word">Latchera</span></a>
      <button class="icon-button" aria-label="Close section list" @click="closeMenu"><X :size="21" /></button>
    </div>
    
    <nav>
      <a v-for="(item, index) in navItems" :key="item[0]" :href="item[1]" @click="closeMenu"><span class="menu-label">{{ item[0] }}</span><span class="menu-index"><b>{{ String(index + 1).padStart(2, '0') }}</b><LockKeyhole :size="14" /></span></a>
      <a href="#/docs" @click="closeMenu"><span class="menu-label">Docs</span><span class="menu-index"><b>06</b><LockKeyhole :size="14" /></span></a>
    </nav>
    <p class="mobile-menu-note">$LORH · Robinhood Chain</p>
  </div>

  <main>
    <section id="top" class="hero band-ink">
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <p class="eyebrow accent">$LORH <span>·</span> on Robinhood Chain</p>
          <h1>Lock in a discount.<br /><span>The chart never notices.</span></h1>
          <p class="hero-lede">Buy Robinhood Chain coins below the pool price. The tokens stay locked until a date you can see, and the locked position is yours to sell on.</p>
          <div class="hero-actions">
            <a class="button button-violet" href="#time-lock"><LockKeyhole :size="15" />See a deal lock</a>
            <a class="button button-ghost" href="#/docs">Read the docs</a>
          </div>
        </div>
        <div class="hero-lock-wrap">
          <button type="button" class="hero-lock" :class="{ opened: unlocked }" :aria-pressed="unlocked" :aria-label="unlocked ? 'Close the lock' : 'Open the lock'" @click="unlocked = !unlocked">
            <div class="lock-halo"></div>
            <div class="lock-shackle"><span></span></div>
            <div class="lock-body"><span class="lock-body-dot"></span><span class="lock-body-line"></span></div>
            <div class="lock-ring ring-one"></div><div class="lock-ring ring-two"></div>
          </button>
          <button class="lock-toggle" :aria-pressed="unlocked" @click="unlocked = !unlocked">
            <span>{{ unlocked ? 'Open' : 'Locked in' }}</span><span>· press to {{ unlocked ? 'lock' : 'open' }}</span>
          </button>
        </div>
      </div>
      <div class="wrap stats-row">
        <div><strong>...</strong><span>Listings open</span></div>
        <div><strong>...</strong><span>ETH filled</span></div>
        <div><strong>...</strong><span>$LORH burned</span></div>
        <p>$LORH and the Latchera market are live on Robinhood Chain. List a bag or buy one at latchera.xyz. Community-built. Not affiliated with any brokerage, launchpad or social network.</p>
      </div>
    </section>

    <section id="rail" class="section section-ink">
      <div class="wrap">
        <div class="section-heading split-heading"><div><p class="eyebrow accent">Rail</p><h2>Every bag hangs in public, with its price on the tag.</h2></div><p class="section-intro">Sample rail. These six bags show what a listing makes visible. The live rail opens with the market.</p></div>
        <div class="listing-grid">
          <article v-for="listing in listings" :key="listing.coin" class="listing-card">
            <div class="listing-lock"><span>{{ listing.discount }}%</span><small>UNDER THE POOL</small><div class="lock-glyph"><span></span></div></div>
            <div class="listing-tag"><strong>{{ listing.coin }}</strong><span>locked {{ listing.lock }}</span><span>{{ listing.eth }} ETH left</span></div>
          </article>
        </div>
        <div class="rail-key"><div><strong>On the lock</strong><span>how far under the pool price the bag is listed</span></div><div><strong>On the tag</strong><span>the coin, the lock length, and how much is left to buy</span></div><div><strong>On the rail</strong><span>everything open right now, deepest discount first</span></div></div>
      </div>
    </section>

    <section class="image-band plate-band"><picture><source media="(max-width: 639px)" srcset="/art/fence-sm.webp" /><img src="/art/fence.webp" alt="Padlocks secured to a dark wire fence" /></picture><div class="wrap image-caption"><p>A locked bag is worth less than a liquid one.</p><p>The gap is the market.</p></div></section>

    <section id="time-lock" class="section section-night">
      <div class="wrap">
        <div class="section-heading split-heading"><div><p class="eyebrow accent">Time lock</p><h2>A deal that closes like a vault door: once, and on a clock.</h2></div><figure class="heading-art"><picture><source media="(max-width: 639px)" srcset="/art/timelock-sm.webp" /><img src="/art/timelock.webp" alt="Three dials of a vault time lock" /></picture><figcaption>Set once. Visible until it opens.</figcaption></figure></div>
        <div class="vault-layout"><div class="time-lock-sticky"><div class="vault-art"><div class="vault-dial"><i></i><i></i><i></i></div><div class="vault-handle"></div><div class="vault-label">LOCK<br /><small>ONCE</small></div></div><div class="flow-diagram"><div class="pool-line"><span>POOL PRICE</span><strong>moved 0.0% by this deal</strong></div><div class="flow-actors"><span>SELLER</span><b>ESCROW</b><span>BUYER</span><span>NEXT BUYER</span><span>BURNER</span></div><div class="flow-fees"><em>2%</em><em>1%</em></div><p>Pool price through all five steps: unchanged</p></div></div><div class="flow-content"><div class="flow-rail"><span class="flow-line"></span><article v-for="step in flowSteps" :key="step[0]" class="flow-step"><span class="flow-number">{{ step[0] }}</span><div><h3>{{ step[1] }}</h3><p>{{ step[2] }}</p></div></article></div></div></div>
      </div>
    </section>

    <section id="combination" class="section section-paper">
      <div class="wrap">
        <div class="section-heading split-heading"><div><p class="eyebrow accent-dark">Combination</p><h2>Dial in a discount. See what the pool would have cost.</h2></div><figure class="heading-art paper-art"><picture><source media="(max-width: 639px)" srcset="/art/bag-sm.webp" /><img src="/art/bag.webp" alt="A canvas pouch secured with a padlock" /></picture><figcaption>The bag, before it moves.</figcaption></figure></div>
        <div class="combination-grid">
          <div class="dial-panel">
            <div class="dial-display"><strong>{{ discount }}%</strong><span>UNDER THE POOL</span></div>
            <input v-model.number="discount" class="range" type="range" min="0" max="60" step="1" aria-label="Discount under the pool price" />
            <div class="range-labels"><span>0</span><span>10</span><span>20</span><span>30</span><span>40</span><span>50</span><span>60</span></div>
            <p class="dial-help">A live comparison against the pool price.</p>
            <label class="field"><span>Pool depth, ETH side</span><div><input v-model.number="poolDepth" type="number" min="1" step="1" /><b>ETH</b></div></label>
            <label class="field"><span>Bag value at the pool price</span><div><input v-model.number="bagValue" type="number" min="0.01" step="0.1" /><b>ETH</b></div></label>
            <div class="lock-choice"><span>Lock length</span><div><button v-for="value in ['24h', '3d', '7d', '30d']" :key="value" :class="{ selected: lockLength === value }" @click="setLock(value)">{{ value }}</button></div><small>Filled now, it would unlock {{ unlockDate }}.</small></div>
          </div>
          <div class="calc-output">
            <div class="calc-row"><span>The seller receives</span><div><p><small>Sold into the pool</small><strong>{{ sellerPool.toFixed(3) }} ETH</strong></p><em>pool price falls {{ (poolDrop * 100).toFixed(1) }}%</em><p><small>Listed on Latchera</small><strong>{{ listedValue.toFixed(3) }} ETH</strong></p><em class="good">pool price moves 0.0%</em></div></div>
            <div class="calc-row"><span>The buyer pays for the same tokens</span><div><p><small>Bought from the pool</small><strong>{{ poolBuy === null ? 'Too shallow' : `${poolBuy.toFixed(3)} ETH` }}</strong></p><em>{{ poolBuy === null ? 'bag is larger than pool depth' : 'liquid at once' }}</em><p><small>Filled on Latchera</small><strong>{{ filledValue.toFixed(3) }} ETH</strong></p><em>locked {{ lockLength }}</em></div></div>
            <div class="burn-row"><span>Burned on this fill</span><strong>{{ burnValue.toFixed(4) }} ETH</strong><small>of $LORH, bought and destroyed</small></div>
            <p class="calc-foot">Past {{ breakEven.toFixed(1) }}% the pool would pay this seller more ETH. The listing buys one thing only: a chart that does not move.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="old-locks" class="section section-ink compare-section">
      <div class="wrap">
        <div class="section-heading"><p class="eyebrow accent">Old locks</p><h2>Lockers ask holders to wait for nothing. Pools punish anyone with size.</h2></div>
        <details open class="section-accordion old-locks-accordion">
          <summary><span>Compare the two lock models</span><ChevronDown :size="18" aria-hidden="true" /></summary>
          <div class="section-accordion-panel">
            <div class="old-lock-issues"><article v-for="(issue, index) in oldLockIssues" :key="issue[0]"><span>{{ String(index + 1).padStart(2, '0') }}</span><h3>{{ issue[0] }}</h3><p>{{ issue[1] }}</p></article></div>
            <div class="comparison-table"><div class="comparison-head"><span>Token lockers</span><span>Latchera</span></div><div v-for="row in oldLocks" :key="row[0]" class="comparison-row"><p>{{ row[0] }}</p><p>{{ row[1] }}</p></div></div>
            <p class="closing-line">Time is worth money, and a market can price it. A seller who takes ETH today accepts a lower price. A buyer who can wait pays less.</p>
          </div>
        </details>
      </div>
    </section>

    <section id="keys" class="section section-paper">
      <div class="wrap keys-grid"><div><p class="eyebrow accent-dark">Keys</p><h2>A position is a key with a date stamped into it.</h2><p class="lead-copy">The tokens sit in escrow. The key moves. Whoever holds it when the clock reaches zero can claim the whole bag.</p><figure class="keys-art"><picture><source media="(max-width: 639px)" srcset="/art/keytag-sm.webp" /><img src="/art/keytag.webp" alt="A metal key tag marked with a lock" /></picture><figcaption>POSITION / THE RIGHT TO CLAIM</figcaption></figure><div class="key-card"><div class="key-head"><KeyRound :size="18" /><span>POSITION #0084</span><span class="key-live">TRANSFERABLE</span></div><div class="key-body"><strong>0.42 ETH</strong><span>unlock 18 Oct · 14:08 UTC</span><div class="key-progress"><i></i></div><small>Claimable by the current holder</small></div></div></div><div class="key-list"><div><span>01</span><h3>Visible before you buy</h3><p>Lock length, discount, amount left, seller history and unlock date sit on the listing.</p></div><div><span>02</span><h3>Tradable while locked</h3><p>Sell the position for ETH if the date no longer works for you. Tokens never touch the pool.</p></div><div><span>03</span><h3>Claimable by anyone</h3><p>A keeper can trigger the release on the date. The escrow only sends tokens to the current key holder.</p></div></div></div>
      <div class="position-record"><div><p class="eyebrow accent-dark">What a position records</p><h3>One fill, one key, one date.</h3></div><dl><div><dt>Coin</dt><dd>the exact token held in escrow</dd></div><div><dt>Amount</dt><dd>the amount this holder can claim</dd></div><div><dt>Unlock</dt><dd>fill time plus the chosen lock length</dd></div><div><dt>Moves</dt><dd>holder changes without moving the tokens</dd></div></dl></div>
    </section>

    <section class="image-band open-band"><picture><source media="(max-width: 639px)" srcset="/art/open-sm.webp" /><img src="/art/open.webp" alt="An open padlock with the key turned" /></picture><div class="wrap image-caption"><p>The key turns once.</p><p>Then the bag is open.</p></div></section>

    <section id="master-key" class="section section-ink">
      <div class="wrap">
        <div class="section-heading split-heading"><div><p class="eyebrow accent">Master key</p><h2>$LORH opens the first ten minutes. It never changes a price.</h2></div><p class="section-intro">The token adds optional access and a visible burn story. The market price still comes from each listing.</p></div>
        <div class="master-key-grid"><article><span>01 / BURN</span><h3>Every fill buys and burns</h3><p>2% of a primary fill and 1% of a resale goes to the burner.</p></article><article><span>02 / FIRST WINDOW</span><h3>Latch the opening minutes</h3><p>A future launch window can require a visible $LORH threshold for the first ten minutes.</p></article><article><span>03 / PIN</span><h3>Pin a listing on the rail</h3><p>A burn can move a listing to the top of the public rail for 24 hours.</p></article><article><span>04 / CHEAPER FEE</span><h3>Use the token later</h3><p>Future fee payment in $LORH can be 25% cheaper and burned directly.</p></article></div>
        <div id="legacy-workings" class="architecture"><div class="arch-side"><span>TRANSACTIONS</span><div class="arch-box">Web app<small>wallet stays in the browser</small></div><div class="arch-box">Read API<small>listings, coin pages, cards</small></div><div class="arch-box">Past blocks<small>an hour of pool prices</small></div></div><div class="arch-center"><ArrowUpRight :size="20" /><span>READS</span><div class="lens-box">LockedinLens<small>a whole screen in one call</small></div></div><div class="arch-side money"><span>VALUE</span><div class="arch-box violet-box">LockedinMarket<small>listings, fills, positions, claims</small></div><div class="arch-box violet-box">LockedinBurner<small>buys $LORH, burns it</small></div><div class="arch-box">$LORH pool<small>curve, then Uniswap V4</small></div></div></div>
        <div class="cannot-grid"><div><h3>What the contract cannot do</h3><ul><li>No owner function can move escrowed tokens or a seller’s ETH.</li><li>Claims, cancels and resales cannot be paused.</li><li>No upgrade path. A change means a new deployment.</li><li>No price feed on the chain, so no feed to manipulate.</li></ul></div><dl><div v-for="spec in specs" :key="spec[0]"><dt>{{ spec[0] }}</dt><dd>{{ spec[1] }}</dd></div></dl></div>
      </div>
    </section>

    <section id="strongbox" class="section section-night strongbox-section">
      <div class="wrap">
        <div class="section-heading"><p class="eyebrow accent">Strongbox</p><h2>The market keeps nothing. Its fees leave as burned $LORH.</h2></div>
        <div class="strongbox-streams"><article><p class="eyebrow">A fill</p><div class="strongbox-stream"><span class="stream-main">98%</span><span class="stream-fee">2%</span></div><div class="stream-caption"><span>the seller, in the same transaction</span><span>buys $LORH and burns it</span></div></article><article><p class="eyebrow">A resale</p><div class="strongbox-stream"><span class="stream-main">99%</span><span class="stream-fee">1%</span></div><div class="stream-caption"><span>the holder who sold</span><span>buys $LORH and burns it</span></div></article></div>
        <div class="strongbox-grid"><article><span>PRIMARY FILL</span><strong>98%</strong><p>Seller receives the ETH in the same transaction.</p><div class="strongbox-bar"><i style="width: 98%"></i></div></article><article><span>PRIMARY FILL</span><strong>2%</strong><p>Burner buys and destroys $LORH.</p><div class="strongbox-bar"><i style="width: 16%"></i></div></article><article><span>POSITION RESALE</span><strong>99%</strong><p>Previous holder receives the resale price.</p><div class="strongbox-bar"><i style="width: 99%"></i></div></article><article><span>POSITION RESALE</span><strong>1%</strong><p>Burner fee keeps the key liquid.</p><div class="strongbox-bar"><i style="width: 10%"></i></div></article></div>
        <p class="strongbox-note">No owner function can withdraw escrowed tokens. A keeper may settle the accumulated burner fee through the approved swap path.</p>
      </div>
    </section>

    <section id="workings" class="section section-paper workings-section">
      <div class="wrap">
        <div class="section-heading"><p class="eyebrow accent-dark">Workings</p><h2>Two contracts hold the money. Everything else only reads.</h2></div>
        <div class="architecture"><div class="arch-side"><span>TRANSACTIONS</span><div class="arch-box">Web app<small>wallet stays in the browser</small></div><div class="arch-box">Read API<small>listings, coin pages, cards</small></div><div class="arch-box">Past blocks<small>an hour of pool prices</small></div></div><div class="arch-center"><ArrowUpRight :size="20" /><span>READS</span><div class="lens-box">LockedinLens<small>a whole screen in one call</small></div></div><div class="arch-side money"><span>VALUE</span><div class="arch-box violet-box">LockedinMarket<small>listings, fills, positions, claims</small></div><div class="arch-box violet-box">LockedinBurner<small>buys $LORH, burns it</small></div><div class="arch-box">$LORH pool<small>curve, then Uniswap V4</small></div></div></div>
        <div class="cannot-grid"><div><h3>What the contract cannot do</h3><ul><li>No owner function can move escrowed tokens or a seller's ETH.</li><li>Claims, cancels and resales cannot be paused.</li><li>No upgrade path. A change means a new deployment.</li><li>No price feed on the chain, so no feed to manipulate.</li></ul></div><dl><div v-for="spec in specs" :key="spec[0]"><dt>{{ spec[0] }}</dt><dd>{{ spec[1] }}</dd></div></dl></div>
      </div>
    </section>

    <section id="pick-proof" class="section section-ink">
      <div class="wrap">
        <div class="section-heading"><p class="eyebrow accent-dark">Pick-proof</p><h2>Eight ways to cheat it, and what each one costs.</h2></div>
        <details open class="section-accordion pick-proof-accordion">
          <summary><span>Open all eight checks</span><ChevronDown :size="18" aria-hidden="true" /></summary>
          <div class="section-accordion-panel">
            <div class="pick-grid"><div v-for="(item, index) in pickProof" :key="item[0]" class="pick-item"><span>{{ String(index + 1).padStart(2, '0') }}</span><strong>{{ item[0] }}</strong><em>{{ item[1] }}</em></div></div>
          </div>
        </details>
      </div>
    </section>

    <section id="workshop" class="section section-night workshop-section">
      <div class="wrap">
        <div class="section-heading split-heading"><div><p class="eyebrow accent">Workshop</p><h2>What is on the bench, and what waits its turn.</h2></div><p class="section-intro">The product ships in public phases. Each phase keeps the market legible before adding another way to move a key.</p></div>
        <details open class="section-accordion workshop-accordion">
          <summary><span>View the four phases</span><ChevronDown :size="18" aria-hidden="true" /></summary>
          <div class="section-accordion-panel">
            <div class="workshop-grid"><article v-for="phase in workshopPhases" :key="phase[0]" class="workshop-card"><p class="phase-label">{{ phase[0] }}</p><h3>{{ phase[1] }}</h3><ul><li v-for="item in phase[2]" :key="item">{{ item }}</li></ul><p class="phase-status">Done when <span>someone outside the team completes the flow.</span></p></article></div>
            <div class="workshop-exclusions"><span>Not on the bench, on purpose</span><strong>Rewards paid for locking</strong><strong>A treasury that holds user funds</strong><strong>Governance</strong><strong>A penalty exit</strong></div>
          </div>
        </details>
      </div>
    </section>

    <section id="spec-sheet" class="section section-paper spec-section">
      <div class="wrap">
        <div class="section-heading split-heading"><div><p class="eyebrow accent-dark">Spec sheet</p><h2>Decisions, and why each one was made.</h2></div><p class="section-intro">The market stays small enough to inspect: fixed fees, fixed lock lengths, no upgrade path and no hidden price feed.</p></div>
        <details open class="section-accordion spec-sheet-accordion">
          <summary><span>Open decisions and measures</span><ChevronDown :size="18" aria-hidden="true" /></summary>
          <div class="section-accordion-panel">
            <div class="spec-grid"><article v-for="decision in specDecisions" :key="decision[0]" class="spec-card"><h3>{{ decision[0] }}</h3><p>{{ decision[1] }}</p></article></div>
            <div class="gauge-grid"><div><h3>What gets measured</h3><ul><li>Listings created and first fills</li><li>ETH filled per week</li><li>Resale turnover</li><li>Median discount per lock length</li><li>$LORH burned with ETH spent</li></ul></div><div><h3>Ignored on purpose</h3><ul><li>The token's price</li><li>Follower counts</li><li>Escrow as a headline number</li></ul></div></div>
          </div>
        </details>
      </div>
    </section>

    <section id="weak-points" class="section section-ink weak-section">
      <div class="wrap">
        <div class="section-heading split-heading"><div><p class="eyebrow accent">Weak points</p><h2>Every lock has weak points. These are ours.</h2></div><p class="section-intro">The design makes the trade visible; it cannot remove market risk, smart-contract risk or the need for a buyer.</p></div>
        <details open class="section-accordion weak-points-accordion">
          <summary><span>Read the holds and weak points</span><ChevronDown :size="18" aria-hidden="true" /></summary>
          <div class="section-accordion-panel">
            <div class="weak-layout"><div class="weak-column"><p class="weak-label">Holds</p><ul><li>A buyer's saving is fixed and visible before paying.</li><li>One seller with one bag is enough to open a market.</li><li>No upgrade path, owner over funds or price feed.</li></ul></div><div class="weak-column"><p class="weak-label">Can give way</p><ul><li v-for="point in weakPoints" :key="point[0]"><strong>{{ point[0] }}</strong><span>{{ point[1] }}</span></li></ul></div></div>
            <div class="weak-cards"><article><h3>A launchpad adds it natively</h3><p>If a launchpad offers locked sales at launch, Latchera starts after launch, where large bags still need a market.</p></article><article><h3>Sellers do not come</h3><p>Outreach starts with teams whose bags are larger than their pools and who need a clear exit.</p></article><article><h3>Buyers get hurt</h3><p>Short locks by default, seller history on every listing and a resale market keep the holder informed.</p></article></div>
          </div>
        </details>
      </div>
    </section>

    <section class="closing-image-band"><div class="closing-locks"><LockKeyhole v-for="n in 7" :key="n" :size="30" :style="{ '--n': n }" /></div><div class="wrap closing-image-copy"><p>Time is worth money, and a market can price it.</p><span>$LORH · Robinhood Chain</span></div></section>

    <section id="app" class="cta-band"><div class="wrap cta-inner"><div><p class="eyebrow accent">$LORH · Robinhood Chain</p><h2>Lock in a discount.<br />The chart never notices.</h2><p>List a bag or buy one at the open market. Every number is public, every date is visible.</p></div><div class="cta-actions"><a class="button button-violet" href="#combination">Try the dial <ArrowDownRight :size="17" /></a><a class="button button-ghost" href="#/docs">Read the docs</a></div></div></section>
  </main>

  <footer class="site-footer"><div class="wrap footer-grid"><div><a class="brand" href="#top"><span class="brand-mark" aria-hidden="true"></span><span class="brand-word">Latchera</span></a><p>Discounted bags, locked until the date.</p><p class="footer-chain">$LORH · Robinhood Chain</p></div><div><p class="footer-label">Hardware</p><a v-for="item in navItems" :key="item[0]" :href="item[1]">{{ item[0] }}</a></div><div><p class="footer-label">Paperwork</p><a href="#/docs">Docs</a><a href="#workings">Workings</a><a href="#spec-sheet">Spec sheet</a><a href="#weak-points">Weak points</a></div></div><div class="wrap footer-bottom"><p>Community-built. Not affiliated with any brokerage, launchpad or social network. $LORH is a utility token for the Latchera market, not a share or a claim on revenue. Nothing on this page is financial, legal or tax advice.</p><p>© 2026 Latchera</p></div></footer>
  </template>
</template>
