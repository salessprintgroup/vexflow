# Contributing

This is a small tool with a deliberately small surface. The most useful contributions
are bug reports from real use, especially around sleep, wake and audio device changes,
which is where almost every failure lives.

## Reporting a bug

Include:

1. What you did and what happened.
2. macOS version and Mac model.
3. The relevant lines from the log.

Logging is off until you switch it on in Settings → Permissions; do that, reproduce
the problem, then read `~/Library/Logs/vexflow.log`. The log never contains transcript
text, only timestamps, frame counts and character counts — it is safe to paste. If you
turned on `DEBUG_TRANSCRIPT` to chase something, check what you are pasting before you
paste it.

For "it recorded but nothing appeared", the log line that matters looks like
`. empty (2.3s, 0 frames, audio: no)` — the frame count and the audio flag say whether
the microphone was actually delivering samples.

## Translations

The interface ships in eleven languages and every table is one self-contained file in
[`i18n/`](i18n/). Fixing a clumsy sentence in your own language is the smallest useful
pull request this project has, and it needs no knowledge of the rest of the code —
[`i18n/README.md`](i18n/README.md) is the whole briefing. Tables written by someone who
does not speak the language daily are exactly the ones worth correcting.

## Licensing of contributions

Read this before you write code, because it is easier to decide now than after.

You keep the copyright in what you write. Nothing here asks you to assign it. What you
grant, by opening a pull request, is:

1. **The project's own licence.** Your contribution is licensed to everyone under the
   [MIT License](LICENSE), the same terms as the rest of the code.
2. **A further grant to the maintainer.** You also grant Sales Sprint Group LLC a
   perpetual, worldwide, irrevocable, royalty-free right to use, modify and distribute
   your contribution under *other* terms as well, including a commercial or
   closed-source edition, with no obligation to you and no payment. Practically: this
   project may one day have a paid edition alongside the free one, and this grant is
   what makes that possible without hunting down every past contributor. It takes
   nothing away from you — your contribution stays MIT for you and for everybody else,
   permanently.
3. **Nothing about the name.** No rights in the Vexflow or Sales Sprint Group marks
   move in either direction. See [NOTICE](NOTICE).

Sign your commits off to certify all of it, plus that you actually have the right to
submit the work — that it is yours, or licensed compatibly, and not something you owe
to an employer:

```bash
git commit -s -m "fix: ..."     # appends Signed-off-by: Your Name <you@example.com>
```

That sign-off is your agreement to this section and to the
[Developer Certificate of Origin](https://developercertificate.org/). Pull requests
without it will be asked for it before merge. If you cannot make those certifications
— because your employer owns your output, or the code came from somewhere with other
terms — say so in the pull request instead of signing off, and it will not be merged.

## Before opening a pull request

Run both checks:

```bash
./.venv/bin/python test_deaf.py    # sleep-recovery logic; no mic, network or permissions
./.venv/bin/python selftest.py     # Deepgram path; needs a key, no mic or permissions
```

`test_deaf.py` is the regression net for the deaf-microphone ladder. If you touch
`Session`, `Engine.report_audio_health`, or anything in the `DEAF_*` thresholds, that
test has to still pass.

## What fits this project

- Bug fixes, especially reproducible ones with a test.
- Additional recognition languages in `config.LANGUAGES`.
- New cleanup providers in `config.CLEAN_PROVIDERS` plus a backend in `llm.py`. The
  backend contract is small: take text and a key, return corrected text or `None`.
- Documentation that saves someone an hour.

## What does not

- **Anything that adds a server, telemetry, analytics or an update check.** The claim
  that the only outbound requests are to your chosen vendors has to stay true and
  auditable.
- **Anything that stores transcripts on disk** outside the existing
  `VEXFLOW_DEBUG_TRANSCRIPT` path.
- **Heavy dependencies.** The dependency list is short on purpose: it is what makes the
  network path reviewable in an afternoon. A pull request that adds a framework needs
  to justify itself against that.
- **Freezing the app with PyInstaller.** It would give a nicer permission dialog and
  remove the installer's dependency on a system Python — and it would cost the reader
  the ability to see what is running. The shipped package carries readable source in
  `Vexflow.app/Contents/Resources/app` instead. That trade is made deliberately.
- **App Store packaging.** Apple rejects Accessibility-based text insertion under
  guideline 2.4.5, and `CGEventPost` does not work inside the sandbox. This is settled,
  not unexplored.

## Packaging

`make_release.sh` builds `dist/Vexflow-<version>.pkg` from `packaging/`:

- `launcher.sh` becomes `Contents/MacOS/vexflow` and joins the bundled source to the
  environment in Application Support.
- `bootstrap.sh` creates that environment. It runs both from the installer and from
  the launcher if the environment goes missing, so it has to stay idempotent.
- `postinstall` runs as root and drops to the console user for everything it creates.
- `welcome.html` and `conclusion.html` are the installer's first and last screens.

Test a change to any of those by building and installing on a Mac that has never had
Vexflow, or at least by removing `~/Library/Application Support/Vexflow/venv` first.

## Style

Match what is there. The comments explain *why* a thing is the way it is, usually
because the obvious version failed in production — those comments are load-bearing, so
please keep them accurate rather than tidy.
