# Security

## Reporting a vulnerability

Email **hello@salessprintgroup.org** with "Vexflow" in the subject. Please do not open
a public issue for anything that could expose a user's audio, transcripts or API keys.

Include what you did, what happened, and the macOS version. A proof of concept helps
but is not required.

Reports are read and acted on as time allows. This is a free tool published by a small
company: there is no service level, no guaranteed response time, no bounty, and no
commitment that any particular report will be fixed, or fixed by a particular date. The
software is provided as is under the [MIT License](LICENSE), with no warranty of any
kind — nothing on this page changes that or creates any obligation. Sending a report is
not a contract, and it does not transfer anything to you or to us beyond what the
licence already says.

Please report only against your own installation and your own accounts. Do not test
against anyone else's machine, keys or vendor account.

## What this project treats as a vulnerability

- Anything that sends audio, transcript text or key material anywhere other than the
  two documented destinations (Deepgram, and the cleanup provider you configured).
- A path that writes anything to disk while logging is switched off, or that writes
  transcript content when `VEXFLOW_DEBUG_TRANSCRIPT` is unset. That variable is the
  only sanctioned way for dictated text to reach the log, it is read once at startup,
  and the Settings window says so in red while it is in force.
- A way for text inside a transcript to make the cleanup model act on it as an
  instruction rather than correcting it as data.
- A way to read a key out of the process, the logs, or the clipboard-restore path.
- Anything that leaves the clipboard holding a transcript, or overwrites content a
  password manager marked concealed.

## What it does not

- **Your keys are yours to look after, at your own risk.** They live in the login
  Keychain and the process reads them at startup, which means anything running as your
  user can reach them — inherent to a client that acts on your behalf, and not
  something any application can promise around. No undertaking is given that a key
  entered here cannot be read, copied, leaked or misused, and no liability is accepted
  for what follows if it is, including charges on your account. Decide whether that is
  acceptable before you paste a key, and rotate anything you have doubts about.
- **`security add-generic-password -w` exposes the secret to `ps` for the duration of
  the call.** This is the documented recipe from Apple's own tooling and applies when
  you save a key. If your threat model includes other local users watching your process
  table, put the key in the Keychain by hand through Keychain Access instead.
- **Nothing is code-signed or notarized.** Neither the installer package nor the app
  carries an Apple Developer signature, which is why macOS blocks the first open of the
  package and makes you clear it by hand. The trust boundary is the repository you got
  it from — check the source in `Vexflow.app/Contents/Resources/app`, which is the same
  source that runs.
- **The installer's postinstall script runs as root.** It is 40 lines of shell in
  `packaging/postinstall`; read it before installing if that matters to you. It drops
  to your user for everything it creates, and touches only `/Applications/Vexflow.app`,
  your LaunchAgents folder, and `~/Library/Application Support/Vexflow`.
- **macOS attributes permissions to "Python", not "Vexflow".** The bundle execs the
  interpreter, so the Microphone and Accessibility grants land on the interpreter.
  Anything else you run in the same virtualenv inherits that reach.
- **What the external services do is between you and them.** Vexflow carries your audio
  to the speech-to-text service you configured and your text to the cleanup service you
  configured, if any. Their security, retention and handling of that data are governed
  by your agreement with them, not by this project. Nothing here is a representation
  about a third party's service, and their behaviour can change without anything
  changing here.
- **Whether you are allowed to record is not checked.** Consent, notice, confidentiality
  and data-protection duties belong to the person holding the microphone. The software
  has no idea who else is in the room.

## Design notes for reviewers

The outbound network surface is deliberately tiny. It is:

- [`deepgram_live.py`](deepgram_live.py) — one websocket to Deepgram.
- [`llm.py`](llm.py) — one HTTPS POST to the configured cleanup endpoint.
- [`billing.py`](billing.py) — two HTTPS GETs to Deepgram, only if you configured a
  separate `billing:read` key.
- [`macos.py`](macos.py) — `open_url`, which hands a URL to the system browser and is
  only ever called with a constant from [`config.py`](config.py).

There is nothing else. `grep -rn "urlopen\|connect(" *.py` is the complete audit.

The event tap in [`hotkeys.py`](hotkeys.py) is `kCGEventTapOptionListenOnly` and its
mask covers only `FlagsChanged` and `OtherMouseDown`. Keystrokes and mouse movement are
filtered by WindowServer and never reach this process — it cannot see what you type.
