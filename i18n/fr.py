"""French interface strings.

The key is the English source string, so an entry that is missing here falls back to
English rather than to a bare identifier. Adding or fixing a language: see README.md
in this directory.
"""
TABLE = {
    # --- menu bar ------------------------------------------------------------
    "Ready": "Prêt",
    "Recording…": "Enregistrement…",
    "Paused": "En pause",
    "Stop recording": "Arrêter l'enregistrement",
    "Pause": "Pause",
    "Resume": "Reprendre",
    "Language": "Langue de reconnaissance",
    "LLM Cleanup": "Nettoyage LLM",
    "Clean up transcripts": "Nettoyer la transcription",
    "Setup Guide…": "Premiers pas…",
    "Settings…": "Réglages…",
    "Open log": "Ouvrir le journal",
    "Vexflow on GitHub": "Vexflow sur GitHub",
    "Built by ": "Réalisé par ",
    "Quit Vexflow": "Quitter",
    "About ": "À propos de ",
    "Hide ": "Masquer ",
    "Quit ": "Quitter ",
    "Edit": "Édition",
    "Undo": "Annuler",
    "Redo": "Rétablir",
    "Cut": "Couper",
    "Copy": "Copier",
    "Paste": "Coller",
    "Select All": "Tout sélectionner",
    "Hold ": "Maintenez ",
    "tap ": "appuyez sur ",
    "middle mouse button": "bouton central de la souris",

    # --- key states, menu bar ------------------------------------------------
    "No Deepgram key — open Settings": "Aucune clé Deepgram — ouvrez les réglages",
    "Checking your Deepgram key…": "Vérification de votre clé Deepgram…",
    "Deepgram rejected your key — open Settings":
        "Deepgram a refusé la clé — ouvrez les réglages",
    "Can't reach Deepgram — check your connection":
        "Deepgram injoignable — vérifiez la connexion",
    "Balance: {}": "Solde : {}",
    "Balance: {} — running low": "Solde : {} — bientôt épuisé",
    "Balance: …": "Solde : …",
    "Balance: checking…": "Solde : vérification…",
    "Balance key rejected — open Settings":
        "Clé de solde refusée — ouvrez les réglages",
    "Balance: can't reach Deepgram": "Solde : Deepgram injoignable",
    " — no key": " — aucune clé",
    " — checking the key…": " — vérification de la clé…",
    " — key rejected": " — clé refusée",
    " — could not check the key": " — impossible de vérifier la clé",

    # --- macOS permission dialog ---------------------------------------------
    # Shown by macOS itself, so it follows the system language, not the setting.
    "Vexflow sends your speech to Deepgram with your own API key so it can be "
    "typed as text.":
        "Vexflow envoie votre voix à Deepgram avec votre propre clé d'API pour la restituer sous forme de texte.",

    # --- settings window: frame ----------------------------------------------
    "{} Settings": "Réglages de {}",
    "Interface language": "Langue de l'interface",
    "Restart to apply": "Redémarrer",
    "Applied after the restart in step 3.":
        "Appliqué après le redémarrage de l'étape 3.",
    "Keys": "Clés",
    "Dictation": "Dictée",
    "Cleanup": "Nettoyage",
    "Permissions": "Autorisations",
    "Done": "OK",

    # --- settings: keys ------------------------------------------------------
    "Speech to text": "Reconnaissance vocale",
    "Audio goes from this Mac straight to Deepgram using your own key. "
    "Fields marked * are required.":
        "L'audio part de ce Mac directement vers Deepgram avec votre propre clé. "
        "Les champs marqués d'un * sont obligatoires.",
    "Transcript cleanup": "Nettoyage de la transcription",
    "Optional. A small model fixes punctuation, false starts and mangled "
    "names. Without a key you still get the raw transcript.":
        "Facultatif. Un petit modèle corrige la ponctuation, les faux départs et les "
        "noms écorchés. Sans clé, il vous reste la transcription brute.",
    "Deepgram key": "Clé Deepgram",
    "Balance key": "Clé du solde",
    "Anthropic key": "Clé Anthropic",
    "OpenAI key": "Clé OpenAI",
    "Save": "Valider",
    "Get key": "Obtenir",
    "paste key": "collez la clé",
    "paste a new key to replace": "collez une nouvelle clé pour la remplacer",
    "{} characters — press Save": "{} caractères — cliquez sur Valider",

    # --- settings: key statuses ----------------------------------------------
    "Not set": "Non définie",
    "Saved in Keychain": "Enregistrée dans le trousseau",
    "Required — dictation does not work without it":
        "Obligatoire — sans elle, pas de dictée",
    "Checking with Deepgram…": "Vérification auprès de Deepgram…",
    "Verified — Deepgram accepted this key":
        "Vérifiée — Deepgram a accepté cette clé",
    "Deepgram rejected this key. Check you copied all of it.":
        "Deepgram a refusé cette clé. Vérifiez que vous l'avez copiée en entier.",
    "Saved, but Deepgram could not be reached to check it":
        "Enregistrée, mais Deepgram était injoignable pour la vérifier",
    "Deepgram rejected this key, or it has no billing:read scope":
        "Deepgram a refusé cette clé, ou elle n'a pas la portée billing:read",
    "Checking with {}…": "Vérification auprès de {}…",
    "Verified — {} accepted this key": "Vérifiée — {} a accepté cette clé",
    "{} rejected this key": "{} a refusé cette clé",
    "{} rejected this key: {}": "{} a refusé cette clé : {}",
    "Saved, but {} could not be reached to check it":
        "Enregistrée, mais {} était injoignable pour la vérifier",

    # --- settings: help popovers ---------------------------------------------
    "Open the console": "Ouvrir la console",
    "The one key Vexflow cannot work without. Your microphone audio goes from this "
    "Mac to the speech-to-text service under this key and comes back as text, with "
    "no server of ours in between. Create a key in your own account there and paste "
    "the whole string. It is kept in your login Keychain, never in a file — and, "
    "like any credential on any machine, it is yours to look after.":
        "La seule clé sans laquelle Vexflow ne fonctionne pas. L'audio de votre "
        "micro part de ce Mac vers le service de reconnaissance sous cette clé et "
        "revient en texte, sans aucun serveur à nous entre les deux. Créez une clé "
        "dans votre propre compte là-bas et collez la chaîne entière. Elle réside "
        "dans votre trousseau de session, jamais dans un fichier — et, comme tout "
        "identifiant sur n'importe quelle machine, elle reste à votre charge.",
    "Optional, and a second key on purpose. Reading your account balance needs the "
    "billing:read scope, which the key above has no business holding — one key that "
    "spends and one that reads are worth keeping apart. Create a key with "
    "billing:read only and the menu bar shows the balance the service reports.":
        "Facultatif, et c'est une deuxième clé à dessein. Lire le solde du compte "
        "demande la portée billing:read, que la clé ci-dessus n'a aucune raison de "
        "porter : une clé qui dépense et une clé qui lit le compte gagnent à rester "
        "séparées. Créez une clé avec billing:read seulement et la barre des menus "
        "affichera le solde communiqué par le service.",
    "Optional. Drives the cleanup pass that repairs punctuation, false starts and "
    "mangled names. Only the transcript is sent, never the audio, and what the "
    "service does with it is between you and them. The key is checked the moment "
    "you save it, so a wrong one says so here instead of quietly doing nothing.":
        "Facultatif. Alimente la passe de nettoyage qui répare la ponctuation, les "
        "faux départs et les noms écorchés. Seule la transcription est envoyée, "
        "jamais l'audio, et ce que le service en fait vous regarde, vous et lui. La "
        "clé est vérifiée dès l'enregistrement : une clé fausse le dit ici même au "
        "lieu de ne rien faire en silence.",
    "Optional, and an alternative to the key above rather than an addition — "
    "cleanup uses whichever provider is selected on the Cleanup tab. That tab can "
    "also point this key at any OpenAI-compatible endpoint, including a model "
    "running on your own machine.":
        "Facultatif, et plutôt une solution de rechange à la clé ci-dessus qu'un "
        "ajout : le nettoyage passe par le fournisseur sélectionné dans l'onglet "
        "Nettoyage. C'est là aussi que cette clé peut viser n'importe quelle adresse "
        "compatible OpenAI, y compris un modèle tournant sur votre propre machine.",

    # --- settings: dictation -------------------------------------------------
    "Recognition language": "Langue de reconnaissance",
    "A single language recognises better than Multilingual. Choose "
    "Multilingual only if you switch languages inside one sentence.":
        "Une langue unique est mieux reconnue que le mode multilingue. Ne prenez le "
        "multilingue que si vous changez de langue à l'intérieur d'une phrase.",
    "Push to talk": "Maintien",
    "Hold, speak, release.": "Maintenez, parlez, relâchez.",
    "Hands-free toggle": "Bascule",
    "Off": "Non",
    "Tap once to start, tap again to stop.":
        "Une pression démarre, une autre arrête.",
    "Combined entries fire only while both keys are held — safer when the "
    "free single keys are ones you type with.":
        "Les combinaisons n'agissent que tant que les deux touches sont maintenues. "
        "Utile quand les touches simples encore libres sont celles qui servent à "
        "écrire.",
    "Also toggle with the middle mouse button":
        "Basculer aussi avec le bouton central de la souris",
    "Play a sound when recording starts and stops":
        "Son au début et à la fin de l'enregistrement",
    "Paste automatically (off: copy to clipboard only)":
        "Coller automatiquement (sinon : copier seulement)",

    # --- settings: cleanup ---------------------------------------------------
    "Clean up transcripts with an LLM": "Nettoyer la transcription avec un LLM",
    "Provider": "Fournisseur",
    "Model": "Modèle",
    "No {} key yet — add one on the Keys tab.":
        "Pas encore de clé {} — ajoutez-en une dans l'onglet Clés.",
    "{} rejected the key — check it on the Keys tab.":
        "{} a refusé la clé — vérifiez-la dans l'onglet Clés.",
    "Your vocabulary": "Votre vocabulaire",
    "Edit vocabulary…": "Ouvrir le vocabulaire…",
    "Names and jargon the recogniser keeps getting wrong. One per line, "
    "kept on this Mac.":
        "Noms et jargon que la reconnaissance rate systématiquement. Un par ligne, "
        "le fichier reste sur ce Mac.",
    "Advanced": "Avancé",
    "Endpoint": "Adresse",
    "Leave as-is for the vendor's own API, or point it at any "
    "OpenAI-compatible endpoint.":
        "Laissez tel quel pour l'API du fournisseur, ou pointez vers n'importe "
        "quelle adresse compatible OpenAI.",

    # --- settings: permissions -----------------------------------------------
    "macOS asks for these once. Vexflow cannot record or type without them.":
        "macOS les demande une seule fois. Sans elles, Vexflow ne peut ni "
        "enregistrer ni écrire.",
    "Microphone": "Microphone",
    "Lets Vexflow hear you.": "Pour que Vexflow vous entende.",
    "Accessibility": "Accessibilité",
    "Lets Vexflow see the hotkey and paste into the app you are using. "
    "Granting it takes effect only after Vexflow restarts.":
        "Pour que Vexflow voie le raccourci et colle dans l'app que vous utilisez. "
        "Une fois accordée, elle ne prend effet qu'au redémarrage de Vexflow.",
    "Granted": "Accordée",
    "Not granted": "Non accordée",
    "Not requested yet": "Pas encore demandée",
    "Asked on first use": "Demandée à la première utilisation",
    "Open Settings": "Ouvrir les réglages",
    "Re-check": "Vérifier à nouveau",
    "Restart Vexflow": "Redémarrer Vexflow",
    "Keep a diagnostic log": "Tenir un journal de diagnostic",
    "Off, so nothing about your dictation reaches the disk. Turn it on to "
    "chase a problem and off again afterwards — switching it off deletes the "
    "file. It records timings and errors, never what you said.":
        "Désactivé, donc rien de votre dictée n'atteint le disque. Activez-le pour "
        "traquer un problème, puis désactivez-le : l'extinction supprime le fichier. "
        "Il note des durées et des erreurs, jamais ce que vous avez dit.",
    "Transcript debug logging is ON for this run — dictated text is being "
    "written to the log. Restart without VEXFLOW_DEBUG_TRANSCRIPT to stop it.":
        "Pour cette exécution, la journalisation de débogage des transcriptions est "
        "ACTIVE : le texte dicté est écrit dans le journal. Redémarrez sans "
        "VEXFLOW_DEBUG_TRANSCRIPT pour l'arrêter.",
    "VEXFLOW_DEBUG_TRANSCRIPT is set for this run: switching the log on would "
    "write what you dictate into it.":
        "VEXFLOW_DEBUG_TRANSCRIPT est défini pour cette exécution : activer le "
        "journal y écrirait ce que vous dictez.",
    "Remove Vexflow from this Mac…": "Retirer Vexflow de ce Mac…",

    # --- uninstall dialogs ---------------------------------------------------
    "Remove Vexflow from this Mac?": "Retirer Vexflow de ce Mac ?",
    "This quits Vexflow, removes it from your login items and deletes the "
    "app. Your API keys and settings are kept unless you choose otherwise.":
        "Vexflow se ferme, sort de vos ouvertures de session et l'app est supprimée. "
        "Vos clés et vos réglages sont conservés, sauf choix contraire.",
    "Remove": "Retirer",
    "Cancel": "Annuler",
    "Remove and Delete My Keys": "Retirer avec les clés",
    "Vexflow has been removed.": "Vexflow a été retiré.",
    "Login item removed, but deleting the app was cancelled.":
        "Retiré de l'ouverture de session, mais la suppression de l'app a été "
        "annulée.",
    "Login item removed, but the app could not be deleted.":
        "Retiré de l'ouverture de session, mais l'app n'a pas pu être supprimée.",
    "Login item removed; deleting the app failed: ":
        "Retiré de l'ouverture de session ; la suppression de l'app a échoué : ",
    "Microphone and Accessibility entries stay in System Settings until "
    "you remove them by hand.":
        "Les entrées Microphone et Accessibilité restent dans les Réglages Système "
        "tant que vous ne les retirez pas à la main.",

    # --- setup guide ---------------------------------------------------------
    "Welcome to ": "Bienvenue dans ",
    "Set up ": "Configurer ",
    "macOS needs to grant two permissions before dictation can work. "
    "This takes about a minute.":
        "macOS doit accorder deux autorisations avant que la dictée fonctionne. "
        "Cela prend environ une minute.",
    "Allow microphone access": "Autorisez l'accès au microphone",
    "So Vexflow can hear you.": "Pour que Vexflow vous entende.",
    "Allow accessibility access": "Autorisez l'accès à l'accessibilité",
    "So Vexflow can see the hotkey and paste the text.":
        "Pour que Vexflow voie le raccourci et colle le texte.",
    "macOS applies the accessibility grant only at launch.":
        "macOS n'applique cette autorisation qu'au lancement.",
    "Allow": "Autoriser",
    "Restart": "Redémarrer",
    "Step {} of {}": "Étape {} sur {}",
    "Permissions are set.": "Autorisations accordées.",
    "Denied — turn it on in System Settings":
        "Refusée — activez-la dans les Réglages Système",
    "Requested on first use": "Demandée à la première utilisation",
    "Hotkeys are live": "Les raccourcis fonctionnent",
    "Restart to activate the hotkey": "Redémarrez pour activer le raccourci",
    "Finish step 2 first": "Terminez d'abord l'étape 2",
    "Close": "Fermer",
    "Add your API key": "Ajouter la clé",

    # --- engine notices in the menu ------------------------------------------
    "Restarted after a dead microphone — please dictate again":
        "Redémarré après un micro mort — dictez à nouveau",
    "No Accessibility permission — hotkeys are dead":
        "Pas d'autorisation d'accessibilité — raccourcis morts",
    "Microphone still dead after a restart — check System Settings > Sound":
        "Micro toujours mort après redémarrage — voyez Réglages Système > Son",
    "Microphone is dead — restart Vexflow manually":
        "Micro mort — redémarrez Vexflow à la main",
    "Microphone did not open — check input and permissions":
        "Le micro ne s'est pas ouvert — vérifiez l'entrée et les autorisations",
    "Microphone is dead — restarting": "Micro mort — redémarrage",
    "Microphone rebuilt mid-recording — the start may be lost":
        "Micro reconstruit en pleine prise — le début peut manquer",
    "Deepgram connection dropped — text lost":
        "Connexion à Deepgram coupée — texte perdu",
    "Deepgram unreachable — check your connection":
        "Deepgram injoignable — vérifiez la connexion",
    "Copied — press Cmd-V to paste": "Copié — collez avec Cmd-V",
    "duration limit": "limite de durée",
    "Deepgram connection dropped": "connexion à Deepgram coupée",
    "Stopped ({}) — text is on the clipboard, press Cmd-V":
        "Arrêté ({}) — le texte est dans le presse-papiers, faites Cmd-V",

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
        "Fourni en l'état, sans garantie d'aucune sorte, et utilisé entièrement à vos "
        "propres risques.\n\n"
        "{app} est un client pour des services externes que vous choisissez, auprès "
        "desquels vous avez des comptes et que vous payez directement. Ces services "
        "ne sont ni exploités par {vendor} ni responsables devant elle : leurs "
        "conditions, leurs tarifs et le traitement de vos données relèvent de vous et "
        "d'eux, et rien ici n'est dit en leur nom. Ce qui est dépensé via vos clés "
        "vous incombe, et aucun engagement n'est pris quant à la sûreté d'une clé que "
        "vous saisissez.\n\n"
        "Les autres noms appartiennent à leurs propriétaires et n'apparaissent que "
        "pour désigner ce à quoi ceci se connecte. Aucune affiliation ni aucun aval "
        "n'est revendiqué.",

    # --- languages -----------------------------------------------------------
    "English": "Anglais",
    "Multilingual (code-switching)": "Multilingue (changement à la volée)",
    "Spanish": "Espagnol",
    "German": "Allemand",
    "French": "Français",
    "Portuguese": "Portugais",
    "Italian": "Italien",
    "Dutch": "Néerlandais",
    "Russian": "Russe",
    "Ukrainian": "Ukrainien",
    "Polish": "Polonais",
    "Turkish": "Turc",
    "Hindi": "Hindi",
    "Japanese": "Japonais",

    # --- hotkeys -------------------------------------------------------------
    # Command, Option, Control and Shift stay: they are what is printed on the keys.
    "Right Command": "Command droite",
    "Right Option": "Option droite",
    "Left Command": "Command gauche",
    "Left Option": "Option gauche",
    "Left Control": "Control gauche",
    "Right Control": "Control droite",
    "Left Shift": "Shift gauche",
    "Right Shift": "Shift droite",
    "Control + Option": "Control + Option",
    "Control + Shift": "Control + Shift",
    "Command + Option": "Command + Option",
    "Option + Shift": "Option + Shift",
    "Control + Option + Shift": "Control + Option + Shift",

    # --- cleanup models ------------------------------------------------------
    # Model names are proper nouns; only what they are good for is translated.
    "Haiku 4.5 — fastest, cheapest": "Haiku 4.5 — la plus rapide et la moins chère",
    "Sonnet 5 — balanced": "Sonnet 5 — équilibrée",
    "Opus 5 — most accurate": "Opus 5 — la plus précise",
    "GPT-5.6 Luna — fastest, cheapest":
        "GPT-5.6 Luna — la plus rapide et la moins chère",
    "GPT-5.6 Terra — balanced": "GPT-5.6 Terra — équilibrée",
    "GPT-5.6 Sol — most accurate": "GPT-5.6 Sol — la plus précise",
}
