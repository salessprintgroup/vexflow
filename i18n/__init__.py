"""Interface translations, one module per language.

Each module holds a single dict named TABLE, keyed by the English source string. An
English key with no entry here is shown as it is, so a partial table is usable — a
language can arrive half-finished and still be an improvement.

Nothing here imports anything: these are data files that happen to be Python, which is
what keeps them mergeable and reviewable by someone who only reads their own language.
"""
