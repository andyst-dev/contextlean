# Final compact-context evidence

[Complete results](report.md) · [methodology](methodology.md) · [measurement review](measurement-review.json) · [summary](summary.json) · [checksums](checksums.json).

Ten runs: the unchanged completed Bug Fix pair plus exactly eight new calls. Preliminary validation, one run per condition per task; tested configuration only, no statistical-confidence or universal token-savings claim. Every unfavorable task result is retained in the complete results.

[Offline evidence validator](verify_evidence.py) reconciles all measurements, checksums,
frozen fixtures, semantic transfers and saved solutions without model calls.
Run it with `python3 verify_evidence.py` from this directory.

Bug Fix raw data is published once under [bug-fix](bug-fix); combined records reference those byte-identical copies. The ignored original local evidence remains unchanged. [Provenance](bug-fix/provenance.json) binds the copies to the original. No historical or diagnostic run was substituted.

[Source snapshot](source-snapshot.zip), [source selection](source-selection.json), [initial fixtures](fixtures.zip), [all ten saved solutions](solutions.zip), [new preparation receipts](preparations), [eight-call journal](call-journal.json) and [offline grading](offline-regrade) are retained.
