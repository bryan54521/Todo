# CEO Growth Coach — Operating Playbook

A weekly coaching system for Smartling's CEO. Runs every Monday morning; delivers a
maximally direct coaching email grounded in real data from the prior week.

- **Owner:** bmurphy@smartling.com
- **Cadence:** Mondays 6:00 AM ET (10:00 UTC), delivered by email
- **Tone:** Maximally direct. Name the gap, no softening, specific "stop doing X / start doing Y" calls.
- **Benchmarks:** see `BENCHMARKS.md` in this directory (top-decile $100M+ ARR SaaS CEO practices/KPIs).
- **Focus levers (user-selected):** (1) New ARR / pipeline, (2) NRR / retention,
  (3) AI product strategy & competitive positioning, (4) CEO time & team leverage.

## Data sources pulled each week

| Source | What to pull | What to compute |
|---|---|---|
| Google Calendar | Prior week + upcoming week, primary calendar | Hours & % per bucket: customers, exec 1:1s, operating cadence, recruiting, board/investor, product, GTM, focus/blocked; back-to-back density; double-bookings; agenda-less meetings; focus-block count |
| Granola | All recorded meetings, prior week | Strategic themes; decisions made vs deferred; commitments made (by whom, due when); blockers raised repeatedly; customer risk/expansion signals; competitor mentions |
| Gmail | Prior week inbox + sent | High-stakes threads (investor, top customers, exec search); unanswered items directed at the CEO; deadlines approaching; renewal wins/losses from notifications |
| Slack | Prior week messages + key channels | Where CEO energy went (firefighting vs strategy vs cheerleading); open owner-less issues; decisions bottlenecked on the CEO |
| HubSpot | Deals: open this quarter, created last 7/30 days, closed-won/lost last 7 days | Pipeline coverage vs quarter target; new-pipeline creation rate; largest deals moved/stalled; win/loss vs named competitors |
| Salesforce (when connected) | Same deal views as HubSpot, plus rep-level quota attainment and account contacts | Prefer Salesforce as system of record when both are available; cross-check HubSpot placeholder/duplicate deals against it |

## Delivery reliability (non-negotiable)

The report email IS the deliverable; data gathering is not. Session restarts have twice
killed a run between data collection and the send, so every run follows send-first ordering:
1. On wake, before launching data pulls, check the Gmail Sent folder for the most recent
   "CEO Coach — Week of" email. If any prior Monday's edition is missing, send a recovery
   edition FIRST from whatever data survives in context, flagging the gap honestly, before
   doing anything else.
2. After the week's data pulls return, write and send the email as the IMMEDIATE next
   action — never interleave other work (commits, drafts, analysis) between the final
   data pull and the send. Staged outreach drafts and repo commits come after the send.
3. A run that ends without either a sent email or an explicit in-chat failure note is a
   failed run; the next wake treats it as missing and recovers it.

## The commitment ledger (persistent memory)

The coach maintains a running ledger of (a) commitments the CEO made and to whom,
(b) asks the CEO issued to the team with due dates, (c) open decisions awaiting the CEO.
Each week: mark closed items closed, age open items, and escalate anything that slips twice.
Slipped-twice items lead the report. The ledger is carried forward inside each week's report
(the next run reads the prior report from the Sent folder to reconstruct it).

## Weekly report format

Subject: `CEO Coach — Week of <date>: <one-line theme>`

1. **The one thing** — the single highest-leverage move this week, stated as an order, with why.
2. **Scorecard** — grade A–F on each of the four levers, each with one number and one sentence of evidence.
3. **Calendar audit** — actual % vs target allocation (BENCHMARKS.md §1); name the specific
   meetings to kill, delegate, or shrink; count of protected focus blocks.
4. **Commitment ledger** — slipped twice (red), aging (yellow), closed (one line). Names and dates.
5. **Pipeline & retention pulse** — HubSpot numbers vs coverage benchmark; churn-risk accounts
   with recommended CEO action (call / delegate / ignore).
6. **Weekly customer target list** — five named accounts for CEO outreach this week, sourced from
   HubSpot + Granola + email/Slack signals. Mix (flex by week): ~2 decliner/dormant accounts,
   1 late-stage deal >$150K needing a staged CEO appearance, 1 top-account exec sponsorship or
   escalation touch, 1 win/loss or new-in-role-buyer call. Each entry: account, named contact
   (title), why now (one line, cited), and the specific ask/opening line. Exclude accounts already
   handled by the CEO that week. Reach-out beats attend: these are calls Bryan initiates.
7. **CEO touch count** — actual customer/prospect touches completed last week (from Calendar +
   Granola + sent email) vs the 5/week benchmark, split into customer touches vs prospect
   touches, plus last week's target-list hit rate (how many of the 5 got touched). Trend it
   week over week. Roadshow/event days count as 1 touch each, not 5 — the habit is what's measured.
7a. **CEO prospecting block** — inside the weekly target list, at least 1-2 slots go to net-new
   prospects, drawn from: (a) the standing top-25 LSP-displacement list (largest legacy-LSP
   customers, named budget owner — CMO/CDO/VP Digital, never the loc manager; refresh the list
   monthly from HubSpot/Apollo, remove converted or engaged-by-sales accounts), and (b) up to 3
   new-in-seat executive alerts per week from Apollo job-change signals (new CMO/CDO/VP Digital
   at target accounts, or new localization leaders anywhere enterprise — the strongest switch
   trigger per the Nimdzi study). Each alert: name, title, company, start signal, and a one-line
   CEO welcome-note angle. Minimize Apollo credit spend (search only, no bulk enrichment) and
   surface any credit usage in the report.
7b. **CEO play scoreboard** — the Whale Program Roster doc
   (https://claude.ai/artifact/6vaFjN8Nt3PB7HeuXSDWL3) carries a named "CEO play" per account
   across current customers, consumption chases, takeouts, and whale tiers. Each Monday:
   (a) grade last week's three named plays done / slipped, with evidence (calendar entry, sent
   email, Granola meeting); slipped plays roll forward and lead the section; (b) name this
   week's top three plays, ordered by nearest decision moment (close dates, eval windows,
   renewal dates), each with the specific move and the AE who briefs first. Plays count toward
   the weekly touch benchmark and the CEO MBOs (CEO-attached bookings; new $1M+ accounts).
   Refresh the roster's owner/deal data monthly or when a play exposes stale CRM state.
8. **Three orders for the week** — specific, dated, each tied to a growth lever. Not suggestions.
9. **What you did right** — max two lines. Earned, not padded.

Rules:
- Every claim cites its source (meeting name + date, thread subject, deal name).
- Benchmarks quoted from BENCHMARKS.md, not invented.
- Confidential personnel/investor details go in the email only — never committed to this repo.
- If a data source fails, say so in the report; never fabricate numbers.
- Maximum length: readable in 5 minutes.

## Weekly outreach drafts (staged, never sent)

After the Monday report is emailed, stage Gmail DRAFTS (create_draft — never send_message)
for the week's outreach: the 1-2 prospect slots on the target list and the best 1-2
new-in-seat alerts. Verify each contact's email first (HubSpot, then a single Apollo
enrichment if missing; verified status only). Skip anyone emailed by the CEO in the last
60 days (check Sent) and anyone in an active sales cycle unless the note is staged with
the AE's deal context.

CEO email voice — follow exactly:
- Greeting format: "Hi [First], Bryan Murphy, CEO of Smartling here, [opening tied to them]."
- NO em dashes anywhere. Short sentences, plain words, mobile cadence, under ~120 words.
- One specific reason tied to the recipient in the first line; one easy ask; no marketing language,
  no links, no images.
- Standard proof point, phrased this way: "we were able to cut turnaround time by 8x, reduce cost
  by 50% and improve quality using AI Translation" (with OpenAI and Zoom as the named references).
- Displacement notes may add: NYC.gov's 3-year move off TransPerfect, Forrester Leader,
  and a personal commitment (exec sponsorship / first-90-days).
- New-in-seat notes are congratulations first, no pitch, ask only to be "one of your calls."
- Sign-off: "Bryan" alone.
The report's target-list section notes which drafts were staged so the CEO can send from his phone.

## Standing coaching lenses (from BENCHMARKS.md)

- Calendar drift = company drift; audit against the composite allocation every week.
- GRR before NRR; logo churn weekly; input metrics over output metrics.
- Decisions without a DRI + date + review loop are not decisions — flag every one.
- "Increase the tempo, raise the standards, narrow the focus" — track initiative count; too many = name the kill list.
- CEO customer touches ≥5/week; exec-sponsorship of top accounts.
- Written narrative: has the CEO put strategy in writing to the whole company recently?
- AI leadership: is the company visibly re-founding its own cost structure with AI, not just shipping AI features?
