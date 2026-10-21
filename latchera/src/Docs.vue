<script setup>
import { ArrowLeft } from 'lucide-vue-next'

const contents = [
  ['Overview', 'overview'],
  ['How a deal works', 'deal'],
  ['Listings', 'listings'],
  ['Positions', 'positions'],
  ['Discount', 'discount'],
  ['Fees and the burn', 'fees'],
  ['$LORH', 'token'],
  ['Token launch', 'launch'],
  ['Contracts', 'contracts'],
  ['Public record', 'record'],
  ['Questions', 'faq']
]

const dealSteps = [
  ['01', 'List the bag', 'A seller lists tokens with a price in ETH and a lock length. The whole amount moves into the market contract.'],
  ['02', 'Fill the listing', 'A buyer pays the listed price for all or part of the bag. The seller receives the ETH, less the 2% fee, in the same transaction.'],
  ['03', 'Mint a position', 'The buyer receives a locked position: the right to claim those tokens after the unlock time.'],
  ['04', 'Move the key', 'The holder waits for the date and claims, or sells the position to someone else before it.'],
  ['05', 'Release on the date', 'At the unlock time, whoever holds the position receives the full amount of tokens.']
]

const listingSpecs = [
  ['Token', 'Any coin launched through Pons, checked against the launch factory on the chain'],
  ['Amount', 'Escrowed in full the moment the listing is created'],
  ['Price', 'Set by the seller in ETH per token, fixed for the life of the listing'],
  ['Lock length', '24 hours, 3 days, 7 days or 30 days'],
  ['Fills', 'Partial fills allowed, from 0.01 ETH per fill'],
  ['Minimum size', '0.05 ETH for the whole listing'],
  ['Lifetime', '7 days; after that the unsold part can only go back to the seller'],
  ['Cancel', 'The seller may cancel the unsold part at any time; filled parts stay sold']
]

const discountSteps = [
  ['01', 'Sample the pool', 'The app reads each listed coin\'s pool price at sixty moments, one minute apart, from the chain\'s own past blocks.'],
  ['02', 'Build the reference', 'The reference price is the mean of the last 60 samples, so a one-minute push of the pool cannot inflate a discount.'],
  ['03', 'Calculate the display', 'Discount = 1 - listing price / reference price.'],
  ['04', 'Show the comparison', 'The listing page shows the reference, the live price and the listing price side by side.'],
  ['05', 'Require enough history', 'A coin with fewer than 30 samples shows "not enough price history" instead of a number.']
]

const marketFunctions = [
  ['createListing', 'Token must come from the Pons factory; the deposit must deliver the exact amount; a listing is worth at least 0.05 ETH and holds at least one millionth of the coin\'s supply.'],
  ['fill', 'Checks the first window, the buyer\'s maximum price and the amount left; then mints the position.'],
  ['cancel', 'Seller only, and the unsold part only. Filled parts cannot be cancelled.'],
  ['sweepExpired', 'Anyone may call it; it returns an expired listing\'s remainder to its seller.'],
  ['claim', 'Anyone may call it at or after the unlock time; payment goes to the position\'s current holder.'],
  ['offerPosition / buyPosition', 'Resale at a fixed ETH price; the buyer names the most they will pay.'],
  ['pin', 'The seller burns $LORH to pin their own listing: one day for every 25,000 tokens.'],
  ['withdraw', 'Pays out ETH a seller\'s address did not accept when it was paid, to an address that seller names.']
]

const badges = [
  ['First fill', 'The first position a wallet buys'],
  ['Held to unlock', 'Positions claimed by the wallet that bought them'],
  ['Thirty days', 'A 30-day position held to its date'],
  ['Never sold early', 'Five or more positions held to their date and none sold before it'],
  ['Second hand', 'Bought someone else\'s position and held it to the date'],
  ['Early position', 'One of the first 1,000 positions ever created'],
  ['Straight seller', 'Ten listings created and none cancelled after a first fill']
]

const questions = [
  ['Can I get my tokens before the date?', 'No. A position cannot be claimed before its unlock time, by anyone, for any fee. You can sell the position to another buyer if one wants it.'],
  ['What if the coin falls during the lock?', 'Then the position is worth less, exactly as the tokens would be. A coin can fall by more than its discount, and it can fall to zero. The discount is a lower entry price, nothing more.'],
  ['Who can list?', 'Anyone holding a coin launched through Pons. There is no approval and no allow-list of sellers.'],
  ['Can the team take the escrowed tokens?', 'The design has no function for it. Tokens leave escrow in three ways only: a claim by the position\'s holder, a cancel of the unsold part by the seller, or the return of an expired listing\'s remainder.'],
  ['Is the code reviewed?', 'Not yet. The source will be verified on the explorer before the first listing, and an external review is planned from the launch listing\'s ETH. A review reduces the chance of an error; it does not remove it.']
]

const hardwareLinks = [
  ['Rail', '#rail'],
  ['Time lock', '#time-lock'],
  ['Combination', '#combination'],
  ['Keys', '#keys'],
  ['Master key', '#master-key']
]

const paperworkLinks = [
  ['Docs', '#/docs'],
  ['Workings', '#workings'],
  ['Spec sheet', '#spec-sheet'],
  ['Weak points', '#weak-points']
]

</script>

<template>
  <div class="lt-app lt-app--docs">
    <header class="lt-command lt-command--docs">
      <a class="lt-sigil" href="#top">
        <span class="lt-sigil-mark" aria-hidden="true"></span>
        <span class="lt-sigil-name">Latchera</span>
      </a>
      <nav class="lt-docs-nav" aria-label="Docs">
        <a href="#top"><ArrowLeft :size="16" aria-hidden="true" /> Back to home</a>
        <span>$LORH - Robinhood Chain</span>
      </nav>
    </header>

    <main class="lt-docs">
      <section class="lt-docs-hero">
        <p class="lt-kicker">Docs / How the lock works</p>
        <h1>How the lock<br /><span>works.</span></h1>
        <p class="lt-lede">How the Latchera market works, what its contracts can and cannot do, and what is still a proposal. The market is live on Robinhood Chain.</p>
      </section>

      <nav class="lt-docs-index" aria-label="On this page">
        <p class="lt-docs-index-label">On this page</p>
        <a v-for="(item, index) in contents" :key="item[1]" :href="`#/docs/${item[1]}`"><span>{{ String(index + 1).padStart(2, '0') }}</span>{{ item[0] }}</a>
      </nav>

      <div class="lt-docs-body">
        <section id="overview" class="lt-doc-block">
          <header class="lt-doc-head"><p class="lt-doc-tag">Overview</p><h2>The market is simple to watch.</h2></header>
          <div class="lt-prose">
            <p>Latchera is a market on Robinhood Chain for locked bags. A holder sells tokens below the pool price in exchange for a lock. The buyer pays ETH today and receives a position that unlocks on a set date. The position can itself be sold, so the tokens never reach the pool before the date.</p>
            <ul class="lt-dot-list"><li>Sellers get ETH without selling into a thin pool.</li><li>Buyers pay less than the pool price and accept a wait.</li><li>Every other holder sees the sale in public, with its unlock date, instead of finding out from a candle.</li></ul>
            <p class="lt-note"><strong>Note</strong><span>Status: live on Robinhood Chain. Items marked as proposed are later phases or settings that are not final.</span></p>
          </div>
        </section>

        <section id="deal" class="lt-doc-block">
          <header class="lt-doc-head"><p class="lt-doc-tag">How a deal works</p><h2>Five events, one escrow.</h2></header>
          <div class="lt-steps lt-steps--docs"><article v-for="step in dealSteps" :key="step[0]"><span>{{ step[0] }}</span><div><h3>{{ step[1] }}</h3><p>{{ step[2] }}</p></div></article></div>
          <p class="lt-after">The pool takes part in none of these steps. Its price does not move and its liquidity is not used.</p>
        </section>

        <section id="listings" class="lt-doc-block">
          <header class="lt-doc-head"><p class="lt-doc-tag">Listings</p><h2>Everything needed to fill is on the tag.</h2></header>
          <dl class="lt-def"><div v-for="row in listingSpecs" :key="row[0]"><dt>{{ row[0] }}</dt><dd>{{ row[1] }}</dd></div></dl>
          <p class="lt-after">Creating a listing is free. Cancelling is free. A listing priced above the pool is allowed; the app labels it "above market" and leaves it off every discount board.</p>
        </section>

        <section id="positions" class="lt-doc-block">
          <header class="lt-doc-head"><p class="lt-doc-tag">Positions</p><h2>A position is a transferable ERC-721 key.</h2></header>
          <div class="lt-prose"><p>Every fill creates one position, owned by the buyer. It is a standard transferable token (ERC-721) that records the coin, the amount, the unlock time and the listing it came from. The unlock time is the fill time plus the listing's lock length.</p><p>Two fills of one listing can unlock on different days. A position cannot be split and cannot be claimed before its date. There is no penalty exit. The way out before the date is to sell the position. After the unlock time anyone may trigger the release; the tokens can only go to the current holder.</p></div>
          <h3 class="lt-subhead">Selling a position</h3>
          <p>The holder sets an ETH price. The app shows the discount that price gives the next buyer for the time left on the lock. When a buyer pays, the position moves to them, the ETH goes to the seller, 1% is burned, and the unlock date does not change.</p>
        </section>

        <section id="discount" class="lt-doc-block">
          <header class="lt-doc-head"><p class="lt-doc-tag">Discount</p><h2>The number is a comparison, not a price feed.</h2></header>
          <div class="lt-prose"><p>The contract has no price feed. It knows one number: the ETH price the seller asked for. The discount shown in the app is a display, and it never changes what a buyer pays.</p></div>
          <div class="lt-steps lt-steps--docs lt-steps--plain"><article v-for="step in discountSteps" :key="step[0]"><span>{{ step[0] }}</span><div><h3>{{ step[1] }}</h3><p>{{ step[2] }}</p></div></article></div>
          <p class="lt-note"><strong>Note</strong><span>A wrong number on screen cannot cost a buyer more than they agreed to: a fill carries the buyer's maximum price, and the contract compares it with the listing's price.</span></p>
        </section>

        <section id="fees" class="lt-doc-block">
          <header class="lt-doc-head"><p class="lt-doc-tag">Fees and the burn</p><h2>The fee stream is visible in every fill.</h2></header>
          <div class="lt-fee-matrix"><div><strong>98%</strong><span>A fill to the seller, in the same transaction</span></div><div><strong>2%</strong><span>A fill to the burner: buys $LORH and burns it</span></div><div><strong>99%</strong><span>A resale to the holder who sold</span></div><div><strong>1%</strong><span>A resale to the burner, through the same path</span></div></div>
          <div class="lt-prose lt-prose--fees"><p>There is no treasury share of these fees and no address that can redirect them. The buyer pays the listed price and nothing on top. Claiming costs only the network fee.</p><h3 class="lt-subhead">The burner</h3><p>Anyone may call it. It buys $LORH with the ETH it holds and burns what it receives. One buy is small: a fixed share of the ETH in the market it buys on, sized so that the price it moves is less than a trade round it costs in fees. What was spent comes back as allowance over ten minutes. It keeps the last five prices it wrote down, a quarter of an hour apart at the least, sets the lowest aside and does not buy more than 5% above the next lowest. A price that was pushed up has to hold for most of an hour before it is bought at. It has no withdraw function. ETH can leave it only as a purchase of $LORH.</p></div>
        </section>

        <section id="token" class="lt-doc-block">
          <header class="lt-doc-head"><p class="lt-doc-tag">$LORH</p><h2>A utility token for the market.</h2></header>
          <div class="lt-prose"><p>The market is complete without the token. Holding it changes when you can act, and every fill shrinks its supply.</p></div>
          <dl class="lt-def"><div><dt>Burn</dt><dd>2% of every fill and 1% of every resale buys $LORH and burns it.</dd></div><div><dt>First window</dt><dd>For its first 10 minutes a new listing can only be filled by wallets holding 1,000,000 $LORH (proposed).</dd></div><div><dt>Pin</dt><dd>A seller burns $LORH to pin a listing for 24 hours (proposed: 25,000).</dd></div><div><dt>Cheaper fee</dt><dd>Later phase: pay the seller fee in $LORH and pay 25% less.</dd></div></dl>
          <h3 class="lt-subhead">What it never does</h3>
          <ul class="lt-dot-list"><li>It never changes a price. A holder and a visitor pay the same ETH for the same listing.</li><li>It is never required to buy, sell, resell or claim.</li><li>It is never paid out for locking, holding or waiting.</li><li>It gives no vote. There are no settings to vote on.</li></ul>
        </section>

        <section id="launch" class="lt-doc-block">
          <header class="lt-doc-head"><p class="lt-doc-tag">Token launch</p><h2>The first listing proves the loop.</h2></header>
          <dl class="lt-def"><div><dt>Supply</dt><dd>1,000,000,000 $LORH, fixed at launch</dd></div><div><dt>Launchpad</dt><dd>Pons: a bonding curve that graduates into a Uniswap V4 pool</dd></div><div><dt>Pre-mine</dt><dd>None</dd></div><div><dt>Team allocation</dt><dd>None</dd></div><div><dt>Private round</dt><dd>None</dd></div><div><dt>Creator tax</dt><dd>1%, set once at launch (proposed)</dd></div><div><dt>Team purchase</dt><dd>5% of supply bought on the curve in the launch transaction (proposed)</dd></div></dl>
          <p class="lt-after">The team's purchase is sold through the market as listing #1: 30% under the pool, locked 30 days. The ETH goes to the published operations wallet, and its first use is an external review of the market contract. After listing #1 fills, the team holds no $LORH.</p>
          <p class="lt-note"><strong>Note</strong><span>The launchpad's owner can re-point a coin's future creator fees after a public three-day delay. The market does not depend on that income.</span></p>
        </section>

        <section id="contracts" class="lt-doc-block">
          <header class="lt-doc-head"><p class="lt-doc-tag">Contracts</p><h2>Small contracts, clear boundaries.</h2></header>
          <div class="lt-contract"><h3>LockedinMarket</h3><p>Holds listings, fills, positions, resale offers and claims.</p><dl class="lt-def"><div v-for="row in marketFunctions" :key="row[0]"><dt>{{ row[0] }}</dt><dd>{{ row[1] }}</dd></div></dl></div>
          <div class="lt-contract"><h3>LockedinBurner</h3><p>Receives the ETH fees and turns them into burned $LORH. Before graduation it buys on the launchpad curve; after graduation, from the pool.</p></div>
          <div class="lt-contract"><h3>LockedinLens and LockedinArt</h3><p>The lens reads the market for the app, a whole screen in one call. The art contract draws each position's picture on the chain: the coin, the amount, the unlock date and a ring that shows how far the lock has run. Neither holds anything, and replacing either does not touch the market.</p></div>
          <p class="lt-after">Deployed contracts keep the names they were verified under (<code>LockedinMarket</code>, <code>LockedinBurner</code>, <code>LockedinLens</code>). The product built on them is Latchera.</p>
          <div class="lt-prose lt-prose--limits"><h3 class="lt-subhead">What the contracts cannot do</h3><ul class="lt-dot-list"><li>No owner function can move escrowed tokens or a seller's ETH.</li><li>Claims, cancels and resales cannot be paused.</li><li>One switch stops new listings only.</li><li>No upgrade path: a change means a new deployment, and old positions keep working until claimed.</li><li>Fee levels are constants, not settings.</li><li>Coins that tax transfers or change balances by themselves are refused.</li></ul></div>
        </section>

        <section id="record" class="lt-doc-block">
          <header class="lt-doc-head"><p class="lt-doc-tag">Public record</p><h2>Read the chain as it is.</h2></header>
          <p>Every wallet that buys through the market has a public page built only from its history on the chain. It opens without a wallet and can be shared as an image.</p>
          <div class="lt-badges"><article v-for="badge in badges" :key="badge[0]"><strong>{{ badge[0] }}</strong><span>{{ badge[1] }}</span></article></div>
          <p class="lt-after">Badges count positions of at least 0.05 ETH. Filling your own listing pays the 2% fee like any other fill.</p>
        </section>

        <section id="faq" class="lt-doc-block">
          <header class="lt-doc-head"><p class="lt-doc-tag">Questions</p><h2>What the lock cannot promise.</h2></header>
          <div class="lt-faq"><details v-for="(question, index) in questions" :key="question[0]" :open="index === 0"><summary>{{ question[0] }}</summary><p>{{ question[1] }}</p></details></div>
        </section>
      </div>
    </main>

    <footer class="lt-foot">
      <div class="lt-foot-grid">
        <div class="lt-foot-brand">
          <a class="lt-sigil" href="#top"><span class="lt-sigil-mark" aria-hidden="true"></span><span class="lt-sigil-name">Latchera</span></a>
          <p>Discounted bags, locked until the date.</p>
          <p class="lt-foot-chain">$LORH - Robinhood Chain</p>
        </div>
        <nav class="lt-foot-nav" aria-label="Hardware">
          <p class="lt-foot-label">Hardware</p>
          <a v-for="link in hardwareLinks" :key="link[0]" :href="link[1]">{{ link[0] }}</a>
        </nav>
        <nav class="lt-foot-nav" aria-label="Paperwork">
          <p class="lt-foot-label">Paperwork</p>
          <a v-for="link in paperworkLinks" :key="link[0]" :href="link[1]">{{ link[0] }}</a>
        </nav>
      </div>
      <div class="lt-foot-bottom"><p>Community-built. Not affiliated with any brokerage, launchpad or social network. $LORH is a utility token for the Latchera market: not a share, not a security, not a claim on any revenue. A locked position cannot be claimed before its unlock time, and a token can fall by more than its discount, or to zero. Nothing on this page is financial, legal or tax advice.</p><p>Copyright 2026 Latchera</p></div>
    </footer>
  </div>
</template>
