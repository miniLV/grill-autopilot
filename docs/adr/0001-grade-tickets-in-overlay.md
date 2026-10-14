# Grade tickets in the autopilot overlay, not in to-tickets

to-tickets sizes slices for one strong-model context window, but the cheap worker needs smaller, fully decided slices. We grade each ticket in grill-autopilot's own `tickets.md` (split first, then set `Implementer: worker | escalate`) instead of editing the upstream mattpocock/skills companion, so upstream updates stay drop-in. We do not split below one behaviour to reach the cheap model, because every ticket costs one strong-model review.
