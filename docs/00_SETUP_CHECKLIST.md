DOC: 00_SETUP_CHECKLIST | OWNER: Aarush | CADENCE: one-time
STATUS: active | LAST-UPDATED: 2026-07-17

# SETUP CHECKLIST — the ONLY things Claude cannot do for you
The OS is built. These 3 steps need your hands, then you're clear to implement (nothing more until mid-Aug S0).

## 1. Upload docs to chat-Project Knowledge (Context "+")
Upload every .md in this bundle EXCEPT 14_WEDGE_SCAN_LOG.md (that lives in Drive).
Also: rename your Idea Lock PDF in Context to read "01_IDEA_LOCK" for naming discipline (optional, cosmetic).
Capacity is fine — these are tiny text files.

## 2. Create the Cowork scheduled task
- Claude Desktop → Cowork → Scheduled → New task.
- Frequency: say in plain language "first Monday of every month, 07:30 IST" (monthly IS supported via plain-language/cron).
- Paste the corrected self-contained scan prompt (from chat; wedge W1–W4 baked in).
- Point STEP 3 at the Drive Doc "14_WEDGE_SCAN_LOG".
- TEST NOW: "Run on demand" once. Verify (a) it searches, (b) it actually writes a line to the Drive Doc.
  If append fails → fallback: have it email/print the line, you paste. (Tell me if this happens.)

## 3. Calendar backup
Recurring reminder, first Monday monthly: "confirm wedge scan ran." Belt-and-suspenders.

## DONE = you can start S0 (mid-Aug) with zero setup left. Until then: DSA prep, deadline Aug 5.
