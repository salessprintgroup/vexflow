# Troubleshooting

Start here: **Settings → Permissions → Keep a diagnostic log**. Logging is off until
you switch it on. Tick it — it starts writing there and then, with no restart —
reproduce the problem, then

```bash
tail -f ~/Library/Logs/vexflow.log
```

or use **Open log**, which appears next to the switch once logging is on. Untick it
when you are done and the file is deleted.

The log never contains what you said. It records timestamps, audio frame counts and
character counts, which is enough to tell every common failure apart.

---

## Nothing happens when I hold the key

**The status line in the menu says "No Deepgram key".** Settings → Keys → paste one.

**The menu shows "No Accessibility permission — hotkeys are dead".** macOS did not
grant the event tap. Settings → Permissions → *Open Settings* for Accessibility, tick
the entry, then **quit and start Vexflow again** — the permission is only read at
launch.

The entry you need to tick is the app that owns the process. Started from
`Vexflow.app`, that is Vexflow (it may appear as "Python"). Started from a terminal,
it is your terminal app.

**Nothing in the log at all when you press the key.** The tap is not seeing the key.
Two common causes:

- **The key does not exist on your keyboard.** Neither the built-in MacBook keyboard
  nor the Magic Keyboard has a *right* Control. Bound to one, Vexflow starts normally
  and simply never fires. The log line `+ hotkeys bound: ptt='…'` at startup tells you
  what it is actually listening for.
- **Another app owns the same key**, including a second copy of Vexflow. Pick a
  different one in Settings → Dictation.

**Every free single modifier is one you type with.** Left Option, Left Command and the
Shift keys all get pressed during ordinary typing, so binding push-to-talk to one of
them opens the microphone constantly. Use a chord instead — *Control + Option* and the
other combined entries in the Settings popup only fire when both keys are down
together, which nothing else does.

**A hotkey change did not take.** Changes apply immediately, but only in the running
process. If you edited `config.py` rather than using Settings, restart Vexflow.

---

## It records but no text appears

Look for the summary line at the end of the recording.

```
. empty (2.3s, 0 frames, audio: no)
```

**`0 frames`** — the stream opened and delivered nothing. This is the classic
post-sleep wedge. Vexflow rebuilds the stream automatically, and restarts itself if
that does not help; you should see `rebuilding stream` or `restarting Vexflow (execv)`
in the log. If it repeats, something else is holding the microphone — check
System Settings → Sound → Input, and quit any conferencing app that may have grabbed it.

**`frames` counted but `audio: no`** — samples arrived and every one was a digital
zero. The input is muted or another app has exclusive use of it.

**Frames and audio, but empty text** — the audio reached Deepgram and came back with
nothing recognised. Usually the wrong language: Settings → Dictation → Language.
Confirm the cloud half works on its own:

```bash
./.venv/bin/python selftest.py
```

That synthesises speech with `say` and streams it through the same code path, using
only your key. If it prints a transcript, the network and key are fine and the problem
is the microphone or permissions.

---

## The text goes to the wrong place, or arrives twice

**Twice:** two copies are running. The single-instance lock normally prevents this, so
it usually means one copy was started by hand and another by the login item.

Quit one of them from its menu bar icon. If you installed from source as well as from
the package, remove one of the two — they are separate installs with separate login
items.

**Wrong window:** the paste goes wherever focus is when the recording *ends*. Do not
switch windows while releasing the key.

**Nothing pastes but the text is on the clipboard:** that is deliberate. Vexflow
refuses to paste after a recording hit its duration limit or after the connection
dropped, because minutes later the focused window is probably not the one you meant.
The menu says so, and Cmd-V still works.

---

## The mic indicator stays on after I finish

The green recording indicator lingers for a second while the last audio uploads and
Deepgram returns the final segments. If it stays on longer than a few seconds, use
**Stop recording** in the menu — it works even when the hotkey tap has died.

---

## Cleanup is not doing anything

- Settings → Cleanup → the checkbox is on.
- Settings → Keys → the line under the provider's key says the vendor accepted it. The
  key is checked when you save it and at every start, so "rejected this key" or "your
  credit balance is too low" appears there rather than nowhere. In the menu, models for
  a vendor with no key are greyed out.
- Cleanup is best-effort by design: a timeout, an error, or a reply that looks wrong
  all fall back to the raw transcript silently, because losing your words would be
  worse than leaving them unpolished.
- To see what it is doing, quit Vexflow and start it from a terminal with
  `VEXFLOW_DEBUG_TRANSCRIPT=1 ./.venv/bin/python vexflow.py`. That logs both the raw
  and the cleaned text, and only for that run — quitting clears it. It is the one mode
  that writes your transcripts to disk.

## Cleanup mangled something

Add the term to your vocabulary: Settings → Cleanup → *Edit vocabulary…*. One term per
line, or `misheard -> correct` to pin a specific fix. It takes effect on the next
recording; no restart needed.

---

## Recognition quality is poor

- **Pick a single language** rather than Multilingual. Multilingual juggles ten
  languages and drops words; a named language is measurably better.
- **Foreign technical terms coming back transliterated is expected** with a named
  language. That is what the cleanup pass and your vocabulary file are for.
- **Check which microphone is live.** The log names it on every recording:
  `* recording [MacBook Pro Microphone]`. A Continuity connection to an iPhone in
  another room is a common surprise.

---

## The interface is in the wrong language

**On a fresh install Vexflow follows macOS.** If your Mac is set to a language Vexflow
has no table for, it falls back to English. Either way, **Settings → Interface
language** overrides it, and the change lands when Vexflow restarts — the button next
to the menu does that for you.

Nothing to fix in a file: the choice is stored as `ui_language` in
`~/Library/Application Support/Vexflow/settings.json`, and an empty value there means
"follow the system".

---

## After a macOS update

Permissions are often reset by a major update. Settings → Permissions → *Re-check*.
If Accessibility shows as granted but hotkeys still do nothing, remove the entry in
System Settings, add it back, and restart Vexflow.

---

## The installer will not open

**"Vexflow-1.2.pkg cannot be opened because it is from an unidentified developer."**
The package is not signed with a paid Apple certificate, so Gatekeeper stops the first
open. Put the package in your Downloads folder and paste this into Terminal:

```bash
xattr -c ~/Downloads/Vexflow-*.pkg && open ~/Downloads/Vexflow-*.pkg
```

Gatekeeper only inspects files carrying the "downloaded from the internet" flag, which
is what `xattr -c` clears; the installer then opens normally. `zsh: no matches found`
means the package is somewhere other than Downloads — move it there and paste again.

Without Terminal, the route depends on the macOS version. On **macOS 15 (Sequoia) and
newer**, dismiss the warning and go to **System Settings → Privacy & Security →
Security → Open Anyway** — Sequoia removed the right-click override that older versions
accepted. On **macOS 14**, right-click the package in Finder, choose **Open**, then
**Open** again in the dialog.

**The install finishes but no icon appears.** The environment build may have failed.
The usual cause is no usable Python on the Mac; install the Command Line Tools with
`xcode-select --install` and run the installer again. The installer's own output is in
the system log — Console → Log Reports → `install.log`.

---

## Starting over

Installed from the package: **Settings → Permissions → Remove Vexflow**, then run the
installer again. Choosing *Remove and Delete My Keys* also clears settings, vocabulary
and Keychain entries.

Installed from source:

```bash
./uninstall.sh --purge   # removes the app, login item, settings, vocabulary and keys
./setup.sh
```

Revoke the Microphone and Accessibility entries in System Settings by hand if you want
a genuinely clean slate — an uninstall script cannot touch those.
