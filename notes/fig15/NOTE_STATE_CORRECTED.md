# Fig. 15 lecture note, revision for the corrected generation 2026-11-18: state of this chat

Chat: the Fig. 15 note writer (session_01DGmqiqazJ9UxECtFYiespR). Branch `claude/fig15-note-corrected`, from origin/main 808c91a.
Order: the Fig. 15 coordinator (session_01DGmqinbgPZhEHKndFyAjfV), 18 Nov ~20:34 UTC, on the owner's order "finish everything".

## Aim
Rewrite the note (public/scripts/resonant-note.js) for generation 2026-11-18: sections 10 and 11 new (staircase cause measured,
exact wall reference, (x, rho) reduction and why it is exact, gate, T_unc / provisional, kept and replaced); every sentence of
sections 6-9, 12, 13 true for the new numbers; NUM block from notes/fig15/gen2_numbers.py reading 2026-11-18/kaggle/index.json
(T_ref where T_far or the twin's T was used).

## Rules (owner and coordinator)
- No runs in the container except the pure index read by gen2_numbers.py; no GPU, no Kaggle launch, no R2 action.
- Derive, never assert (notes/STANDARD.md). Never write the owner's name or e-mail.
- Readers: at most two rounds in total (one referee + one derivation checker), owner watching cost.
- Build, check in headless Chromium (no KaTeX errors, numbers = NUM), merge to main, verify live.
- Reply to the coordinator in at most 8 lines; message no other session.

## Done
- (nothing yet)

## Left
- read THEORY_AND_CODE.md, the new index; adapt gen2_numbers.py; rewrite sections; readers; build; merge; live check; reply.

## Done (draft, before readers)
- gen2_numbers.py reads 2026-11-18 (T_ref everywhere; T_unc, provisional, status), the 2026-11-14 index for bookkeeping, the
  audit json; removed the rt3d2.run1d side-loss computation (a run; banned) and the twin/T_far numbers.
- Note: sections 10 and 11 rewritten (25a-25f); sections 6-9, 12-14 sentences made true (long-packet table now exact vs (18);
  ten walls exact; disc table T_ref, kept lifetimes marked *; shells: one shell already traps, provisional; diode from T_ref).
- docs page updated. Build: 1219 KaTeX, 0 errors, no overflow at 390/1440.
## Left
- one referee round + one derivation-checker round; fix; merge to main; verify live; reply to coordinator (<= 8 lines).

## Readers (the one allowed round)
- Referee: 8 errors + 29 stops. Derivation checker: 7 errors (equations 25a-25f and the 515-value NUM block otherwise check).
- Fixed: time-step claim (changes up to 0.002), (25e) stray semicolon, disc difference ~0.046, shell comparison (wider pair at
  R3 lives longer; R5 bounds cannot be ranked), long-packet gap ~1e-3 stated as untraced, fit-rule sign reconciled (1.7 % long,
  unrounded), kept-run asterisks, shell accuracy (~0.0012 in two tests), equation order ((25f) -> (26a)), inside share from |chi|^2
  not flux, biased walls' two independent checks (26 kept; one (x, rho) run), V0 = 3 ratio range filter stated, k/k_R reason,
  (x, rho) grid stated, shell faces, rho/phi flagged, (25d) absorbed part, sigma_E range for the diode.
- Not fixed: shell run lengths, the two out-of-date correction docs (545 vs 745), the twin lifetime 15.3 (not re-checkable).
