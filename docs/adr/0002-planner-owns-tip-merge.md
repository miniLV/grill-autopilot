# The planner owns the integration tip merge

The hardened protocol first asked each worker to merge the integration tip, rerun Verify and report the post-merge SHA. That bookkeeping is beyond what a cheap model follows reliably. The planner now runs a deterministic DONE check and the tip merge itself, and the reviewer reruns Verify on the candidate. Files-overlap scheduling makes a conflict unexpected, so a conflict blocks the ticket instead of going back to a worker.
