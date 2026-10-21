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
  <div v-else class="lt-app">
    <header class="lt-command">
      <a class="lt-sigil" href="#top" aria-label="Latchera home">
        <span class="lt-sigil-mark" aria-hidden="true"></span>
        <span class="lt-sigil-name">Latchera</span>
      </a>
      <span class="lt-presence"><i></i> Market live</span>
      <div class="lt-command-actions">
        <a class="lt-act lt-act--fill" href="#time-lock"><LockKeyhole :size="15" aria-hidden="true" />See a deal lock</a>
        <a class="lt-act lt-act--line" href="#/docs">Read the docs</a>
        <button class="lt-burger" aria-label="Open the section list" aria-haspopup="dialog" @click="menuOpen = true"><Menu :size="20" aria-hidden="true" /></button>
      </div>
    </header>

    <div v-if="menuOpen" class="lt-sheet" role="dialog" aria-modal="true" aria-label="Sections">
      <div class="lt-sheet-top">
        <a class="lt-sigil" href="#top" @click="closeMenu"><span class="lt-sigil-mark" aria-hidden="true"></span><span class="lt-sigil-name">Latchera</span></a>
        <button class="lt-sheet-close" aria-label="Close section list" @click="closeMenu"><X :size="21" aria-hidden="true" /></button>
      </div>
      <nav class="lt-sheet-nav">
        <a v-for="(item, index) in navItems" :key="item[0]" :href="item[1]" @click="closeMenu"><span class="lt-sheet-label">{{ item[0] }}</span><span class="lt-sheet-index"><b>{{ String(index + 1).padStart(2, '0') }}</b><LockKeyhole :size="14" aria-hidden="true" /></span></a>
        <a href="#/docs" @click="closeMenu"><span class="lt-sheet-label">Docs</span><span class="lt-sheet-index"><b>06</b><LockKeyhole :size="14" aria-hidden="true" /></span></a>
      </nav>
      <p class="lt-sheet-note">$LORH · Robinhood Chain</p>
    </div>

    <div class="lt-spine">
      <nav class="lt-spine-nav" aria-label="Sections">
        <a v-for="(item, index) in navItems" :key="item[0]" class="lt-spine-link" :href="item[1]">
          <span class="lt-spine-glyph" :class="'lt-spine-glyph--' + index" aria-hidden="true"></span>
          <span class="lt-spine-text">{{ item[0] }}</span>
        </a>
      </nav>
      <nav class="lt-spine-nav lt-spine-nav--doc" aria-label="Paperwork">
        <a class="lt-spine-link" href="#/docs">
          <span class="lt-spine-glyph lt-spine-glyph--doc" aria-hidden="true"></span>
          <span class="lt-spine-text">Docs</span>
        </a>
      </nav>
    </div>

    <main class="lt-main">
      <section id="top" class="lt-hero">
        <div class="lt-hero-stage">
          <div class="lt-hero-copy">
            <p class="lt-kicker">$LORH <span>·</span> on Robinhood Chain</p>
            <h1>Lock in a discount.<br /><span>The chart never notices.</span></h1>
            <p class="lt-lede">Buy Robinhood Chain coins below the pool price. The tokens stay locked until a date you can see, and the locked position is yours to sell on.</p>
          </div>
          <div class="lt-vault-wrap">
            <button type="button" class="lt-vault" :class="{ 'is-open': unlocked }" :aria-pressed="unlocked" :aria-label="unlocked ? 'Close the lock' : 'Open the lock'" @click="unlocked = !unlocked">
              <span class="lt-vault-halo" aria-hidden="true"></span>
              <span class="lt-vault-guide" aria-hidden="true"></span>
              <span class="lt-vault-notch lt-vault-notch--a" aria-hidden="true"></span>
              <span class="lt-vault-notch lt-vault-notch--b" aria-hidden="true"></span>
              <span class="lt-vault-notch lt-vault-notch--c" aria-hidden="true"></span>
              <span class="lt-vault-notch lt-vault-notch--d" aria-hidden="true"></span>
              <span class="lt-vault-body" aria-hidden="true">
                <span class="lt-vault-pin"></span>
                <span class="lt-vault-stem"></span>
              </span>
              <span class="lt-vault-legend" aria-hidden="true"></span>
            </button>
            <button class="lt-vault-switch" :aria-pressed="unlocked" @click="unlocked = !unlocked">
              <span>{{ unlocked ? 'Open' : 'Locked in' }}</span><span>· press to {{ unlocked ? 'lock' : 'open' }}</span>
            </button>
          </div>
        </div>
        <div class="lt-telemetry">
          <div><strong>...</strong><span>Listings open</span></div>
          <div><strong>...</strong><span>ETH filled</span></div>
          <div><strong>...</strong><span>$LORH burned</span></div>
          <p>$LORH and the Latchera market are live on Robinhood Chain. List a bag or buy one at latchera.xyz. Community-built. Not affiliated with any brokerage, launchpad or social network.</p>
        </div>
      </section>

      <section id="rail" class="lt-band">
        <p class="lt-marker"><span>Rail</span></p>
        <div class="lt-band-body">
          <div class="lt-head lt-head--split">
            <h2>Every bag hangs in public, with its price on the tag.</h2>
            <p class="lt-head-note">Sample rail. These six bags show what a listing makes visible. The live rail opens with the market.</p>
          </div>
          <ol class="lt-tape" tabindex="0">
            <li v-for="listing in listings" :key="listing.coin" class="lt-tape-row">
              <span class="lt-tape-cut">{{ listing.discount }}%</span>
              <small class="lt-tape-under">UNDER THE POOL</small>
              <div class="lt-tape-tag"><strong>{{ listing.coin }}</strong><span>locked {{ listing.lock }}</span><span>{{ listing.eth }} ETH left</span></div>
            </li>
          </ol>
          <div class="lt-legend">
            <div><strong>On the lock</strong><span>how far under the pool price the bag is listed</span></div>
            <div><strong>On the tag</strong><span>the coin, the lock length, and how much is left to buy</span></div>
            <div><strong>On the rail</strong><span>everything open right now, deepest discount first</span></div>
          </div>
        </div>
      </section>

      <section class="lt-plate">
        <picture><source media="(max-width: 639px)" srcset="/art/fence-sm.webp" /><img src="/art/fence.webp" alt="Padlocks secured to a dark wire fence" /></picture>
        <div class="lt-plate-copy">
          <p>A locked bag is worth less than a liquid one.</p>
          <p>The gap is the market.</p>
        </div>
      </section>

      <section id="time-lock" class="lt-band">
        <p class="lt-marker"><span>Time lock</span></p>
        <div class="lt-band-body">
          <div class="lt-head lt-head--split">
            <h2>A deal that closes like a vault door: once, and on a clock.</h2>
            <figure class="lt-thumb">
              <picture><source media="(max-width: 639px)" srcset="/art/timelock-sm.webp" /><img src="/art/timelock.webp" alt="Three dials of a vault time lock" /></picture>
              <figcaption>Set once. Visible until it opens.</figcaption>
            </figure>
          </div>
          <div class="lt-signal-stage">
            <div class="lt-steps">
              <article v-for="step in flowSteps" :key="step[0]" class="lt-step">
                <span class="lt-step-no">{{ step[0] }}</span>
                <div class="lt-step-body"><h3>{{ step[1] }}</h3><p>{{ step[2] }}</p></div>
              </article>
            </div>
            <div class="lt-signal">
              <div class="lt-signal-dial" aria-hidden="true"><i></i><i></i><i></i><span class="lt-signal-label">LOCK<br /><small>ONCE</small></span></div>
              <div class="lt-signal-pool"><span>POOL PRICE</span><strong>moved 0.0% by this deal</strong></div>
              <div class="lt-signal-actors"><span>SELLER</span><b>ESCROW</b><span>BUYER</span><span>NEXT BUYER</span><span>BURNER</span></div>
              <div class="lt-signal-fees"><em>2%</em><em>1%</em></div>
              <p>Pool price through all five steps: unchanged</p>
            </div>
          </div>
        </div>
      </section>

      <section id="combination" class="lt-band">
        <p class="lt-marker"><span>Combination</span></p>
        <div class="lt-band-body">
          <div class="lt-head lt-head--split">
            <h2>Dial in a discount. See what the pool would have cost.</h2>
            <figure class="lt-thumb">
              <picture><source media="(max-width: 639px)" srcset="/art/bag-sm.webp" /><img src="/art/bag.webp" alt="A canvas pouch secured with a padlock" /></picture>
              <figcaption>The bag, before it moves.</figcaption>
            </figure>
          </div>
          <div class="lt-dial-stage">
            <div class="lt-dial">
              <div class="lt-dial-read"><strong>{{ discount }}%</strong><span>UNDER THE POOL</span></div>
              <input v-model.number="discount" class="lt-slider" type="range" min="0" max="60" step="1" aria-label="Discount under the pool price" />
              <div class="lt-scale"><span>0</span><span>10</span><span>20</span><span>30</span><span>40</span><span>50</span><span>60</span></div>
              <p class="lt-dial-help">A live comparison against the pool price.</p>
              <label class="lt-field"><span>Pool depth, ETH side</span><div><input v-model.number="poolDepth" type="number" min="1" step="1" /><b>ETH</b></div></label>
              <label class="lt-field"><span>Bag value at the pool price</span><div><input v-model.number="bagValue" type="number" min="0.01" step="0.1" /><b>ETH</b></div></label>
              <div class="lt-lockchoice"><span>Lock length</span><div><button v-for="value in ['24h', '3d', '7d', '30d']" :key="value" :class="{ 'is-on': lockLength === value }" @click="setLock(value)">{{ value }}</button></div><small>Filled now, it would unlock {{ unlockDate }}.</small></div>
            </div>
            <div class="lt-calc">
              <div class="lt-calc-row"><span>The seller receives</span><div><p><small>Sold into the pool</small><strong>{{ sellerPool.toFixed(3) }} ETH</strong></p><em>pool price falls {{ (poolDrop * 100).toFixed(1) }}%</em><p><small>Listed on Latchera</small><strong>{{ listedValue.toFixed(3) }} ETH</strong></p><em class="lt-good">pool price moves 0.0%</em></div></div>
              <div class="lt-calc-row"><span>The buyer pays for the same tokens</span><div><p><small>Bought from the pool</small><strong>{{ poolBuy === null ? 'Too shallow' : `${poolBuy.toFixed(3)} ETH` }}</strong></p><em>{{ poolBuy === null ? 'bag is larger than pool depth' : 'liquid at once' }}</em><p><small>Filled on Latchera</small><strong>{{ filledValue.toFixed(3) }} ETH</strong></p><em>locked {{ lockLength }}</em></div></div>
              <div class="lt-burn"><span>Burned on this fill</span><strong>{{ burnValue.toFixed(4) }} ETH</strong><small>of $LORH, bought and destroyed</small></div>
              <p class="lt-calc-foot">Past {{ breakEven.toFixed(1) }}% the pool would pay this seller more ETH. The listing buys one thing only: a chart that does not move.</p>
            </div>
          </div>
        </div>
      </section>

      <section id="old-locks" class="lt-band">
        <p class="lt-marker"><span>Old locks</span></p>
        <div class="lt-band-body">
          <div class="lt-head"><h2>Lockers ask holders to wait for nothing. Pools punish anyone with size.</h2></div>
          <details open class="lt-fold">
            <summary><span>Compare the two lock models</span><ChevronDown :size="18" aria-hidden="true" /></summary>
            <div class="lt-fold-body">
              <ol class="lt-issues">
                <li v-for="(issue, index) in oldLockIssues" :key="issue[0]"><span>{{ String(index + 1).padStart(2, '0') }}</span><h3>{{ issue[0] }}</h3><p>{{ issue[1] }}</p></li>
              </ol>
              <div class="lt-compare">
                <div class="lt-compare-head"><span>Token lockers</span><span>Latchera</span></div>
                <div v-for="row in oldLocks" :key="row[0]" class="lt-compare-row"><p>{{ row[0] }}</p><p>{{ row[1] }}</p></div>
              </div>
              <p class="lt-close-line">Time is worth money, and a market can price it. A seller who takes ETH today accepts a lower price. A buyer who can wait pays less.</p>
            </div>
          </details>
        </div>
      </section>

      <section id="keys" class="lt-band">
        <p class="lt-marker"><span>Keys</span></p>
        <div class="lt-band-body">
          <div class="lt-keys">
            <div class="lt-keys-copy">
              <h2>A position is a key with a date stamped into it.</h2>
              <p class="lt-lead">The tokens sit in escrow. The key moves. Whoever holds it when the clock reaches zero can claim the whole bag.</p>
              <figure class="lt-thumb lt-thumb--tag">
                <picture><source media="(max-width: 639px)" srcset="/art/keytag-sm.webp" /><img src="/art/keytag.webp" alt="A metal key tag marked with a lock" /></picture>
                <figcaption>POSITION / THE RIGHT TO CLAIM</figcaption>
              </figure>
              <div class="lt-ticket">
                <div class="lt-ticket-head"><KeyRound :size="18" aria-hidden="true" /><span>POSITION #0084</span><span class="lt-ticket-live">TRANSFERABLE</span></div>
                <div class="lt-ticket-body"><strong>0.42 ETH</strong><span>unlock 18 Oct · 14:08 UTC</span><div class="lt-ticket-meter"><i></i></div><small>Claimable by the current holder</small></div>
              </div>
            </div>
            <div class="lt-key-list">
              <div><span>01</span><h3>Visible before you buy</h3><p>Lock length, discount, amount left, seller history and unlock date sit on the listing.</p></div>
              <div><span>02</span><h3>Tradable while locked</h3><p>Sell the position for ETH if the date no longer works for you. Tokens never touch the pool.</p></div>
              <div><span>03</span><h3>Claimable by anyone</h3><p>A keeper can trigger the release on the date. The escrow only sends tokens to the current key holder.</p></div>
            </div>
          </div>
          <div class="lt-record">
            <div><p class="lt-submark">What a position records</p><h3>One fill, one key, one date.</h3></div>
            <dl><div><dt>Coin</dt><dd>the exact token held in escrow</dd></div><div><dt>Amount</dt><dd>the amount this holder can claim</dd></div><div><dt>Unlock</dt><dd>fill time plus the chosen lock length</dd></div><div><dt>Moves</dt><dd>holder changes without moving the tokens</dd></div></dl>
          </div>
        </div>
      </section>

      <section class="lt-plate lt-plate--open">
        <picture><source media="(max-width: 639px)" srcset="/art/open-sm.webp" /><img src="/art/open.webp" alt="An open padlock with the key turned" /></picture>
        <div class="lt-plate-copy">
          <p>The key turns once.</p>
          <p>Then the bag is open.</p>
        </div>
      </section>

      <section id="master-key" class="lt-band">
        <p class="lt-marker"><span>Master key</span></p>
        <div class="lt-band-body">
          <div class="lt-head lt-head--split">
            <h2>$LORH opens the first ten minutes. It never changes a price.</h2>
            <p class="lt-head-note">The token adds optional access and a visible burn story. The market price still comes from each listing.</p>
          </div>
          <div class="lt-matrix">
            <article><span>01 / BURN</span><h3>Every fill buys and burns</h3><p>2% of a primary fill and 1% of a resale goes to the burner.</p></article>
            <article><span>02 / FIRST WINDOW</span><h3>Latch the opening minutes</h3><p>A future launch window can require a visible $LORH threshold for the first ten minutes.</p></article>
            <article><span>03 / PIN</span><h3>Pin a listing on the rail</h3><p>A burn can move a listing to the top of the public rail for 24 hours.</p></article>
            <article><span>04 / CHEAPER FEE</span><h3>Use the token later</h3><p>Future fee payment in $LORH can be 25% cheaper and burned directly.</p></article>
          </div>
          <div id="legacy-workings" class="lt-wire">
            <div class="lt-wire-row">
              <span class="lt-wire-label">TRANSACTIONS</span>
              <div class="lt-node">Web app<small>wallet stays in the browser</small></div>
              <div class="lt-node">Read API<small>listings, coin pages, cards</small></div>
              <div class="lt-node">Past blocks<small>an hour of pool prices</small></div>
            </div>
            <div class="lt-wire-link"><ArrowUpRight :size="20" aria-hidden="true" /><span>READS</span><div class="lt-node lt-node--lens">LockedinLens<small>a whole screen in one call</small></div></div>
            <div class="lt-wire-row lt-wire-row--value">
              <span class="lt-wire-label">VALUE</span>
              <div class="lt-node lt-node--hot">LockedinMarket<small>listings, fills, positions, claims</small></div>
              <div class="lt-node lt-node--hot">LockedinBurner<small>buys $LORH, burns it</small></div>
              <div class="lt-node">$LORH pool<small>curve, then Uniswap V4</small></div>
            </div>
          </div>
          <div class="lt-limits">
            <div><h3>What the contract cannot do</h3><ul><li>No owner function can move escrowed tokens or a seller’s ETH.</li><li>Claims, cancels and resales cannot be paused.</li><li>No upgrade path. A change means a new deployment.</li><li>No price feed on the chain, so no feed to manipulate.</li></ul></div>
            <dl><div v-for="spec in specs" :key="spec[0]"><dt>{{ spec[0] }}</dt><dd>{{ spec[1] }}</dd></div></dl>
          </div>
        </div>
      </section>

      <section id="strongbox" class="lt-band">
        <p class="lt-marker"><span>Strongbox</span></p>
        <div class="lt-band-body">
          <div class="lt-head"><h2>The market keeps nothing. Its fees leave as burned $LORH.</h2></div>
          <div class="lt-streams">
            <article><p class="lt-submark">A fill</p><div class="lt-stream-bar"><span class="lt-stream-main">98%</span><span class="lt-stream-fee">2%</span></div><div class="lt-stream-cap"><span>the seller, in the same transaction</span><span>buys $LORH and burns it</span></div></article>
            <article><p class="lt-submark">A resale</p><div class="lt-stream-bar"><span class="lt-stream-main">99%</span><span class="lt-stream-fee">1%</span></div><div class="lt-stream-cap"><span>the holder who sold</span><span>buys $LORH and burns it</span></div></article>
          </div>
          <div class="lt-matrix lt-matrix--bars">
            <article><span>PRIMARY FILL</span><strong>98%</strong><p>Seller receives the ETH in the same transaction.</p><div class="lt-bar"><i style="width: 98%"></i></div></article>
            <article><span>PRIMARY FILL</span><strong>2%</strong><p>Burner buys and destroys $LORH.</p><div class="lt-bar"><i style="width: 16%"></i></div></article>
            <article><span>POSITION RESALE</span><strong>99%</strong><p>Previous holder receives the resale price.</p><div class="lt-bar"><i style="width: 99%"></i></div></article>
            <article><span>POSITION RESALE</span><strong>1%</strong><p>Burner fee keeps the key liquid.</p><div class="lt-bar"><i style="width: 10%"></i></div></article>
          </div>
          <p class="lt-foot-note">No owner function can withdraw escrowed tokens. A keeper may settle the accumulated burner fee through the approved swap path.</p>
        </div>
      </section>

      <section id="workings" class="lt-band">
        <p class="lt-marker"><span>Workings</span></p>
        <div class="lt-band-body">
          <div class="lt-head"><h2>Two contracts hold the money. Everything else only reads.</h2></div>
          <div class="lt-wire">
            <div class="lt-wire-row">
              <span class="lt-wire-label">TRANSACTIONS</span>
              <div class="lt-node">Web app<small>wallet stays in the browser</small></div>
              <div class="lt-node">Read API<small>listings, coin pages, cards</small></div>
              <div class="lt-node">Past blocks<small>an hour of pool prices</small></div>
            </div>
            <div class="lt-wire-link"><ArrowUpRight :size="20" aria-hidden="true" /><span>READS</span><div class="lt-node lt-node--lens">LockedinLens<small>a whole screen in one call</small></div></div>
            <div class="lt-wire-row lt-wire-row--value">
              <span class="lt-wire-label">VALUE</span>
              <div class="lt-node lt-node--hot">LockedinMarket<small>listings, fills, positions, claims</small></div>
              <div class="lt-node lt-node--hot">LockedinBurner<small>buys $LORH, burns it</small></div>
              <div class="lt-node">$LORH pool<small>curve, then Uniswap V4</small></div>
            </div>
          </div>
          <div class="lt-limits">
            <div><h3>What the contract cannot do</h3><ul><li>No owner function can move escrowed tokens or a seller's ETH.</li><li>Claims, cancels and resales cannot be paused.</li><li>No upgrade path. A change means a new deployment.</li><li>No price feed on the chain, so no feed to manipulate.</li></ul></div>
            <dl><div v-for="spec in specs" :key="spec[0]"><dt>{{ spec[0] }}</dt><dd>{{ spec[1] }}</dd></div></dl>
          </div>
        </div>
      </section>

      <section id="pick-proof" class="lt-band">
        <p class="lt-marker"><span>Pick-proof</span></p>
        <div class="lt-band-body">
          <div class="lt-head"><h2>Eight ways to cheat it, and what each one costs.</h2></div>
          <details open class="lt-fold">
            <summary><span>Open all eight checks</span><ChevronDown :size="18" aria-hidden="true" /></summary>
            <div class="lt-fold-body">
              <ol class="lt-checks">
                <li v-for="(item, index) in pickProof" :key="item[0]"><span>{{ String(index + 1).padStart(2, '0') }}</span><strong>{{ item[0] }}</strong><em>{{ item[1] }}</em></li>
              </ol>
            </div>
          </details>
        </div>
      </section>

      <section id="workshop" class="lt-band">
        <p class="lt-marker"><span>Workshop</span></p>
        <div class="lt-band-body">
          <div class="lt-head lt-head--split">
            <h2>What is on the bench, and what waits its turn.</h2>
            <p class="lt-head-note">The product ships in public phases. Each phase keeps the market legible before adding another way to move a key.</p>
          </div>
          <details open class="lt-fold">
            <summary><span>View the four phases</span><ChevronDown :size="18" aria-hidden="true" /></summary>
            <div class="lt-fold-body">
              <ol class="lt-phases">
                <li v-for="phase in workshopPhases" :key="phase[0]">
                  <p class="lt-phase-label">{{ phase[0] }}</p>
                  <h3>{{ phase[1] }}</h3>
                  <ul><li v-for="item in phase[2]" :key="item">{{ item }}</li></ul>
                  <p class="lt-phase-status">Done when <span>someone outside the team completes the flow.</span></p>
                </li>
              </ol>
              <div class="lt-exclusions"><span>Not on the bench, on purpose</span><strong>Rewards paid for locking</strong><strong>A treasury that holds user funds</strong><strong>Governance</strong><strong>A penalty exit</strong></div>
            </div>
          </details>
        </div>
      </section>

      <section id="spec-sheet" class="lt-band">
        <p class="lt-marker"><span>Spec sheet</span></p>
        <div class="lt-band-body">
          <div class="lt-head lt-head--split">
            <h2>Decisions, and why each one was made.</h2>
            <p class="lt-head-note">The market stays small enough to inspect: fixed fees, fixed lock lengths, no upgrade path and no hidden price feed.</p>
          </div>
          <details open class="lt-fold">
            <summary><span>Open decisions and measures</span><ChevronDown :size="18" aria-hidden="true" /></summary>
            <div class="lt-fold-body">
              <div class="lt-decisions">
                <article v-for="decision in specDecisions" :key="decision[0]"><h3>{{ decision[0] }}</h3><p>{{ decision[1] }}</p></article>
              </div>
              <div class="lt-gauges">
                <div><h3>What gets measured</h3><ul><li>Listings created and first fills</li><li>ETH filled per week</li><li>Resale turnover</li><li>Median discount per lock length</li><li>$LORH burned with ETH spent</li></ul></div>
                <div><h3>Ignored on purpose</h3><ul><li>The token's price</li><li>Follower counts</li><li>Escrow as a headline number</li></ul></div>
              </div>
            </div>
          </details>
        </div>
      </section>

      <section id="weak-points" class="lt-band">
        <p class="lt-marker"><span>Weak points</span></p>
        <div class="lt-band-body">
          <div class="lt-head lt-head--split">
            <h2>Every lock has weak points. These are ours.</h2>
            <p class="lt-head-note">The design makes the trade visible; it cannot remove market risk, smart-contract risk or the need for a buyer.</p>
          </div>
          <details open class="lt-fold">
            <summary><span>Read the holds and weak points</span><ChevronDown :size="18" aria-hidden="true" /></summary>
            <div class="lt-fold-body">
              <div class="lt-weak">
                <div class="lt-weak-col"><p class="lt-weak-label">Holds</p><ul><li>A buyer's saving is fixed and visible before paying.</li><li>One seller with one bag is enough to open a market.</li><li>No upgrade path, owner over funds or price feed.</li></ul></div>
                <div class="lt-weak-col"><p class="lt-weak-label">Can give way</p><ul><li v-for="point in weakPoints" :key="point[0]"><strong>{{ point[0] }}</strong><span>{{ point[1] }}</span></li></ul></div>
              </div>
              <div class="lt-risk">
                <article><h3>A launchpad adds it natively</h3><p>If a launchpad offers locked sales at launch, Latchera starts after launch, where large bags still need a market.</p></article>
                <article><h3>Sellers do not come</h3><p>Outreach starts with teams whose bags are larger than their pools and who need a clear exit.</p></article>
                <article><h3>Buyers get hurt</h3><p>Short locks by default, seller history on every listing and a resale market keep the holder informed.</p></article>
              </div>
            </div>
          </details>
        </div>
      </section>

      <section class="lt-finale">
        <div class="lt-finale-locks" aria-hidden="true"><LockKeyhole v-for="n in 7" :key="n" :size="30" :style="{ '--n': n }" /></div>
        <div class="lt-finale-copy"><p>Time is worth money, and a market can price it.</p><span>$LORH · Robinhood Chain</span></div>
      </section>

      <section id="app" class="lt-cta">
        <div class="lt-cta-copy">
          <p class="lt-kicker">$LORH · Robinhood Chain</p>
          <h2>Lock in a discount.<br />The chart never notices.</h2>
          <p>List a bag or buy one at the open market. Every number is public, every date is visible.</p>
        </div>
        <div class="lt-cta-actions">
          <a class="lt-act lt-act--fill" href="#combination">Try the dial <ArrowDownRight :size="17" aria-hidden="true" /></a>
          <a class="lt-act lt-act--line" href="#/docs">Read the docs</a>
        </div>
      </section>
    </main>

    <footer class="lt-foot">
      <div class="lt-foot-grid">
        <div class="lt-foot-brand">
          <a class="lt-sigil" href="#top"><span class="lt-sigil-mark" aria-hidden="true"></span><span class="lt-sigil-name">Latchera</span></a>
          <p>Discounted bags, locked until the date.</p>
          <p class="lt-foot-chain">$LORH · Robinhood Chain</p>
        </div>
        <nav class="lt-foot-nav" aria-label="Hardware">
          <p class="lt-foot-label">Hardware</p>
          <a v-for="item in navItems" :key="item[0]" :href="item[1]">{{ item[0] }}</a>
        </nav>
        <nav class="lt-foot-nav" aria-label="Paperwork">
          <p class="lt-foot-label">Paperwork</p>
          <a href="#/docs">Docs</a><a href="#workings">Workings</a><a href="#spec-sheet">Spec sheet</a><a href="#weak-points">Weak points</a>
        </nav>
      </div>
      <div class="lt-foot-bottom"><p>Community-built. Not affiliated with any brokerage, launchpad or social network. $LORH is a utility token for the Latchera market, not a share or a claim on revenue. Nothing on this page is financial, legal or tax advice.</p><p>© 2026 Latchera</p></div>
    </footer>
  </div>
</template>
