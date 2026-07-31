"""German interface strings.

The key is the English source string, so an entry that is missing here falls back to
English rather than to a bare identifier. Adding or fixing a language: see README.md
in this directory.
"""
TABLE = {
    # --- menu bar ------------------------------------------------------------
    "Ready": "Bereit",
    "Recording…": "Aufnahme…",
    "Paused": "Pausiert",
    "Stop recording": "Aufnahme beenden",
    "Pause": "Pause",
    "Resume": "Fortsetzen",
    "Language": "Erkennungssprache",
    "LLM Cleanup": "LLM-Bereinigung",
    "Clean up transcripts": "Transkript bereinigen",
    "Setup Guide…": "Erste Schritte…",
    "Settings…": "Einstellungen…",
    "Open log": "Protokoll öffnen",
    "Vexflow on GitHub": "Vexflow auf GitHub",
    "Built by ": "Gebaut von ",
    "Quit Vexflow": "Beenden",
    "About ": "Über ",
    "Hide ": "Ausblenden ",
    "Quit ": "Beenden ",
    "Edit": "Bearbeiten",
    "Undo": "Widerrufen",
    "Redo": "Wiederholen",
    "Cut": "Ausschneiden",
    "Copy": "Kopieren",
    "Paste": "Einsetzen",
    "Select All": "Alles auswählen",
    "Hold ": "Halte ",
    "tap ": "tippe ",
    "middle mouse button": "mittlere Maustaste",

    # --- key states, menu bar ------------------------------------------------
    "No Deepgram key — open Settings":
        "Kein Deepgram-Schlüssel — Einstellungen öffnen",
    "Checking your Deepgram key…": "Deepgram-Schlüssel wird geprüft…",
    "Deepgram rejected your key — open Settings":
        "Deepgram hat den Schlüssel abgelehnt — Einstellungen öffnen",
    "Can't reach Deepgram — check your connection":
        "Deepgram nicht erreichbar — Verbindung prüfen",
    "Balance: {}": "Guthaben: {}",
    "Balance: {} — running low": "Guthaben: {} — geht zur Neige",
    "Balance: …": "Guthaben: …",
    "Balance: checking…": "Guthaben: wird geprüft…",
    "Balance key rejected — open Settings":
        "Guthaben-Schlüssel abgelehnt — Einstellungen öffnen",
    "Balance: can't reach Deepgram": "Guthaben: Deepgram nicht erreichbar",
    " — no key": " — kein Schlüssel",
    " — checking the key…": " — Schlüssel wird geprüft…",
    " — key rejected": " — Schlüssel abgelehnt",
    " — could not check the key": " — Schlüssel ließ sich nicht prüfen",

    # --- macOS permission dialog ---------------------------------------------
    # Shown by macOS itself, so it follows the system language, not the setting.
    "Vexflow sends your speech to Deepgram with your own API key so it can be "
    "typed as text.":
        "Vexflow sendet deine Sprache mit deinem eigenen API-Schlüssel an Deepgram, damit sie als Text zurückkommt.",

    # --- settings window: frame ----------------------------------------------
    "{} Settings": "{}-Einstellungen",
    "Interface language": "Sprache der Oberfläche",
    "Restart to apply": "Neu starten",
    "Applied after the restart in step 3.":
        "Gilt nach dem Neustart in Schritt 3.",
    "Keys": "Schlüssel",
    "Dictation": "Diktat",
    "Cleanup": "Bereinigung",
    "Permissions": "Zugriff",
    "Done": "Fertig",

    # --- settings: keys ------------------------------------------------------
    "Speech to text": "Spracherkennung",
    "Audio goes from this Mac straight to Deepgram using your own key. "
    "Fields marked * are required.":
        "Der Ton geht von diesem Mac direkt an Deepgram, mit deinem eigenen "
        "Schlüssel. Mit * markierte Felder sind erforderlich.",
    "Transcript cleanup": "Transkript bereinigen",
    "Optional. A small model fixes punctuation, false starts and mangled "
    "names. Without a key you still get the raw transcript.":
        "Optional. Ein kleines Modell korrigiert Zeichensetzung, Versprecher und "
        "verhunzte Namen. Ohne Schlüssel bleibt das rohe Transkript.",
    "Deepgram key": "Deepgram-Schlüssel",
    "Balance key": "Guthaben-Schlüssel",
    "Anthropic key": "Anthropic-Schlüssel",
    "OpenAI key": "OpenAI-Schlüssel",
    "Save": "Sichern",
    "Get key": "Holen",
    "paste key": "Schlüssel einsetzen",
    "paste a new key to replace": "neuen Schlüssel einsetzen zum Ersetzen",
    "{} characters — press Save": "{} Zeichen — auf Sichern klicken",

    # --- settings: key statuses ----------------------------------------------
    "Not set": "Nicht gesetzt",
    "Saved in Keychain": "Im Schlüsselbund gesichert",
    "Required — dictation does not work without it":
        "Erforderlich — ohne ihn kein Diktat",
    "Checking with Deepgram…": "Wird bei Deepgram geprüft…",
    "Verified — Deepgram accepted this key":
        "Geprüft — Deepgram hat den Schlüssel angenommen",
    "Deepgram rejected this key. Check you copied all of it.":
        "Deepgram hat den Schlüssel abgelehnt. Prüfe, ob du ihn vollständig "
        "kopiert hast.",
    "Saved, but Deepgram could not be reached to check it":
        "Gesichert, aber Deepgram war zum Prüfen nicht erreichbar",
    "Deepgram rejected this key, or it has no billing:read scope":
        "Deepgram hat den Schlüssel abgelehnt, oder ihm fehlt billing:read",
    "Checking with {}…": "Wird bei {} geprüft…",
    "Verified — {} accepted this key": "Geprüft — {} hat den Schlüssel angenommen",
    "{} rejected this key": "{} hat den Schlüssel abgelehnt",
    "{} rejected this key: {}": "{} hat den Schlüssel abgelehnt: {}",
    "Saved, but {} could not be reached to check it":
        "Gesichert, aber {} war zum Prüfen nicht erreichbar",

    # --- settings: help popovers ---------------------------------------------
    "Open the console": "Konsole öffnen",
    "The one key Vexflow cannot work without. Your microphone audio goes from this "
    "Mac to the speech-to-text service under this key and comes back as text, with "
    "no server of ours in between. Create a key in your own account there and paste "
    "the whole string. It is kept in your login Keychain, never in a file — and, "
    "like any credential on any machine, it is yours to look after.":
        "Der eine Schlüssel, ohne den Vexflow nicht läuft. Der Ton deines Mikrofons "
        "geht von diesem Mac unter diesem Schlüssel an den Spracherkennungsdienst und "
        "kommt als Text zurück, ohne einen Server von uns dazwischen. Lege in deinem "
        "eigenen Konto dort einen Schlüssel an und setze die ganze Zeichenfolge ein. "
        "Er liegt in deinem Anmeldeschlüsselbund, nie in einer Datei — und bleibt, "
        "wie jede Zugangsdatei auf jeder Maschine, deine Sache.",
    "Optional, and a second key on purpose. Reading your account balance needs the "
    "billing:read scope, which the key above has no business holding — one key that "
    "spends and one that reads are worth keeping apart. Create a key with "
    "billing:read only and the menu bar shows the balance the service reports.":
        "Optional, und mit Absicht ein zweiter Schlüssel. Das Guthaben zu lesen "
        "verlangt den Bereich billing:read, den der Schlüssel oben nichts zu suchen "
        "hat: Ein Schlüssel, der ausgibt, und einer, der die Rechnung liest, gehören "
        "getrennt. Lege einen Schlüssel nur mit billing:read an, dann zeigt die "
        "Menüleiste das Guthaben, das der Dienst meldet.",
    "Optional. Drives the cleanup pass that repairs punctuation, false starts and "
    "mangled names. Only the transcript is sent, never the audio, and what the "
    "service does with it is between you and them. The key is checked the moment "
    "you save it, so a wrong one says so here instead of quietly doing nothing.":
        "Optional. Treibt den Bereinigungsdurchgang an, der Zeichensetzung, "
        "Versprecher und verhunzte Namen repariert. Gesendet wird nur das Transkript, "
        "nie der Ton, und was der Dienst damit macht, ist eine Sache zwischen dir und "
        "ihm. Der Schlüssel wird beim Sichern geprüft, ein falscher sagt es also "
        "gleich hier, statt still nichts zu tun.",
    "Optional, and an alternative to the key above rather than an addition — "
    "cleanup uses whichever provider is selected on the Cleanup tab. That tab can "
    "also point this key at any OpenAI-compatible endpoint, including a model "
    "running on your own machine.":
        "Optional, und eher eine Alternative zum Schlüssel oben als eine Ergänzung: "
        "Die Bereinigung nimmt den Anbieter, der im Tab „Bereinigung“ ausgewählt ist. "
        "Dort lässt sich dieser Schlüssel auch auf jede OpenAI-kompatible Adresse "
        "richten, samt einem Modell auf deiner eigenen Maschine.",

    # --- settings: dictation -------------------------------------------------
    "Recognition language": "Erkennungssprache",
    "A single language recognises better than Multilingual. Choose "
    "Multilingual only if you switch languages inside one sentence.":
        "Eine einzelne Sprache wird besser erkannt als der mehrsprachige Modus. Nimm "
        "mehrsprachig nur, wenn du mitten im Satz die Sprache wechselst.",
    "Push to talk": "Halten zum Sprechen",
    "Hold, speak, release.": "Halten, sprechen, loslassen.",
    "Hands-free toggle": "Umschalter",
    "Off": "Aus",
    "Tap once to start, tap again to stop.":
        "Einmal tippen startet, noch einmal tippen beendet.",
    "Combined entries fire only while both keys are held — safer when the "
    "free single keys are ones you type with.":
        "Kombinationen greifen nur, solange beide Tasten gehalten werden. Das hilft, "
        "wenn die freien Einzeltasten genau die sind, mit denen du schreibst.",
    "Also toggle with the middle mouse button":
        "Auch mit der mittleren Maustaste umschalten",
    "Play a sound when recording starts and stops":
        "Ton am Anfang und am Ende der Aufnahme",
    "Paste automatically (off: copy to clipboard only)":
        "Automatisch einsetzen (aus: nur in die Zwischenablage)",

    # --- settings: cleanup ---------------------------------------------------
    "Clean up transcripts with an LLM": "Transkript mit einem LLM bereinigen",
    "Provider": "Anbieter",
    "Model": "Modell",
    "No {} key yet — add one on the Keys tab.":
        "Noch kein {}-Schlüssel — im Tab „Schlüssel“ hinzufügen.",
    "{} rejected the key — check it on the Keys tab.":
        "{} hat den Schlüssel abgelehnt — im Tab „Schlüssel“ prüfen.",
    "Your vocabulary": "Eigenes Vokabular",
    "Edit vocabulary…": "Vokabular öffnen…",
    "Names and jargon the recogniser keeps getting wrong. One per line, "
    "kept on this Mac.":
        "Namen und Fachwörter, die die Erkennung immer wieder verfehlt. Eines pro "
        "Zeile, die Datei bleibt auf diesem Mac.",
    "Advanced": "Für Fortgeschrittene",
    "Endpoint": "Adresse",
    "Leave as-is for the vendor's own API, or point it at any "
    "OpenAI-compatible endpoint.":
        "So lassen für die eigene API des Anbieters, oder auf eine beliebige "
        "OpenAI-kompatible Adresse richten.",

    # --- settings: permissions -----------------------------------------------
    "macOS asks for these once. Vexflow cannot record or type without them.":
        "macOS fragt einmal danach. Ohne sie kann Vexflow weder aufnehmen noch "
        "schreiben.",
    "Microphone": "Mikrofon",
    "Lets Vexflow hear you.": "Damit Vexflow dich hört.",
    "Accessibility": "Bedienungshilfen",
    "Lets Vexflow see the hotkey and paste into the app you are using. "
    "Granting it takes effect only after Vexflow restarts.":
        "Damit Vexflow den Kurzbefehl sieht und in die App einsetzt, die du gerade "
        "benutzt. Erteilt wirkt der Zugriff erst nach einem Neustart von Vexflow.",
    "Granted": "Erteilt",
    "Not granted": "Nicht erteilt",
    "Not requested yet": "Noch nicht angefragt",
    "Asked on first use": "Wird bei der ersten Nutzung gefragt",
    "Open Settings": "Einstellungen öffnen",
    "Re-check": "Erneut prüfen",
    "Restart Vexflow": "Vexflow neu starten",
    "Keep a diagnostic log": "Diagnoseprotokoll führen",
    "Off, so nothing about your dictation reaches the disk. Turn it on to "
    "chase a problem and off again afterwards — switching it off deletes the "
    "file. It records timings and errors, never what you said.":
        "Aus, damit nichts über dein Diktat auf die Festplatte gelangt. Schalte es "
        "ein, um einem Problem nachzugehen, und danach wieder aus — beim Ausschalten "
        "wird die Datei gelöscht. Festgehalten werden Zeiten und Fehler, nie das "
        "Gesagte.",
    "Transcript debug logging is ON for this run — dictated text is being "
    "written to the log. Restart without VEXFLOW_DEBUG_TRANSCRIPT to stop it.":
        "Für diesen Lauf ist das Debug-Protokoll der Transkripte AN — diktierter Text "
        "wird ins Protokoll geschrieben. Zum Beenden ohne VEXFLOW_DEBUG_TRANSCRIPT "
        "neu starten.",
    "VEXFLOW_DEBUG_TRANSCRIPT is set for this run: switching the log on would "
    "write what you dictate into it.":
        "Für diesen Lauf ist VEXFLOW_DEBUG_TRANSCRIPT gesetzt: Das Protokoll "
        "einzuschalten würde dein Diktat hineinschreiben.",
    "Remove Vexflow from this Mac…": "Vexflow von diesem Mac entfernen…",

    # --- uninstall dialogs ---------------------------------------------------
    "Remove Vexflow from this Mac?": "Vexflow von diesem Mac entfernen?",
    "This quits Vexflow, removes it from your login items and deletes the "
    "app. Your API keys and settings are kept unless you choose otherwise.":
        "Vexflow wird beendet, aus den Anmeldeobjekten genommen und die App gelöscht. "
        "Deine Schlüssel und Einstellungen bleiben, sofern du nichts anderes wählst.",
    "Remove": "Entfernen",
    "Cancel": "Abbrechen",
    "Remove and Delete My Keys": "Samt Schlüsseln entfernen",
    "Vexflow has been removed.": "Vexflow wurde entfernt.",
    "Login item removed, but deleting the app was cancelled.":
        "Aus den Anmeldeobjekten genommen, aber das Löschen der App wurde abgebrochen.",
    "Login item removed, but the app could not be deleted.":
        "Aus den Anmeldeobjekten genommen, aber die App ließ sich nicht löschen.",
    "Login item removed; deleting the app failed: ":
        "Aus den Anmeldeobjekten genommen; das Löschen der App schlug fehl: ",
    "Microphone and Accessibility entries stay in System Settings until "
    "you remove them by hand.":
        "Die Einträge unter „Mikrofon“ und „Bedienungshilfen“ bleiben in den "
        "Systemeinstellungen, bis du sie von Hand entfernst.",

    # --- setup guide ---------------------------------------------------------
    "Welcome to ": "Willkommen bei ",
    "Set up ": "Einrichten: ",
    "macOS needs to grant two permissions before dictation can work. "
    "This takes about a minute.":
        "macOS muss zwei Zugriffsrechte erteilen, bevor das Diktat läuft. Das dauert "
        "etwa eine Minute.",
    "Allow microphone access": "Zugriff aufs Mikrofon erlauben",
    "So Vexflow can hear you.": "Damit Vexflow dich hört.",
    "Allow accessibility access": "Bedienungshilfen erlauben",
    "So Vexflow can see the hotkey and paste the text.":
        "Damit Vexflow den Kurzbefehl sieht und den Text einsetzt.",
    "macOS applies the accessibility grant only at launch.":
        "macOS übernimmt diesen Zugriff erst beim Start.",
    "Allow": "Erlauben",
    "Restart": "Neu starten",
    "Step {} of {}": "Schritt {} von {}",
    "Permissions are set.": "Zugriffsrechte sind erteilt.",
    "Denied — turn it on in System Settings":
        "Verweigert — in den Systemeinstellungen einschalten",
    "Requested on first use": "Wird bei der ersten Nutzung gefragt",
    "Hotkeys are live": "Kurzbefehle laufen",
    "Restart to activate the hotkey": "Neu starten, damit der Kurzbefehl greift",
    "Finish step 2 first": "Erst Schritt 2 abschließen",
    "Close": "Schließen",
    "Add your API key": "Schlüssel hinzufügen",

    # --- engine notices in the menu ------------------------------------------
    "Restarted after a dead microphone — please dictate again":
        "Nach totem Mikrofon neu gestartet — bitte noch einmal diktieren",
    "No Accessibility permission — hotkeys are dead":
        "Kein Zugriff auf Bedienungshilfen — Kurzbefehle tot",
    "Microphone still dead after a restart — check System Settings > Sound":
        "Mikrofon auch nach Neustart tot — Systemeinstellungen > Ton prüfen",
    "Microphone is dead — restart Vexflow manually":
        "Mikrofon tot — Vexflow von Hand neu starten",
    "Microphone did not open — check input and permissions":
        "Mikrofon ließ sich nicht öffnen — Eingang und Zugriff prüfen",
    "Microphone is dead — restarting": "Mikrofon tot — Neustart läuft",
    "Microphone rebuilt mid-recording — the start may be lost":
        "Mikrofon mitten in der Aufnahme neu aufgebaut — der Anfang fehlt womöglich",
    "Deepgram connection dropped — text lost":
        "Verbindung zu Deepgram abgerissen — Text verloren",
    "Deepgram unreachable — check your connection":
        "Deepgram nicht erreichbar — Verbindung prüfen",
    "Copied — press Cmd-V to paste": "Kopiert — mit Cmd-V einsetzen",
    "duration limit": "Längenbegrenzung",
    "Deepgram connection dropped": "Verbindung zu Deepgram abgerissen",
    "Stopped ({}) — text is on the clipboard, press Cmd-V":
        "Gestoppt ({}) — der Text liegt in der Zwischenablage, Cmd-V drücken",

    # --- about panel ---------------------------------------------------------
    "Provided as is, without warranty of any kind, and used entirely at your own "
    "risk.\n\n"
    "{app} is a client for external services that you choose, hold accounts with and "
    "pay directly. Those services are not operated by or answerable to {vendor}; "
    "their terms, prices and handling of your data are a matter between you and them, "
    "and nothing here is said on their behalf. Charges incurred through your keys are "
    "yours, and no undertaking is given about the safety of any key you enter.\n\n"
    "Other names belong to their owners and appear only to identify what this "
    "connects to. No affiliation or endorsement is claimed.":
        "Bereitgestellt wie besehen, ohne Gewährleistung jeder Art, und vollständig "
        "auf dein eigenes Risiko genutzt.\n\n"
        "{app} ist ein Client für externe Dienste, die du selbst wählst, bei denen du "
        "Konten hast und die du direkt bezahlst. Diese Dienste werden nicht von "
        "{vendor} betrieben und sind ihr nicht rechenschaftspflichtig: Ihre "
        "Bedingungen, ihre Preise und der Umgang mit deinen Daten sind eine Sache "
        "zwischen dir und ihnen, und hier wird nichts in ihrem Namen gesagt. Was über "
        "deine Schlüssel anfällt, gehört dir, und für die Sicherheit eines von dir "
        "eingegebenen Schlüssels wird nicht eingestanden.\n\n"
        "Andere Namen gehören ihren Eigentümern und stehen hier nur, um zu benennen, "
        "womit dies sich verbindet. Eine Verbindung oder Billigung wird nicht "
        "behauptet.",

    # --- languages -----------------------------------------------------------
    "English": "Englisch",
    "Multilingual (code-switching)": "Mehrsprachig (Wechsel im Satz)",
    "Spanish": "Spanisch",
    "German": "Deutsch",
    "French": "Französisch",
    "Portuguese": "Portugiesisch",
    "Italian": "Italienisch",
    "Dutch": "Niederländisch",
    "Russian": "Russisch",
    "Ukrainian": "Ukrainisch",
    "Polish": "Polnisch",
    "Turkish": "Türkisch",
    "Hindi": "Hindi",
    "Japanese": "Japanisch",

    # --- hotkeys -------------------------------------------------------------
    # Command, Option, Control and Shift stay: they are what is printed on the keys.
    "Right Command": "Command rechts",
    "Right Option": "Option rechts",
    "Left Command": "Command links",
    "Left Option": "Option links",
    "Left Control": "Control links",
    "Right Control": "Control rechts",
    "Left Shift": "Shift links",
    "Right Shift": "Shift rechts",
    "Control + Option": "Control + Option",
    "Control + Shift": "Control + Shift",
    "Command + Option": "Command + Option",
    "Option + Shift": "Option + Shift",
    "Control + Option + Shift": "Control + Option + Shift",

    # --- cleanup models ------------------------------------------------------
    # Model names are proper nouns; only what they are good for is translated.
    "Haiku 4.5 — fastest, cheapest": "Haiku 4.5 — am schnellsten, am günstigsten",
    "Sonnet 5 — balanced": "Sonnet 5 — ausgewogen",
    "Opus 5 — most accurate": "Opus 5 — am genauesten",
    "GPT-5.6 Luna — fastest, cheapest": "GPT-5.6 Luna — am schnellsten, am günstigsten",
    "GPT-5.6 Terra — balanced": "GPT-5.6 Terra — ausgewogen",
    "GPT-5.6 Sol — most accurate": "GPT-5.6 Sol — am genauesten",
}
