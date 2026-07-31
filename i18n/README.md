# Translations

One file per language, named after its two-letter code. Each holds a single dict
called `TABLE`, keyed by the English source string:

```python
TABLE = {
    "Restart Vexflow": "Vexflow neu starten",
}
```

The key being the English sentence is the whole design. A string with no entry is
shown as it is, so a half-finished table is still an improvement, and a table can
never show a user a bare identifier like `settings.restart.button`.

## Fixing a word in a language that already exists

Edit the file, run the checker, open a pull request:

```bash
./.venv/bin/python test_i18n.py de
```

You do not need to read any other file, and nobody else is editing yours.

## Adding a language

1. Copy the closest existing table to `i18n/<code>.py`. Use the code Deepgram uses
   for that language, since the two lists are meant to line up.
2. Add `("Native name", "<code>")` to `UI_LANGUAGES` in [`config.py`](../config.py),
   in alphabetical order by the native name, Latin scripts before Cyrillic. The name
   stays in its own language and is never translated: somebody who has landed in a
   language they cannot read finds their own by recognising a word, and "Deutsch"
   only helps while it says Deutsch.
3. Translate. Leave in English: product names, model names, and the modifier keys
   (Command, Option, Control, Shift) — those are what is printed on the keyboard.
   Placeholders `{}`, `{app}` and `{vendor}` have to survive in the same number.
4. Run `./.venv/bin/python test_i18n.py <code>` until it is clean.

Optionally, a translated installer pane: `packaging/welcome.<code>.html` and
`conclusion.<code>.html`. The build picks those up on its own, and the English ones
are used when they are absent, so this part can wait.

## What the checker actually checks

```
de   ok    198/198 translated, 0 orphaned, 0 clipped
```

- **translated** — how much of what the interface asks for this table answers.
- **orphaned** — keys nothing asks for any more, usually left behind by a rename in
  the source. They are silently dead, which is why a machine has to find them.
- **clipped** — the useful one. It builds every window in your language and asks each
  control whether the text fits the space it was given. A German button reading
  "Neu star…" is caught here rather than in a screenshot from an annoyed user.

Layout is sized for long languages, so a clip usually means the phrasing can be
shorter rather than that the window needs to grow. If it genuinely cannot be shorter,
say so in the pull request — widening a control is a fine outcome, it just needs to be
a decision rather than an accident.

## What belongs here, and what does not

Only text a person reads. Log lines stay English on purpose: they are grep targets,
they are quoted in the documentation, and they are read by whoever is debugging rather
than by whoever is dictating.
