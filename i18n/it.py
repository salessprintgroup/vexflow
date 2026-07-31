"""Italian interface strings.

The key is the English source string, so an entry that is missing here falls back to
English rather than to a bare identifier. Adding or fixing a language: see README.md
in this directory.
"""
TABLE = {
    # --- menu bar ------------------------------------------------------------
    "Ready": "Pronto",
    "Recording…": "Registrazione…",
    "Paused": "In pausa",
    "Stop recording": "Ferma la registrazione",
    "Pause": "Pausa",
    "Resume": "Riprendi",
    "Language": "Lingua di riconoscimento",
    "LLM Cleanup": "Pulizia LLM",
    "Clean up transcripts": "Pulisci la trascrizione",
    "Setup Guide…": "Primi passi…",
    "Settings…": "Impostazioni…",
    "Open log": "Apri il registro",
    "Vexflow on GitHub": "Vexflow su GitHub",
    "Built by ": "Realizzato da ",
    "Quit Vexflow": "Esci",
    "About ": "Info su ",
    "Hide ": "Nascondi ",
    "Quit ": "Esci da ",
    "Edit": "Modifica",
    "Undo": "Annulla",
    "Redo": "Ripristina",
    "Cut": "Taglia",
    "Copy": "Copia",
    "Paste": "Incolla",
    "Select All": "Seleziona tutto",
    "Hold ": "Tieni premuto ",
    "tap ": "premi ",
    "middle mouse button": "tasto centrale del mouse",

    # --- key states, menu bar ------------------------------------------------
    "No Deepgram key — open Settings": "Nessuna chiave Deepgram — apri le impostazioni",
    "Checking your Deepgram key…": "Verifica della chiave Deepgram…",
    "Deepgram rejected your key — open Settings":
        "Deepgram ha rifiutato la chiave — apri le impostazioni",
    "Can't reach Deepgram — check your connection":
        "Deepgram irraggiungibile — controlla la connessione",
    "Balance: {}": "Saldo: {}",
    "Balance: {} — running low": "Saldo: {} — sta finendo",
    "Balance: …": "Saldo: …",
    "Balance: checking…": "Saldo: verifica…",
    "Balance key rejected — open Settings":
        "Chiave del saldo rifiutata — apri le impostazioni",
    "Balance: can't reach Deepgram": "Saldo: Deepgram irraggiungibile",
    " — no key": " — nessuna chiave",
    " — checking the key…": " — verifica della chiave…",
    " — key rejected": " — chiave rifiutata",
    " — could not check the key": " — impossibile verificare la chiave",

    # --- macOS permission dialog ---------------------------------------------
    # Shown by macOS itself, so it follows the system language, not the setting.
    "Vexflow sends your speech to Deepgram with your own API key so it can be "
    "typed as text.":
        "Vexflow invia la tua voce a Deepgram con la tua chiave API per restituirla come testo.",

    # --- settings window: frame ----------------------------------------------
    "{} Settings": "Impostazioni di {}",
    "Interface language": "Lingua dell'interfaccia",
    "Keys": "Chiavi",
    "Dictation": "Dettatura",
    "Cleanup": "Pulizia",
    "Permissions": "Permessi",
    "Done": "OK",

    # --- settings: keys ------------------------------------------------------
    "Speech to text": "Riconoscimento vocale",
    "Audio goes from this Mac straight to Deepgram using your own key. "
    "Fields marked * are required.":
        "L'audio parte da questo Mac dritto verso Deepgram con la tua chiave. "
        "I campi con * sono obbligatori.",
    "Transcript cleanup": "Pulizia della trascrizione",
    "Optional. A small model fixes punctuation, false starts and mangled "
    "names. Without a key you still get the raw transcript.":
        "Facoltativo. Un modello piccolo sistema la punteggiatura, le partenze false "
        "e i nomi storpiati. Senza chiave ti resta comunque la trascrizione grezza.",
    "Deepgram key": "Chiave Deepgram",
    "Balance key": "Chiave del saldo",
    "Anthropic key": "Chiave Anthropic",
    "OpenAI key": "Chiave OpenAI",
    "Save": "Salva",
    "Get key": "Ottieni",
    "paste key": "incolla la chiave",
    "paste a new key to replace": "incolla una nuova chiave per sostituirla",
    "{} characters — press Save": "{} caratteri — premi Salva",

    # --- settings: key statuses ----------------------------------------------
    "Not set": "Non impostata",
    "Saved in Keychain": "Salvata nel portachiavi",
    "Required — dictation does not work without it":
        "Obbligatoria — senza di lei niente dettatura",
    "Checking with Deepgram…": "Verifica presso Deepgram…",
    "Verified — Deepgram accepted this key":
        "Verificata — Deepgram ha accettato questa chiave",
    "Deepgram rejected this key. Check you copied all of it.":
        "Deepgram ha rifiutato questa chiave. Controlla di averla copiata tutta.",
    "Saved, but Deepgram could not be reached to check it":
        "Salvata, ma Deepgram non era raggiungibile per verificarla",
    "Deepgram rejected this key, or it has no billing:read scope":
        "Deepgram ha rifiutato questa chiave, oppure non ha l'ambito billing:read",
    "Checking with {}…": "Verifica presso {}…",
    "Verified — {} accepted this key": "Verificata — {} ha accettato questa chiave",
    "{} rejected this key": "{} ha rifiutato questa chiave",
    "{} rejected this key: {}": "{} ha rifiutato questa chiave: {}",
    "Saved, but {} could not be reached to check it":
        "Salvata, ma {} non era raggiungibile per verificarla",

    # --- settings: help popovers ---------------------------------------------
    "Open the console": "Apri la console",
    "The one key Vexflow cannot work without. Your microphone audio goes from this "
    "Mac to the speech-to-text service under this key and comes back as text, with "
    "no server of ours in between. Create a key in your own account there and paste "
    "the whole string. It is kept in your login Keychain, never in a file — and, "
    "like any credential on any machine, it is yours to look after.":
        "L'unica chiave senza la quale Vexflow non funziona. L'audio del microfono "
        "parte da questo Mac verso il servizio di riconoscimento con questa chiave e "
        "torna sotto forma di testo, senza nessun nostro server in mezzo. Crea una "
        "chiave nel tuo account là e incolla l'intera stringa. Sta nel portachiavi "
        "di accesso, mai in un file — e, come ogni credenziale su qualsiasi "
        "macchina, resta una tua responsabilità.",
    "Optional, and a second key on purpose. Reading your account balance needs the "
    "billing:read scope, which the key above has no business holding — one key that "
    "spends and one that reads are worth keeping apart. Create a key with "
    "billing:read only and the menu bar shows the balance the service reports.":
        "Facoltativa, ed è una seconda chiave di proposito. Leggere il saldo richiede "
        "l'ambito billing:read, che la chiave qui sopra non ha motivo di portarsi "
        "dietro: una chiave che spende e una che legge il conto è meglio tenerle "
        "separate. Crea una chiave con il solo billing:read e la barra dei menu "
        "mostrerà il saldo che il servizio comunica.",
    "Optional. Drives the cleanup pass that repairs punctuation, false starts and "
    "mangled names. Only the transcript is sent, never the audio, and what the "
    "service does with it is between you and them. The key is checked the moment "
    "you save it, so a wrong one says so here instead of quietly doing nothing.":
        "Facoltativa. Alimenta il passaggio di pulizia che ripara punteggiatura, "
        "partenze false e nomi storpiati. Viene inviata solo la trascrizione, mai "
        "l'audio, e quello che il servizio ne fa riguarda te e lui. La chiave viene "
        "verificata nel momento in cui la salvi, così una sbagliata lo dice qui "
        "invece di restare zitta senza fare nulla.",
    "Optional, and an alternative to the key above rather than an addition — "
    "cleanup uses whichever provider is selected on the Cleanup tab. That tab can "
    "also point this key at any OpenAI-compatible endpoint, including a model "
    "running on your own machine.":
        "Facoltativa, e più un'alternativa alla chiave qui sopra che un'aggiunta: la "
        "pulizia usa il fornitore selezionato nel pannello Pulizia. Lì stesso questa "
        "chiave può puntare a qualsiasi indirizzo compatibile con OpenAI, compreso "
        "un modello che gira sulla tua macchina.",

    # --- settings: dictation -------------------------------------------------
    "Recognition language": "Lingua di riconoscimento",
    "A single language recognises better than Multilingual. Choose "
    "Multilingual only if you switch languages inside one sentence.":
        "Una lingua sola viene riconosciuta meglio della modalità multilingue. "
        "Scegli multilingue solo se cambi lingua dentro la stessa frase.",
    "Push to talk": "Tieni premuto",
    "Hold, speak, release.": "Tieni premuto, parla, rilascia.",
    "Hands-free toggle": "Interruttore",
    "Off": "No",
    "Tap once to start, tap again to stop.":
        "Una pressione avvia, un'altra ferma.",
    "Combined entries fire only while both keys are held — safer when the "
    "free single keys are ones you type with.":
        "Le combinazioni scattano solo finché tieni premuti entrambi i tasti. Aiuta "
        "quando i tasti singoli rimasti liberi sono quelli con cui scrivi.",
    "Also toggle with the middle mouse button":
        "Commuta anche con il tasto centrale del mouse",
    "Play a sound when recording starts and stops":
        "Suono all'inizio e alla fine della registrazione",
    "Paste automatically (off: copy to clipboard only)":
        "Incolla in automatico (se no: solo copia)",

    # --- settings: cleanup ---------------------------------------------------
    "Clean up transcripts with an LLM": "Pulisci la trascrizione con un LLM",
    "Provider": "Fornitore",
    "Model": "Modello",
    "No {} key yet — add one on the Keys tab.":
        "Non c'è ancora una chiave {} — aggiungila nel pannello Chiavi.",
    "{} rejected the key — check it on the Keys tab.":
        "{} ha rifiutato la chiave — controllala nel pannello Chiavi.",
    "Your vocabulary": "Il tuo vocabolario",
    "Edit vocabulary…": "Apri il vocabolario…",
    "Names and jargon the recogniser keeps getting wrong. One per line, "
    "kept on this Mac.":
        "Nomi e gergo che il riconoscimento sbaglia di continuo. Uno per riga, il "
        "file resta su questo Mac.",
    "Advanced": "Avanzate",
    "Endpoint": "Indirizzo",
    "Leave as-is for the vendor's own API, or point it at any "
    "OpenAI-compatible endpoint.":
        "Lascialo com'è per l'API del fornitore, oppure puntalo a un qualsiasi "
        "indirizzo compatibile con OpenAI.",

    # --- settings: permissions -----------------------------------------------
    "macOS asks for these once. Vexflow cannot record or type without them.":
        "macOS li chiede una volta sola. Senza, Vexflow non registra e non scrive.",
    "Microphone": "Microfono",
    "Lets Vexflow hear you.": "Perché Vexflow ti senta.",
    "Accessibility": "Accessibilità",
    "Lets Vexflow see the hotkey and paste into the app you are using. "
    "Granting it takes effect only after Vexflow restarts.":
        "Perché Vexflow veda la scorciatoia e incolli nell'app che stai usando. Una "
        "volta concesso, ha effetto solo dopo il riavvio di Vexflow.",
    "Granted": "Concesso",
    "Not granted": "Non concesso",
    "Not requested yet": "Non ancora richiesto",
    "Asked on first use": "Chiesto al primo utilizzo",
    "Open Settings": "Apri le impostazioni",
    "Re-check": "Ricontrolla",
    "Restart Vexflow": "Riavvia Vexflow",
    "Keep a diagnostic log": "Tieni un registro di diagnostica",
    "Off, so nothing about your dictation reaches the disk. Turn it on to "
    "chase a problem and off again afterwards — switching it off deletes the "
    "file. It records timings and errors, never what you said.":
        "Spento, così della tua dettatura non arriva niente sul disco. Accendilo per "
        "inseguire un problema e rispegnilo dopo: spegnerlo cancella il file. "
        "Registra tempi ed errori, mai quello che hai detto.",
    "Transcript debug logging is ON for this run — dictated text is being "
    "written to the log. Restart without VEXFLOW_DEBUG_TRANSCRIPT to stop it.":
        "In questa esecuzione il registro di debug delle trascrizioni è ATTIVO: il "
        "testo dettato viene scritto nel registro. Riavvia senza "
        "VEXFLOW_DEBUG_TRANSCRIPT per fermarlo.",
    "VEXFLOW_DEBUG_TRANSCRIPT is set for this run: switching the log on would "
    "write what you dictate into it.":
        "In questa esecuzione VEXFLOW_DEBUG_TRANSCRIPT è impostato: accendere il "
        "registro ci scriverebbe dentro quello che detti.",
    "Remove Vexflow from this Mac…": "Rimuovi Vexflow da questo Mac…",

    # --- uninstall dialogs ---------------------------------------------------
    "Remove Vexflow from this Mac?": "Rimuovere Vexflow da questo Mac?",
    "This quits Vexflow, removes it from your login items and deletes the "
    "app. Your API keys and settings are kept unless you choose otherwise.":
        "Vexflow si chiude, esce dagli elementi di login e l'app viene eliminata. Le "
        "tue chiavi e le impostazioni restano, a meno che tu non scelga altrimenti.",
    "Remove": "Rimuovi",
    "Cancel": "Annulla",
    "Remove and Delete My Keys": "Rimuovi insieme alle chiavi",
    "Vexflow has been removed.": "Vexflow è stato rimosso.",
    "Login item removed, but deleting the app was cancelled.":
        "Tolto dagli elementi di login, ma l'eliminazione dell'app è stata annullata.",
    "Login item removed, but the app could not be deleted.":
        "Tolto dagli elementi di login, ma l'app non è stata eliminata.",
    "Login item removed; deleting the app failed: ":
        "Tolto dagli elementi di login; l'eliminazione dell'app è fallita: ",
    "Microphone and Accessibility entries stay in System Settings until "
    "you remove them by hand.":
        "Le voci Microfono e Accessibilità restano in Impostazioni di Sistema finché "
        "non le togli a mano.",

    # --- setup guide ---------------------------------------------------------
    "Welcome to ": "Benvenuto in ",
    "Set up ": "Configura ",
    "macOS needs to grant two permissions before dictation can work. "
    "This takes about a minute.":
        "macOS deve concedere due permessi prima che la dettatura funzioni. Ci vuole "
        "circa un minuto.",
    "Allow microphone access": "Consenti l'accesso al microfono",
    "So Vexflow can hear you.": "Perché Vexflow ti senta.",
    "Allow accessibility access": "Consenti l'accesso di accessibilità",
    "So Vexflow can see the hotkey and paste the text.":
        "Perché Vexflow veda la scorciatoia e incolli il testo.",
    "macOS applies the accessibility grant only at launch.":
        "macOS applica quel permesso solo all'avvio.",
    "Allow": "Consenti",
    "Restart": "Riavvia",
    "Step {} of {}": "Passo {} di {}",
    "Permissions are set.": "Permessi concessi.",
    "Denied — turn it on in System Settings":
        "Negato — attivalo in Impostazioni di Sistema",
    "Requested on first use": "Chiesto al primo utilizzo",
    "Hotkeys are live": "Le scorciatoie funzionano",
    "Restart to activate the hotkey": "Riavvia per attivare la scorciatoia",
    "Finish step 2 first": "Finisci prima il passo 2",
    "Close": "Chiudi",
    "Add your API key": "Aggiungi la chiave",

    # --- engine notices in the menu ------------------------------------------
    "Restarted after a dead microphone — please dictate again":
        "Riavviato dopo un microfono morto — detta di nuovo",
    "No Accessibility permission — hotkeys are dead":
        "Nessun permesso di accessibilità — scorciatoie morte",
    "Microphone still dead after a restart — check System Settings > Sound":
        "Microfono ancora morto dopo il riavvio — vedi Impostazioni di Sistema > Suono",
    "Microphone is dead — restart Vexflow manually":
        "Microfono morto — riavvia Vexflow a mano",
    "Microphone did not open — check input and permissions":
        "Il microfono non si è aperto — controlla ingresso e permessi",
    "Microphone is dead — restarting": "Microfono morto — riavvio in corso",
    "Microphone rebuilt mid-recording — the start may be lost":
        "Microfono ricostruito a metà registrazione — l'inizio potrebbe mancare",
    "Deepgram connection dropped — text lost":
        "Connessione a Deepgram caduta — testo perso",
    "Deepgram unreachable — check your connection":
        "Deepgram irraggiungibile — controlla la connessione",
    "Copied — press Cmd-V to paste": "Copiato — incolla con Cmd-V",
    "duration limit": "limite di durata",
    "Deepgram connection dropped": "connessione a Deepgram caduta",
    "Stopped ({}) — text is on the clipboard, press Cmd-V":
        "Fermato ({}) — il testo è negli appunti, premi Cmd-V",

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
        "Fornito così com'è, senza garanzia di alcun tipo, e usato interamente a tuo "
        "rischio.\n\n"
        "{app} è un client per servizi esterni che scegli tu, presso cui hai account "
        "e che paghi direttamente. Quei servizi non sono gestiti da {vendor} né le "
        "rispondono: le loro condizioni, i loro prezzi e il trattamento dei tuoi dati "
        "riguardano te e loro, e qui non si dice nulla a nome loro. Quanto speso con "
        "le tue chiavi è tuo, e non viene assunto alcun impegno sulla sicurezza di "
        "nessuna chiave che inserisci.\n\n"
        "Gli altri nomi appartengono ai rispettivi proprietari e compaiono solo per "
        "indicare a cosa questo si collega. Non si rivendica alcuna affiliazione né "
        "alcun avallo.",

    # --- languages -----------------------------------------------------------
    "English": "Inglese",
    "Multilingual (code-switching)": "Multilingue (cambio al volo)",
    "Spanish": "Spagnolo",
    "German": "Tedesco",
    "French": "Francese",
    "Portuguese": "Portoghese",
    "Italian": "Italiano",
    "Dutch": "Neerlandese",
    "Russian": "Russo",
    "Ukrainian": "Ucraino",
    "Polish": "Polacco",
    "Turkish": "Turco",
    "Hindi": "Hindi",
    "Japanese": "Giapponese",

    # --- hotkeys -------------------------------------------------------------
    # Command, Option, Control and Shift stay: they are what is printed on the keys.
    "Right Command": "Command destro",
    "Right Option": "Option destro",
    "Left Command": "Command sinistro",
    "Left Option": "Option sinistro",
    "Left Control": "Control sinistro",
    "Right Control": "Control destro",
    "Left Shift": "Shift sinistro",
    "Right Shift": "Shift destro",
    "Control + Option": "Control + Option",
    "Control + Shift": "Control + Shift",
    "Command + Option": "Command + Option",
    "Option + Shift": "Option + Shift",
    "Control + Option + Shift": "Control + Option + Shift",

    # --- cleanup models ------------------------------------------------------
    # Model names are proper nouns; only what they are good for is translated.
    "Haiku 4.5 — fastest, cheapest": "Haiku 4.5 — la più rapida ed economica",
    "Sonnet 5 — balanced": "Sonnet 5 — equilibrata",
    "Opus 5 — most accurate": "Opus 5 — la più precisa",
    "GPT-5.6 Luna — fastest, cheapest": "GPT-5.6 Luna — la più rapida ed economica",
    "GPT-5.6 Terra — balanced": "GPT-5.6 Terra — equilibrata",
    "GPT-5.6 Sol — most accurate": "GPT-5.6 Sol — la più precisa",
}
