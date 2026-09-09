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
6. **Three orders for the week** — specific, dated, each tied to a growth lever. Not suggestions.
7. **What you did right** — max two lines. Earned, not padded.

Rules:
- Every claim cites its source (meeting name + date, thread subject, deal name).
- Benchmarks quoted from BENCHMARKS.md, not invented.
- Confidential personnel/investor details go in the email only — never committed to this repo.
- If a data source fails, say so in the report; never fabricate numbers.
- Maximum length: readable in 5 minutes.

## Standing coaching lenses (from BENCHMARKS.md)

- Calendar drift = company drift; audit against the composite allocation every week.
- GRR before NRR; logo churn weekly; input metrics over output metrics.
- Decisions without a DRI + date + review loop are not decisions — flag every one.
- "Increase the tempo, raise the standards, narrow the focus" — track initiative count; too many = name the kill list.
- CEO customer touches ≥5/week; exec-sponsorship of top accounts.
- Written narrative: has the CEO put strategy in writing to the whole company recently?
- AI leadership: is the company visibly re-founding its own cost structure with AI, not just shipping AI features?
