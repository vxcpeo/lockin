<template>
  <DocsPage v-if="isDocs" />
  <div v-else class="gx-page">
    <button class="gx-index-btn" aria-label="Open the section list" aria-haspopup="dialog" @click="menuOpen = true"><Menu :size="20" aria-hidden="true" /></button>

    <div v-if="menuOpen" class="gx-sheet" role="dialog" aria-modal="true" aria-label="Sections">
      <div class="gx-sheet-top">
        <a class="gx-brand" href="#top" @click="closeMenu"><span class="gx-brand-mark" aria-hidden="true"></span><span class="gx-brand-word">Holdavia</span></a>
        <button class="gx-sheet-close" aria-label="Close section list" @click="closeMenu"><X :size="22" aria-hidden="true" /></button>
      </div>
      <nav class="gx-sheet-nav" aria-label="Sections">
        <a v-for="(item, index) in navItems" :key="item[0]" class="gx-sheet-link" :href="item[1]" @click="closeMenu"><span class="gx-sheet-label">{{ item[0] }}</span><span class="gx-sheet-index"><b>{{ String(index + 1).padStart(2, '0') }}</b><LockKeyhole :size="14" aria-hidden="true" /></span></a>
        <a class="gx-sheet-link" href="#/docs" @click="closeMenu"><span class="gx-sheet-label">Docs</span><span class="gx-sheet-index"><b>06</b><LockKeyhole :size="14" aria-hidden="true" /></span></a>
      </nav>
      <p class="gx-sheet-note">$LORH · Robinhood Chain</p>
    </div>

    <main class="gx-main">
      <section id="top" class="gx-scene gx-scene--open">
        <div class="gx-open-copy">
          <a class="gx-brand" href="#top" aria-label="Holdavia home">
            <span class="gx-brand-mark" aria-hidden="true"></span>
            <span class="gx-brand-word">Holdavia</span>
          </a>
          <p class="gx-kicker">$LORH <span>·</span> on Robinhood Chain</p>
          <h1 class="gx-display">Lock in a discount.<br /><span>The chart never notices.</span></h1>
          <p class="gx-lede">Buy Robinhood Chain coins below the pool price. The tokens stay locked until a date you can see, and the locked position is yours to sell on.</p>
          <div class="gx-open-actions">
            <a class="gx-btn gx-btn--solid" href="#time-lock"><LockKeyhole :size="15" aria-hidden="true" />See a deal lock</a>
            <a class="gx-btn" href="#/docs">Read the docs</a>
          </div>
          <p class="gx-presence"><i aria-hidden="true"></i> Market live</p>
        </div>
        <div class="gx-seal-wrap">
          <button type="button" class="gx-seal" :class="{ 'is-open': unlocked }" :aria-pressed="unlocked" :aria-label="unlocked ? 'Close the lock' : 'Open the lock'" @click="unlocked = !unlocked">
            <span class="gx-seal-ring" aria-hidden="true"></span>
            <span class="gx-seal-ring gx-seal-ring--inner" aria-hidden="true"></span>
            <span class="gx-seal-ticks" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
            <span class="gx-seal-keyhole" aria-hidden="true"><i></i></span>
            <span class="gx-seal-stamp" aria-hidden="true"></span>
          </button>
          <button class="gx-seal-switch" :aria-pressed="unlocked" @click="unlocked = !unlocked">
            <span>{{ unlocked ? 'Open' : 'Locked in' }}</span><span>· press to {{ unlocked ? 'lock' : 'open' }}</span>
          </button>
        </div>
        <div class="gx-telemetry">
          <div><strong>...</strong><span>Listings open</span></div>
          <div><strong>...</strong><span>ETH filled</span></div>
          <div><strong>...</strong><span>$LORH burned</span></div>
          <p>$LORH and the Holdavia market are live on Robinhood Chain. List a bag or buy one at holdavia.xyz. Community-built. Not affiliated with any brokerage, launchpad or social network.</p>
        </div>
      </section>

      <section id="rail" class="gx-scene">
        <p class="gx-tag"><span class="gx-tag-rule" aria-hidden="true"></span><span>Rail</span></p>
        <h2>Every bag hangs in public, with its price on the tag.</h2>
        <p class="gx-note">Sample rail. These six bags show what a listing makes visible. The live rail opens with the market.</p>
        <ol class="gx-rail" tabindex="0">
          <li v-for="listing in listings" :key="listing.coin" class="gx-rail-plate">
            <span class="gx-rail-pct">{{ listing.discount }}%</span>
            <small class="gx-rail-under">UNDER THE POOL</small>
            <div class="gx-rail-tag"><strong>{{ listing.coin }}</strong><span>locked {{ listing.lock }}</span><span>{{ listing.eth }} ETH left</span></div>
          </li>
        </ol>
        <div class="gx-legend">
          <div><strong>On the lock</strong><span>how far under the pool price the bag is listed</span></div>
          <div><strong>On the tag</strong><span>the coin, the lock length, and how much is left to buy</span></div>
          <div><strong>On the rail</strong><span>everything open right now, deepest discount first</span></div>
        </div>
      </section>

      <section class="gx-plate">
        <figure class="gx-plate-figure">
          <picture><source media="(max-width: 719px)" srcset="/art/fence-sm.webp" /><img src="/art/fence.webp" alt="Padlocks secured to a dark wire fence" /></picture>
          <figcaption class="gx-plate-caption"><p>A locked bag is worth less than a liquid one.</p><p>The gap is the market.</p></figcaption>
        </figure>
      </section>

      <section id="time-lock" class="gx-scene">
        <p class="gx-tag"><span class="gx-tag-rule" aria-hidden="true"></span><span>Time lock</span></p>
        <h2>A deal that closes like a vault door: once, and on a clock.</h2>
        <figure class="gx-thumb">
          <picture><source media="(max-width: 719px)" srcset="/art/timelock-sm.webp" /><img src="/art/timelock.webp" alt="Three dials of a vault time lock" /></picture>
          <figcaption>Set once. Visible until it opens.</figcaption>
        </figure>
        <div class="gx-signal-stage">
          <div class="gx-steps-rail">
            <article v-for="step in flowSteps" :key="step[0]" class="gx-step">
              <span class="gx-step-no">{{ step[0] }}</span>
              <h3>{{ step[1] }}</h3>
              <p>{{ step[2] }}</p>
            </article>
          </div>
          <div class="gx-signal">
            <div class="gx-signal-dial" aria-hidden="true"><i></i><i></i><i></i><span class="gx-signal-label">LOCK<br /><small>ONCE</small></span></div>
            <div class="gx-signal-pool"><span>POOL PRICE</span><strong>moved 0.0% by this deal</strong></div>
            <div class="gx-signal-actors"><span>SELLER</span><b>ESCROW</b><span>BUYER</span><span>NEXT BUYER</span><span>BURNER</span></div>
            <div class="gx-signal-fees"><em>2%</em><em>1%</em></div>
            <p>Pool price through all five steps: unchanged</p>
          </div>
        </div>
      </section>

      <section id="combination" class="gx-scene">
        <p class="gx-tag"><span class="gx-tag-rule" aria-hidden="true"></span><span>Combination</span></p>
        <h2>Dial in a discount. See what the pool would have cost.</h2>
        <figure class="gx-thumb">
          <picture><source media="(max-width: 719px)" srcset="/art/bag-sm.webp" /><img src="/art/bag.webp" alt="A canvas pouch secured with a padlock" /></picture>
          <figcaption>The bag, before it moves.</figcaption>
        </figure>
        <div class="gx-workbook">
          <div class="gx-dial">
            <div class="gx-dial-read"><strong>{{ discount }}%</strong><span>UNDER THE POOL</span></div>
            <input v-model.number="discount" class="gx-slider" type="range" min="0" max="60" step="1" aria-label="Discount under the pool price" />
            <div class="gx-scale"><span>0</span><span>10</span><span>20</span><span>30</span><span>40</span><span>50</span><span>60</span></div>
            <p class="gx-help">A live comparison against the pool price.</p>
            <label class="gx-field"><span>Pool depth, ETH side</span><div><input v-model.number="poolDepth" type="number" min="1" step="1" /><b>ETH</b></div></label>
            <label class="gx-field"><span>Bag value at the pool price</span><div><input v-model.number="bagValue" type="number" min="0.01" step="0.1" /><b>ETH</b></div></label>
            <div class="gx-lockchoice"><span>Lock length</span><div><button v-for="value in ['24h', '3d', '7d', '30d']" :key="value" :class="{ 'is-on': lockLength === value }" @click="setLock(value)">{{ value }}</button></div><small>Filled now, it would unlock {{ unlockDate }}.</small></div>
          </div>
          <div class="gx-ledger">
            <div class="gx-ledger-row"><span>The seller receives</span><div><p><small>Sold into the pool</small><output>{{ sellerPool.toFixed(3) }} ETH</output></p><em>pool price falls {{ (poolDrop * 100).toFixed(1) }}%</em><p><small>Listed on Holdavia</small><output>{{ listedValue.toFixed(3) }} ETH</output></p><em class="gx-good">pool price moves 0.0%</em></div></div>
            <div class="gx-ledger-row"><span>The buyer pays for the same tokens</span><div><p><small>Bought from the pool</small><output>{{ poolBuy === null ? 'Too shallow' : `${poolBuy.toFixed(3)} ETH` }}</output></p><em>{{ poolBuy === null ? 'bag is larger than pool depth' : 'liquid at once' }}</em><p><small>Filled on Holdavia</small><output>{{ filledValue.toFixed(3) }} ETH</output></p><em>locked {{ lockLength }}</em></div></div>
            <div class="gx-burn"><span>Burned on this fill</span><output>{{ burnValue.toFixed(4) }} ETH</output><small>of $LORH, bought and destroyed</small></div>
            <p class="gx-footnote">Past {{ breakEven.toFixed(1) }}% the pool would pay this seller more ETH. The listing buys one thing only: a chart that does not move.</p>
          </div>
        </div>
      </section>

      <section id="old-locks" class="gx-scene">
        <p class="gx-tag"><span class="gx-tag-rule" aria-hidden="true"></span><span>Old locks</span></p>
        <h2 class="gx-wide">Lockers ask holders to wait for nothing. Pools punish anyone with size.</h2>
        <details open class="gx-fold">
          <summary class="gx-fold-summary"><span>Compare the two lock models</span><ChevronDown :size="18" aria-hidden="true" /></summary>
          <div class="gx-fold-body">
            <ol class="gx-issues">
              <li v-for="(issue, index) in oldLockIssues" :key="issue[0]"><span>{{ String(index + 1).padStart(2, '0') }}</span><h3>{{ issue[0] }}</h3><p>{{ issue[1] }}</p></li>
            </ol>
            <table class="gx-compare">
              <thead><tr><th scope="col">Token lockers</th><th scope="col">Holdavia</th></tr></thead>
              <tbody><tr v-for="row in oldLocks" :key="row[0]"><td>{{ row[0] }}</td><td>{{ row[1] }}</td></tr></tbody>
            </table>
            <p class="gx-close-line">Time is worth money, and a market can price it. A seller who takes ETH today accepts a lower price. A buyer who can wait pays less.</p>
          </div>
        </details>
      </section>

      <section id="keys" class="gx-scene">
        <p class="gx-tag"><span class="gx-tag-rule" aria-hidden="true"></span><span>Keys</span></p>
        <h2>A position is a key with a date stamped into it.</h2>
        <div class="gx-keys">
          <div class="gx-keys-copy">
            <p class="gx-lead">The tokens sit in escrow. The key moves. Whoever holds it when the clock reaches zero can claim the whole bag.</p>
            <figure class="gx-thumb gx-thumb--tag">
              <picture><source media="(max-width: 719px)" srcset="/art/keytag-sm.webp" /><img src="/art/keytag.webp" alt="A metal key tag marked with a lock" /></picture>
              <figcaption>POSITION / THE RIGHT TO CLAIM</figcaption>
            </figure>
            <div class="gx-ticket">
              <div class="gx-ticket-head"><KeyRound :size="18" aria-hidden="true" /><span>POSITION #0084</span><span class="gx-ticket-live">TRANSFERABLE</span></div>
              <div class="gx-ticket-body"><strong>0.42 ETH</strong><span>unlock 18 Oct · 14:08 UTC</span><div class="gx-ticket-meter"><i></i></div><small>Claimable by the current holder</small></div>
            </div>
          </div>
          <div class="gx-keylist">
            <div><span>01</span><h3>Visible before you buy</h3><p>Lock length, discount, amount left, seller history and unlock date sit on the listing.</p></div>
            <div><span>02</span><h3>Tradable while locked</h3><p>Sell the position for ETH if the date no longer works for you. Tokens never touch the pool.</p></div>
            <div><span>03</span><h3>Claimable by anyone</h3><p>A keeper can trigger the release on the date. The escrow only sends tokens to the current key holder.</p></div>
          </div>
        </div>
        <div class="gx-record">
          <div><p class="gx-submark">What a position records</p><h3>One fill, one key, one date.</h3></div>
          <dl><div><dt>Coin</dt><dd>the exact token held in escrow</dd></div><div><dt>Amount</dt><dd>the amount this holder can claim</dd></div><div><dt>Unlock</dt><dd>fill time plus the chosen lock length</dd></div><div><dt>Moves</dt><dd>holder changes without moving the tokens</dd></div></dl>
        </div>
      </section>

      <section class="gx-plate gx-plate--open">
        <figure class="gx-plate-figure">
          <picture><source media="(max-width: 719px)" srcset="/art/open-sm.webp" /><img src="/art/open.webp" alt="An open padlock with the key turned" /></picture>
          <figcaption class="gx-plate-caption"><p>The key turns once.</p><p>Then the bag is open.</p></figcaption>
        </figure>
      </section>

      <section id="master-key" class="gx-scene">
        <p class="gx-tag"><span class="gx-tag-rule" aria-hidden="true"></span><span>Master key</span></p>
        <h2>$LORH opens the first ten minutes. It never changes a price.</h2>
        <p class="gx-note">The token adds optional access and a visible burn story. The market price still comes from each listing.</p>
        <div class="gx-matrix">
          <article><span>01 / BURN</span><h3>Every fill buys and burns</h3><p>2% of a primary fill and 1% of a resale goes to the burner.</p></article>
          <article><span>02 / FIRST WINDOW</span><h3>Latch the opening minutes</h3><p>A future launch window can require a visible $LORH threshold for the first ten minutes.</p></article>
          <article><span>03 / PIN</span><h3>Pin a listing on the rail</h3><p>A burn can move a listing to the top of the public rail for 24 hours.</p></article>
          <article><span>04 / CHEAPER FEE</span><h3>Use the token later</h3><p>Future fee payment in $LORH can be 25% cheaper and burned directly.</p></article>
        </div>
        <div id="legacy-workings" class="gx-wire">
          <div class="gx-wire-row">
            <span class="gx-wire-label">TRANSACTIONS</span>
            <div class="gx-node">Web app<small>wallet stays in the browser</small></div>
            <div class="gx-node">Read API<small>listings, coin pages, cards</small></div>
            <div class="gx-node">Past blocks<small>an hour of pool prices</small></div>
          </div>
          <div class="gx-wire-link"><ArrowUpRight :size="20" aria-hidden="true" /><span>READS</span><div class="gx-node gx-node--lens">LockedinLens<small>a whole screen in one call</small></div></div>
          <div class="gx-wire-row gx-wire-row--value">
            <span class="gx-wire-label">VALUE</span>
            <div class="gx-node gx-node--hot">LockedinMarket<small>listings, fills, positions, claims</small></div>
            <div class="gx-node gx-node--hot">LockedinBurner<small>buys $LORH, burns it</small></div>
            <div class="gx-node">$LORH pool<small>curve, then Uniswap V4</small></div>
          </div>
        </div>
        <div class="gx-limits">
          <div><h3>What the contract cannot do</h3><ul><li>No owner function can move escrowed tokens or a seller’s ETH.</li><li>Claims, cancels and resales cannot be paused.</li><li>No upgrade path. A change means a new deployment.</li><li>No price feed on the chain, so no feed to manipulate.</li></ul></div>
          <dl><div v-for="spec in specs" :key="spec[0]"><dt>{{ spec[0] }}</dt><dd>{{ spec[1] }}</dd></div></dl>
        </div>
      </section>

      <section id="strongbox" class="gx-scene">
        <p class="gx-tag"><span class="gx-tag-rule" aria-hidden="true"></span><span>Strongbox</span></p>
        <h2 class="gx-wide">The market keeps nothing. Its fees leave as burned $LORH.</h2>
        <div class="gx-streams">
          <article><p class="gx-submark">A fill</p><div class="gx-stream-bar"><span class="gx-stream-main">98%</span><span class="gx-stream-fee">2%</span></div><div class="gx-stream-cap"><span>the seller, in the same transaction</span><span>buys $LORH and burns it</span></div></article>
          <article><p class="gx-submark">A resale</p><div class="gx-stream-bar"><span class="gx-stream-main">99%</span><span class="gx-stream-fee">1%</span></div><div class="gx-stream-cap"><span>the holder who sold</span><span>buys $LORH and burns it</span></div></article>
        </div>
        <div class="gx-matrix gx-matrix--bars">
          <article><span>PRIMARY FILL</span><strong>98%</strong><p>Seller receives the ETH in the same transaction.</p><div class="gx-track"><i style="width: 98%"></i></div></article>
          <article><span>PRIMARY FILL</span><strong>2%</strong><p>Burner buys and destroys $LORH.</p><div class="gx-track"><i style="width: 16%"></i></div></article>
          <article><span>POSITION RESALE</span><strong>99%</strong><p>Previous holder receives the resale price.</p><div class="gx-track"><i style="width: 99%"></i></div></article>
          <article><span>POSITION RESALE</span><strong>1%</strong><p>Burner fee keeps the key liquid.</p><div class="gx-track"><i style="width: 10%"></i></div></article>
        </div>
        <p class="gx-foot-note">No owner function can withdraw escrowed tokens. A keeper may settle the accumulated burner fee through the approved swap path.</p>
      </section>

      <section id="workings" class="gx-scene">
        <p class="gx-tag"><span class="gx-tag-rule" aria-hidden="true"></span><span>Workings</span></p>
        <h2 class="gx-wide">Two contracts hold the money. Everything else only reads.</h2>
        <div class="gx-wire">
          <div class="gx-wire-row">
            <span class="gx-wire-label">TRANSACTIONS</span>
            <div class="gx-node">Web app<small>wallet stays in the browser</small></div>
            <div class="gx-node">Read API<small>listings, coin pages, cards</small></div>
            <div class="gx-node">Past blocks<small>an hour of pool prices</small></div>
          </div>
          <div class="gx-wire-link"><ArrowUpRight :size="20" aria-hidden="true" /><span>READS</span><div class="gx-node gx-node--lens">LockedinLens<small>a whole screen in one call</small></div></div>
          <div class="gx-wire-row gx-wire-row--value">
            <span class="gx-wire-label">VALUE</span>
            <div class="gx-node gx-node--hot">LockedinMarket<small>listings, fills, positions, claims</small></div>
            <div class="gx-node gx-node--hot">LockedinBurner<small>buys $LORH, burns it</small></div>
            <div class="gx-node">$LORH pool<small>curve, then Uniswap V4</small></div>
          </div>
        </div>
        <div class="gx-limits">
          <div><h3>What the contract cannot do</h3><ul><li>No owner function can move escrowed tokens or a seller's ETH.</li><li>Claims, cancels and resales cannot be paused.</li><li>No upgrade path. A change means a new deployment.</li><li>No price feed on the chain, so no feed to manipulate.</li></ul></div>
          <dl><div v-for="spec in specs" :key="spec[0]"><dt>{{ spec[0] }}</dt><dd>{{ spec[1] }}</dd></div></dl>
        </div>
      </section>

      <section id="pick-proof" class="gx-scene">
        <p class="gx-tag"><span class="gx-tag-rule" aria-hidden="true"></span><span>Pick-proof</span></p>
        <h2 class="gx-wide">Eight ways to cheat it, and what each one costs.</h2>
        <details open class="gx-fold">
          <summary class="gx-fold-summary"><span>Open all eight checks</span><ChevronDown :size="18" aria-hidden="true" /></summary>
          <div class="gx-fold-body">
            <ol class="gx-checks">
              <li v-for="(item, index) in pickProof" :key="item[0]"><span>{{ String(index + 1).padStart(2, '0') }}</span><strong>{{ item[0] }}</strong><em>{{ item[1] }}</em></li>
            </ol>
          </div>
        </details>
      </section>

      <section id="workshop" class="gx-scene">
        <p class="gx-tag"><span class="gx-tag-rule" aria-hidden="true"></span><span>Workshop</span></p>
        <h2>What is on the bench, and what waits its turn.</h2>
        <p class="gx-note">The product ships in public phases. Each phase keeps the market legible before adding another way to move a key.</p>
        <details open class="gx-fold">
          <summary class="gx-fold-summary"><span>View the four phases</span><ChevronDown :size="18" aria-hidden="true" /></summary>
          <div class="gx-fold-body">
            <ol class="gx-phases">
              <li v-for="phase in workshopPhases" :key="phase[0]">
                <p class="gx-phase-label">{{ phase[0] }}</p>
                <h3>{{ phase[1] }}</h3>
                <ul><li v-for="item in phase[2]" :key="item">{{ item }}</li></ul>
                <p class="gx-phase-status">Done when <span>someone outside the team completes the flow.</span></p>
              </li>
            </ol>
            <div class="gx-exclusions"><span>Not on the bench, on purpose</span><strong>Rewards paid for locking</strong><strong>A treasury that holds user funds</strong><strong>Governance</strong><strong>A penalty exit</strong></div>
          </div>
        </details>
      </section>

      <section id="spec-sheet" class="gx-scene">
        <p class="gx-tag"><span class="gx-tag-rule" aria-hidden="true"></span><span>Spec sheet</span></p>
        <h2>Decisions, and why each one was made.</h2>
        <p class="gx-note">The market stays small enough to inspect: fixed fees, fixed lock lengths, no upgrade path and no hidden price feed.</p>
        <details open class="gx-fold">
          <summary class="gx-fold-summary"><span>Open decisions and measures</span><ChevronDown :size="18" aria-hidden="true" /></summary>
          <div class="gx-fold-body">
            <div class="gx-decisions">
              <article v-for="decision in specDecisions" :key="decision[0]"><h3>{{ decision[0] }}</h3><p>{{ decision[1] }}</p></article>
            </div>
            <div class="gx-gauges">
              <div><h3>What gets measured</h3><ul><li>Listings created and first fills</li><li>ETH filled per week</li><li>Resale turnover</li><li>Median discount per lock length</li><li>$LORH burned with ETH spent</li></ul></div>
              <div><h3>Ignored on purpose</h3><ul><li>The token's price</li><li>Follower counts</li><li>Escrow as a headline number</li></ul></div>
            </div>
          </div>
        </details>
      </section>

      <section id="weak-points" class="gx-scene">
        <p class="gx-tag"><span class="gx-tag-rule" aria-hidden="true"></span><span>Weak points</span></p>
        <h2>Every lock has weak points. These are ours.</h2>
        <p class="gx-note">The design makes the trade visible; it cannot remove market risk, smart-contract risk or the need for a buyer.</p>
        <details open class="gx-fold">
          <summary class="gx-fold-summary"><span>Read the holds and weak points</span><ChevronDown :size="18" aria-hidden="true" /></summary>
          <div class="gx-fold-body">
            <div class="gx-weak">
              <div class="gx-weak-col"><p class="gx-weak-label">Holds</p><ul><li>A buyer's saving is fixed and visible before paying.</li><li>One seller with one bag is enough to open a market.</li><li>No upgrade path, owner over funds or price feed.</li></ul></div>
              <div class="gx-weak-col"><p class="gx-weak-label">Can give way</p><ul><li v-for="point in weakPoints" :key="point[0]"><strong>{{ point[0] }}</strong><span>{{ point[1] }}</span></li></ul></div>
            </div>
            <div class="gx-risk">
              <article><h3>A launchpad adds it natively</h3><p>If a launchpad offers locked sales at launch, Holdavia starts after launch, where large bags still need a market.</p></article>
              <article><h3>Sellers do not come</h3><p>Outreach starts with teams whose bags are larger than their pools and who need a clear exit.</p></article>
              <article><h3>Buyers get hurt</h3><p>Short locks by default, seller history on every listing and a resale market keep the holder informed.</p></article>
            </div>
          </div>
        </details>
      </section>

      <section class="gx-closing">
        <div class="gx-finale">
          <div class="gx-finale-locks" aria-hidden="true"><LockKeyhole v-for="n in 7" :key="n" :size="30" :style="{ '--n': n }" /></div>
          <div class="gx-finale-copy"><p>Time is worth money, and a market can price it.</p><span>$LORH · Robinhood Chain</span></div>
        </div>
        <div id="app" class="gx-cta">
          <div class="gx-cta-copy">
            <p class="gx-kicker">$LORH · Robinhood Chain</p>
            <h2>Lock in a discount.<br />The chart never notices.</h2>
            <p>List a bag or buy one at the open market. Every number is public, every date is visible.</p>
          </div>
          <div class="gx-cta-actions">
            <a class="gx-btn gx-btn--solid" href="#combination">Try the dial <ArrowDownRight :size="17" aria-hidden="true" /></a>
            <a class="gx-btn" href="#/docs">Read the docs</a>
          </div>
        </div>
      </section>
    </main>

    <footer class="gx-foot">
      <div class="gx-foot-grid">
        <div class="gx-foot-brand">
          <a class="gx-brand" href="#top"><span class="gx-brand-mark" aria-hidden="true"></span><span class="gx-brand-word">Holdavia</span></a>
          <p>Discounted bags, locked until the date.</p>
          <p class="gx-foot-chain">$LORH · Robinhood Chain</p>
        </div>
        <nav class="gx-foot-nav" aria-label="Hardware">
          <p class="gx-foot-label">Hardware</p>
          <a v-for="item in navItems" :key="item[0]" :href="item[1]">{{ item[0] }}</a>
        </nav>
        <nav class="gx-foot-nav" aria-label="Paperwork">
          <p class="gx-foot-label">Paperwork</p>
          <a href="#/docs">Docs</a><a href="#workings">Workings</a><a href="#spec-sheet">Spec sheet</a><a href="#weak-points">Weak points</a>
        </nav>
      </div>
      <div class="gx-foot-legal"><p>Community-built. Not affiliated with any brokerage, launchpad or social network. $LORH is a utility token for the Holdavia market, not a share or a claim on revenue. Nothing on this page is financial, legal or tax advice.</p><p>© 2026 Holdavia</p></div>
    </footer>

    <nav class="gx-dock" aria-label="Sections">
      <a class="gx-dock-brand" href="#top" aria-label="Holdavia home"><span class="gx-brand-mark" aria-hidden="true"></span></a>
      <a v-for="item in navItems" :key="item[0]" class="gx-dock-link" :href="item[1]">{{ item[0] }}</a>
      <a class="gx-dock-link gx-dock-link--docs" href="#/docs">Docs</a>
    </nav>
  </div>
</template>
