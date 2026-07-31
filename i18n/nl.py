"""Dutch interface strings.

The key is the English source string, so an entry that is missing here falls back to
English rather than to a bare identifier. Adding or fixing a language: see README.md
in this directory.
"""
TABLE = {
    # --- menu bar ------------------------------------------------------------
    "Ready": "Gereed",
    "Recording…": "Opnemen…",
    "Paused": "Gepauzeerd",
    "Stop recording": "Opname stoppen",
    "Pause": "Pauzeer",
    "Resume": "Hervat",
    "Language": "Herkenningstaal",
    "LLM Cleanup": "LLM-opschoning",
    "Clean up transcripts": "Transcript opschonen",
    "Setup Guide…": "Eerste stappen…",
    "Settings…": "Instellingen…",
    "Open log": "Log openen",
    "Vexflow on GitHub": "Vexflow op GitHub",
    "Built by ": "Gemaakt door ",
    "Quit Vexflow": "Stop",
    "About ": "Over ",
    "Hide ": "Verberg ",
    "Quit ": "Stop ",
    "Edit": "Wijzig",
    "Undo": "Herstel",
    "Redo": "Opnieuw",
    "Cut": "Knip",
    "Copy": "Kopieer",
    "Paste": "Plak",
    "Select All": "Selecteer alles",
    "Hold ": "Houd ",
    "tap ": "tik ",
    "middle mouse button": "middelste muisknop",

    # --- key states, menu bar ------------------------------------------------
    "No Deepgram key — open Settings":
        "Geen Deepgram-sleutel — open de instellingen",
    "Checking your Deepgram key…": "Je Deepgram-sleutel wordt gecontroleerd…",
    "Deepgram rejected your key — open Settings":
        "Deepgram weigerde de sleutel — open de instellingen",
    "Can't reach Deepgram — check your connection":
        "Deepgram onbereikbaar — controleer je verbinding",
    "Balance: {}": "Saldo: {}",
    "Balance: {} — running low": "Saldo: {} — raakt op",
    "Balance: …": "Saldo: …",
    "Balance: checking…": "Saldo: wordt gecontroleerd…",
    "Balance key rejected — open Settings":
        "Saldosleutel geweigerd — open de instellingen",
    "Balance: can't reach Deepgram": "Saldo: Deepgram onbereikbaar",
    " — no key": " — geen sleutel",
    " — checking the key…": " — sleutel wordt gecontroleerd…",
    " — key rejected": " — sleutel geweigerd",
    " — could not check the key": " — sleutel kon niet gecontroleerd worden",

    # --- macOS permission dialog ---------------------------------------------
    # Shown by macOS itself, so it follows the system language, not the setting.
    "Vexflow sends your speech to Deepgram with your own API key so it can be "
    "typed as text.":
        "Vexflow stuurt je spraak met je eigen API-sleutel naar Deepgram om die als tekst terug te krijgen.",

    # --- settings window: frame ----------------------------------------------
    "{} Settings": "{}-instellingen",
    "Interface language": "Taal van de interface",
    "Keys": "Sleutels",
    "Dictation": "Dicteren",
    "Cleanup": "Opschonen",
    "Permissions": "Toegang",
    "Done": "Gereed",

    # --- settings: keys ------------------------------------------------------
    "Speech to text": "Spraakherkenning",
    "Audio goes from this Mac straight to Deepgram using your own key. "
    "Fields marked * are required.":
        "Het geluid gaat van deze Mac rechtstreeks naar Deepgram met je eigen "
        "sleutel. Velden met * zijn verplicht.",
    "Transcript cleanup": "Transcript opschonen",
    "Optional. A small model fixes punctuation, false starts and mangled "
    "names. Without a key you still get the raw transcript.":
        "Optioneel. Een klein model herstelt leestekens, valse starts en verhaspelde "
        "namen. Zonder sleutel houd je het ruwe transcript.",
    "Deepgram key": "Deepgram-sleutel",
    "Balance key": "Saldosleutel",
    "Anthropic key": "Anthropic-sleutel",
    "OpenAI key": "OpenAI-sleutel",
    "Save": "Bewaar",
    "Get key": "Ophalen",
    "paste key": "plak de sleutel",
    "paste a new key to replace": "plak een nieuwe sleutel om te vervangen",
    "{} characters — press Save": "{} tekens — klik op Bewaar",

    # --- settings: key statuses ----------------------------------------------
    "Not set": "Niet ingesteld",
    "Saved in Keychain": "Bewaard in de sleutelhanger",
    "Required — dictation does not work without it":
        "Verplicht — zonder deze werkt dicteren niet",
    "Checking with Deepgram…": "Wordt bij Deepgram gecontroleerd…",
    "Verified — Deepgram accepted this key":
        "Gecontroleerd — Deepgram accepteerde deze sleutel",
    "Deepgram rejected this key. Check you copied all of it.":
        "Deepgram weigerde deze sleutel. Kijk na of je hem helemaal gekopieerd hebt.",
    "Saved, but Deepgram could not be reached to check it":
        "Bewaard, maar Deepgram was niet bereikbaar om te controleren",
    "Deepgram rejected this key, or it has no billing:read scope":
        "Deepgram weigerde deze sleutel, of hij mist het bereik billing:read",
    "Checking with {}…": "Wordt bij {} gecontroleerd…",
    "Verified — {} accepted this key": "Gecontroleerd — {} accepteerde deze sleutel",
    "{} rejected this key": "{} weigerde deze sleutel",
    "{} rejected this key: {}": "{} weigerde deze sleutel: {}",
    "Saved, but {} could not be reached to check it":
        "Bewaard, maar {} was niet bereikbaar om te controleren",

    # --- settings: help popovers ---------------------------------------------
    "Open the console": "Open de console",
    "The one key Vexflow cannot work without. Your microphone audio goes from this "
    "Mac to the speech-to-text service under this key and comes back as text, with "
    "no server of ours in between. Create a key in your own account there and paste "
    "the whole string. It is kept in your login Keychain, never in a file — and, "
    "like any credential on any machine, it is yours to look after.":
        "De ene sleutel zonder welke Vexflow niet werkt. Het geluid van je microfoon "
        "gaat van deze Mac onder deze sleutel naar de spraakherkenningsdienst en komt "
        "als tekst terug, zonder server van ons ertussen. Maak een sleutel aan in je "
        "eigen account daar en plak de hele tekenreeks. Hij zit in je "
        "inlogsleutelhanger, nooit in een bestand — en blijft, zoals elke "
        "toegangscode op elke machine, jouw verantwoordelijkheid.",
    "Optional, and a second key on purpose. Reading your account balance needs the "
    "billing:read scope, which the key above has no business holding — one key that "
    "spends and one that reads are worth keeping apart. Create a key with "
    "billing:read only and the menu bar shows the balance the service reports.":
        "Optioneel, en met opzet een tweede sleutel. Je saldo lezen vraagt het bereik "
        "billing:read, dat de sleutel hierboven niets te zoeken heeft: een sleutel "
        "die uitgeeft en een die de rekening leest kun je beter uit elkaar houden. "
        "Maak een sleutel met alleen billing:read en de menubalk toont het saldo dat "
        "de dienst meldt.",
    "Optional. Drives the cleanup pass that repairs punctuation, false starts and "
    "mangled names. Only the transcript is sent, never the audio, and what the "
    "service does with it is between you and them. The key is checked the moment "
    "you save it, so a wrong one says so here instead of quietly doing nothing.":
        "Optioneel. Voedt de opschoonronde die leestekens, valse starts en "
        "verhaspelde namen herstelt. Alleen het transcript gaat weg, nooit het "
        "geluid, en wat de dienst ermee doet is een zaak tussen jou en hen. De "
        "sleutel wordt gecontroleerd op het moment dat je hem bewaart, dus een "
        "verkeerde zegt dat hier meteen in plaats van stilletjes niets te doen.",
    "Optional, and an alternative to the key above rather than an addition — "
    "cleanup uses whichever provider is selected on the Cleanup tab. That tab can "
    "also point this key at any OpenAI-compatible endpoint, including a model "
    "running on your own machine.":
        "Optioneel, en eerder een alternatief voor de sleutel hierboven dan een "
        "aanvulling: het opschonen gebruikt de aanbieder die op het tabblad "
        "Opschonen is gekozen. Daar kun je deze sleutel ook op elk "
        "OpenAI-compatibel adres richten, inclusief een model dat op je eigen "
        "machine draait.",

    # --- settings: dictation -------------------------------------------------
    "Recognition language": "Herkenningstaal",
    "A single language recognises better than Multilingual. Choose "
    "Multilingual only if you switch languages inside one sentence.":
        "Eén enkele taal wordt beter herkend dan de meertalige stand. Kies meertalig "
        "alleen als je binnen één zin van taal wisselt.",
    "Push to talk": "Ingedrukt houden",
    "Hold, speak, release.": "Houd vast, spreek, laat los.",
    "Hands-free toggle": "Schakelaar",
    "Off": "Uit",
    "Tap once to start, tap again to stop.":
        "Eén tik start, nog een tik stopt.",
    "Combined entries fire only while both keys are held — safer when the "
    "free single keys are ones you type with.":
        "Combinaties werken alleen zolang je beide toetsen ingedrukt houdt. Dat "
        "helpt als de vrije losse toetsen juist die zijn waarmee je typt.",
    "Also toggle with the middle mouse button":
        "Ook schakelen met de middelste muisknop",
    "Play a sound when recording starts and stops":
        "Geluid bij het begin en het eind van de opname",
    "Paste automatically (off: copy to clipboard only)":
        "Automatisch plakken (uit: alleen kopiëren)",

    # --- settings: cleanup ---------------------------------------------------
    "Clean up transcripts with an LLM": "Transcript opschonen met een LLM",
    "Provider": "Aanbieder",
    "Model": "Model",
    "No {} key yet — add one on the Keys tab.":
        "Nog geen {}-sleutel — voeg er een toe op het tabblad Sleutels.",
    "{} rejected the key — check it on the Keys tab.":
        "{} weigerde de sleutel — controleer hem op het tabblad Sleutels.",
    "Your vocabulary": "Je eigen woordenlijst",
    "Edit vocabulary…": "Woordenlijst openen…",
    "Names and jargon the recogniser keeps getting wrong. One per line, "
    "kept on this Mac.":
        "Namen en jargon die de herkenning steeds misslaat. Eén per regel, het "
        "bestand blijft op deze Mac.",
    "Advanced": "Geavanceerd",
    "Endpoint": "Adres",
    "Leave as-is for the vendor's own API, or point it at any "
    "OpenAI-compatible endpoint.":
        "Laat staan voor de eigen API van de aanbieder, of richt hem op een "
        "willekeurig OpenAI-compatibel adres.",

    # --- settings: permissions -----------------------------------------------
    "macOS asks for these once. Vexflow cannot record or type without them.":
        "macOS vraagt hier één keer om. Zonder deze kan Vexflow niet opnemen en niet "
        "typen.",
    "Microphone": "Microfoon",
    "Lets Vexflow hear you.": "Zodat Vexflow je hoort.",
    "Accessibility": "Toegankelijkheid",
    "Lets Vexflow see the hotkey and paste into the app you are using. "
    "Granting it takes effect only after Vexflow restarts.":
        "Zodat Vexflow de sneltoets ziet en plakt in de app die je gebruikt. Eenmaal "
        "verleend werkt het pas nadat Vexflow opnieuw is gestart.",
    "Granted": "Verleend",
    "Not granted": "Niet verleend",
    "Not requested yet": "Nog niet gevraagd",
    "Asked on first use": "Wordt bij het eerste gebruik gevraagd",
    "Open Settings": "Open de instellingen",
    "Re-check": "Opnieuw controleren",
    "Restart Vexflow": "Vexflow herstarten",
    "Keep a diagnostic log": "Een diagnoselog bijhouden",
    "Off, so nothing about your dictation reaches the disk. Turn it on to "
    "chase a problem and off again afterwards — switching it off deletes the "
    "file. It records timings and errors, never what you said.":
        "Uit, zodat er niets over je dictaat op de schijf terechtkomt. Zet hem aan om "
        "een probleem na te jagen en daarna weer uit: uitzetten wist het bestand. Hij "
        "noteert tijden en fouten, nooit wat je zei.",
    "Transcript debug logging is ON for this run — dictated text is being "
    "written to the log. Restart without VEXFLOW_DEBUG_TRANSCRIPT to stop it.":
        "Voor deze sessie staat het debuglog van transcripten AAN — gedicteerde tekst "
        "wordt naar het log geschreven. Herstart zonder VEXFLOW_DEBUG_TRANSCRIPT om "
        "dat te stoppen.",
    "VEXFLOW_DEBUG_TRANSCRIPT is set for this run: switching the log on would "
    "write what you dictate into it.":
        "Voor deze sessie is VEXFLOW_DEBUG_TRANSCRIPT gezet: het log aanzetten zou "
        "schrijven wat je dicteert.",
    "Remove Vexflow from this Mac…": "Vexflow van deze Mac verwijderen…",

    # --- uninstall dialogs ---------------------------------------------------
    "Remove Vexflow from this Mac?": "Vexflow van deze Mac verwijderen?",
    "This quits Vexflow, removes it from your login items and deletes the "
    "app. Your API keys and settings are kept unless you choose otherwise.":
        "Vexflow stopt, verdwijnt uit je inlogonderdelen en de app wordt verwijderd. "
        "Je sleutels en instellingen blijven staan, tenzij je anders kiest.",
    "Remove": "Verwijder",
    "Cancel": "Annuleer",
    "Remove and Delete My Keys": "Verwijder met sleutels en al",
    "Vexflow has been removed.": "Vexflow is verwijderd.",
    "Login item removed, but deleting the app was cancelled.":
        "Uit de inlogonderdelen gehaald, maar het verwijderen van de app is "
        "geannuleerd.",
    "Login item removed, but the app could not be deleted.":
        "Uit de inlogonderdelen gehaald, maar de app kon niet verwijderd worden.",
    "Login item removed; deleting the app failed: ":
        "Uit de inlogonderdelen gehaald; het verwijderen van de app mislukte: ",
    "Microphone and Accessibility entries stay in System Settings until "
    "you remove them by hand.":
        "De vermeldingen bij Microfoon en Toegankelijkheid blijven in "
        "Systeeminstellingen staan tot je ze met de hand weghaalt.",

    # --- setup guide ---------------------------------------------------------
    "Welcome to ": "Welkom bij ",
    "Set up ": "Stel in: ",
    "macOS needs to grant two permissions before dictation can work. "
    "This takes about a minute.":
        "macOS moet twee soorten toegang verlenen voordat dicteren werkt. Dat kost "
        "ongeveer een minuut.",
    "Allow microphone access": "Geef toegang tot de microfoon",
    "So Vexflow can hear you.": "Zodat Vexflow je hoort.",
    "Allow accessibility access": "Geef toegang tot toegankelijkheid",
    "So Vexflow can see the hotkey and paste the text.":
        "Zodat Vexflow de sneltoets ziet en de tekst plakt.",
    "macOS applies the accessibility grant only at launch.":
        "macOS past die toegang pas bij het starten toe.",
    "Allow": "Toestaan",
    "Restart": "Herstart",
    "Step {} of {}": "Stap {} van {}",
    "Permissions are set.": "Toegang is geregeld.",
    "Denied — turn it on in System Settings":
        "Geweigerd — zet het aan in Systeeminstellingen",
    "Requested on first use": "Wordt bij het eerste gebruik gevraagd",
    "Hotkeys are live": "De sneltoetsen werken",
    "Restart to activate the hotkey": "Herstart om de sneltoets te activeren",
    "Finish step 2 first": "Maak eerst stap 2 af",
    "Close": "Sluit",
    "Add your API key": "Sleutel toevoegen",

    # --- engine notices in the menu ------------------------------------------
    "Restarted after a dead microphone — please dictate again":
        "Herstart na een dode microfoon — dicteer nog een keer",
    "No Accessibility permission — hotkeys are dead":
        "Geen toegang tot toegankelijkheid — sneltoetsen dood",
    "Microphone still dead after a restart — check System Settings > Sound":
        "Microfoon na de herstart nog dood — kijk in Systeeminstellingen > Geluid",
    "Microphone is dead — restart Vexflow manually":
        "Microfoon dood — herstart Vexflow met de hand",
    "Microphone did not open — check input and permissions":
        "De microfoon ging niet open — controleer ingang en toegang",
    "Microphone is dead — restarting": "Microfoon dood — bezig met herstarten",
    "Microphone rebuilt mid-recording — the start may be lost":
        "Microfoon halverwege de opname opnieuw opgebouwd — het begin kan weg zijn",
    "Deepgram connection dropped — text lost":
        "Verbinding met Deepgram weggevallen — tekst kwijt",
    "Deepgram unreachable — check your connection":
        "Deepgram onbereikbaar — controleer je verbinding",
    "Copied — press Cmd-V to paste": "Gekopieerd — plak met Cmd-V",
    "duration limit": "duurgrens",
    "Deepgram connection dropped": "verbinding met Deepgram weggevallen",
    "Stopped ({}) — text is on the clipboard, press Cmd-V":
        "Gestopt ({}) — de tekst staat op het klembord, druk Cmd-V",

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
        "Geleverd zoals het is, zonder enige garantie, en volledig op eigen risico "
        "gebruikt.\n\n"
        "{app} is een client voor externe diensten die je zelf kiest, waar je zelf "
        "een account hebt en die je rechtstreeks betaalt. Die diensten worden niet "
        "door {vendor} beheerd en leggen daar geen verantwoording aan af: hun "
        "voorwaarden, hun prijzen en de omgang met jouw gegevens zijn een zaak tussen "
        "jou en hen, en hier wordt niets namens hen gezegd. Wat er via jouw sleutels "
        "wordt uitgegeven is van jou, en er wordt geen toezegging gedaan over de "
        "veiligheid van welke sleutel je ook invoert.\n\n"
        "Andere namen behoren toe aan hun eigenaren en staan hier alleen om te "
        "benoemen waarmee dit verbinding maakt. Er wordt geen band of goedkeuring "
        "geclaimd.",

    # --- languages -----------------------------------------------------------
    "English": "Engels",
    "Multilingual (code-switching)": "Meertalig (wisselen tijdens het spreken)",
    "Spanish": "Spaans",
    "German": "Duits",
    "French": "Frans",
    "Portuguese": "Portugees",
    "Italian": "Italiaans",
    "Dutch": "Nederlands",
    "Russian": "Russisch",
    "Ukrainian": "Oekraïens",
    "Polish": "Pools",
    "Turkish": "Turks",
    "Hindi": "Hindi",
    "Japanese": "Japans",

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
    "Haiku 4.5 — fastest, cheapest": "Haiku 4.5 — snelst en goedkoopst",
    "Sonnet 5 — balanced": "Sonnet 5 — in balans",
    "Opus 5 — most accurate": "Opus 5 — nauwkeurigst",
    "GPT-5.6 Luna — fastest, cheapest": "GPT-5.6 Luna — snelst en goedkoopst",
    "GPT-5.6 Terra — balanced": "GPT-5.6 Terra — in balans",
    "GPT-5.6 Sol — most accurate": "GPT-5.6 Sol — nauwkeurigst",
}
