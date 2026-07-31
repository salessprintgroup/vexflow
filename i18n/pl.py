"""Polish interface strings.

The key is the English source string, so an entry that is missing here falls back to
English rather than to a bare identifier. Adding or fixing a language: see README.md
in this directory.
"""
TABLE = {
    # --- menu bar ------------------------------------------------------------
    "Ready": "Gotowy",
    "Recording…": "Nagrywanie…",
    "Paused": "Wstrzymane",
    "Stop recording": "Zatrzymaj nagrywanie",
    "Pause": "Wstrzymaj",
    "Resume": "Wznów",
    "Language": "Język rozpoznawania",
    "LLM Cleanup": "Czyszczenie LLM",
    "Clean up transcripts": "Czyść transkrypcję",
    "Setup Guide…": "Pierwsze kroki…",
    "Settings…": "Ustawienia…",
    "Open log": "Otwórz dziennik",
    "Vexflow on GitHub": "Vexflow na GitHubie",
    "Built by ": "Wykonanie: ",
    "Quit Vexflow": "Zakończ",
    "About ": "Informacje o ",
    "Hide ": "Ukryj ",
    "Quit ": "Zakończ ",
    "Edit": "Edycja",
    "Undo": "Cofnij",
    "Redo": "Ponów",
    "Cut": "Wytnij",
    "Copy": "Kopiuj",
    "Paste": "Wklej",
    "Select All": "Zaznacz wszystko",
    "Hold ": "Przytrzymaj ",
    "tap ": "naciśnij ",
    "middle mouse button": "środkowy przycisk myszy",

    # --- key states, menu bar ------------------------------------------------
    "No Deepgram key — open Settings": "Brak klucza Deepgram — otwórz ustawienia",
    "Checking your Deepgram key…": "Sprawdzanie klucza Deepgram…",
    "Deepgram rejected your key — open Settings":
        "Deepgram odrzucił klucz — otwórz ustawienia",
    "Can't reach Deepgram — check your connection":
        "Deepgram nieosiągalny — sprawdź połączenie",
    "Balance: {}": "Saldo: {}",
    "Balance: {} — running low": "Saldo: {} — na wyczerpaniu",
    "Balance: …": "Saldo: …",
    "Balance: checking…": "Saldo: sprawdzanie…",
    "Balance key rejected — open Settings":
        "Klucz salda odrzucony — otwórz ustawienia",
    "Balance: can't reach Deepgram": "Saldo: Deepgram nieosiągalny",
    " — no key": " — brak klucza",
    " — checking the key…": " — sprawdzanie klucza…",
    " — key rejected": " — klucz odrzucony",
    " — could not check the key": " — nie udało się sprawdzić klucza",

    # --- macOS permission dialog ---------------------------------------------
    # Shown by macOS itself, so it follows the system language, not the setting.
    "Vexflow sends your speech to Deepgram with your own API key so it can be "
    "typed as text.":
        "Vexflow wysyła twoją mowę do Deepgram na twoim własnym kluczu API, aby wróciła jako tekst.",

    # --- settings window: frame ----------------------------------------------
    "{} Settings": "Ustawienia {}",
    "Interface language": "Język interfejsu",
    "Restart to apply": "Uruchom ponownie",
    "Applied after the restart in step 3.":
        "Zadziała po ponownym uruchomieniu w kroku 3.",
    "Keys": "Klucze",
    "Dictation": "Dyktowanie",
    "Cleanup": "Czyszczenie",
    "Permissions": "Uprawnienia",
    "Done": "Gotowe",

    # --- settings: keys ------------------------------------------------------
    "Speech to text": "Rozpoznawanie mowy",
    "Audio goes from this Mac straight to Deepgram using your own key. "
    "Fields marked * are required.":
        "Dźwięk idzie z tego Maca prosto do Deepgram na twoim własnym kluczu. Pola "
        "oznaczone gwiazdką są wymagane.",
    "Transcript cleanup": "Czyszczenie transkrypcji",
    "Optional. A small model fixes punctuation, false starts and mangled "
    "names. Without a key you still get the raw transcript.":
        "Opcjonalne. Mały model poprawia interpunkcję, przejęzyczenia i przekręcone "
        "nazwiska. Bez klucza zostaje surowa transkrypcja.",
    "Deepgram key": "Klucz Deepgram",
    "Balance key": "Klucz do salda",
    "Anthropic key": "Klucz Anthropic",
    "OpenAI key": "Klucz OpenAI",
    "Save": "Zapisz",
    "Get key": "Pobierz",
    "paste key": "wklej klucz",
    "paste a new key to replace": "wklej nowy klucz, aby zastąpić",
    "{} characters — press Save": "znaków: {} — kliknij Zapisz",

    # --- settings: key statuses ----------------------------------------------
    "Not set": "Nie ustawiony",
    "Saved in Keychain": "Zapisany w pęku kluczy",
    "Required — dictation does not work without it":
        "Wymagany — bez niego dyktowanie nie działa",
    "Checking with Deepgram…": "Sprawdzanie w Deepgram…",
    "Verified — Deepgram accepted this key":
        "Sprawdzony — Deepgram przyjął ten klucz",
    "Deepgram rejected this key. Check you copied all of it.":
        "Deepgram odrzucił ten klucz. Sprawdź, czy został skopiowany w całości.",
    "Saved, but Deepgram could not be reached to check it":
        "Zapisany, ale Deepgram był nieosiągalny podczas sprawdzania",
    "Deepgram rejected this key, or it has no billing:read scope":
        "Deepgram odrzucił ten klucz albo nie ma on zakresu billing:read",
    "Checking with {}…": "Sprawdzanie w {}…",
    "Verified — {} accepted this key": "Sprawdzony — {} przyjął ten klucz",
    "{} rejected this key": "{} odrzucił ten klucz",
    "{} rejected this key: {}": "{} odrzucił ten klucz: {}",
    "Saved, but {} could not be reached to check it":
        "Zapisany, ale {} był nieosiągalny podczas sprawdzania",

    # --- settings: help popovers ---------------------------------------------
    "Open the console": "Otwórz konsolę",
    "The one key Vexflow cannot work without. Your microphone audio goes from this "
    "Mac to the speech-to-text service under this key and comes back as text, with "
    "no server of ours in between. Create a key in your own account there and paste "
    "the whole string. It is kept in your login Keychain, never in a file — and, "
    "like any credential on any machine, it is yours to look after.":
        "Jedyny klucz, bez którego Vexflow nie działa. Dźwięk z mikrofonu idzie z "
        "tego Maca do usługi rozpoznawania na tym kluczu i wraca jako tekst, bez "
        "żadnego naszego serwera po drodze. Załóż klucz na własnym koncie tam i "
        "wklej cały ciąg. Leży w pęku kluczy logowania, nigdy w pliku — i, jak każde "
        "poświadczenie na każdej maszynie, pozostaje pod twoją opieką.",
    "Optional, and a second key on purpose. Reading your account balance needs the "
    "billing:read scope, which the key above has no business holding — one key that "
    "spends and one that reads are worth keeping apart. Create a key with "
    "billing:read only and the menu bar shows the balance the service reports.":
        "Opcjonalny i celowo drugi. Odczyt salda wymaga zakresu billing:read, którego "
        "klucz powyżej nie ma po co nosić: klucz, który wydaje, i klucz, który czyta "
        "rachunek, lepiej trzymać osobno. Załóż klucz wyłącznie z billing:read, a "
        "pasek menu pokaże saldo podawane przez usługę.",
    "Optional. Drives the cleanup pass that repairs punctuation, false starts and "
    "mangled names. Only the transcript is sent, never the audio, and what the "
    "service does with it is between you and them. The key is checked the moment "
    "you save it, so a wrong one says so here instead of quietly doing nothing.":
        "Opcjonalny. Napędza przebieg czyszczenia, który naprawia interpunkcję, "
        "przejęzyczenia i przekręcone nazwiska. Wysyłana jest wyłącznie transkrypcja, "
        "nigdy dźwięk, a co usługa z nią robi, jest sprawą między tobą a nią. Klucz "
        "jest sprawdzany w chwili zapisu, więc o błędnym dowiesz się tutaj, zamiast "
        "milczącego bezczynnego trwania.",
    "Optional, and an alternative to the key above rather than an addition — "
    "cleanup uses whichever provider is selected on the Cleanup tab. That tab can "
    "also point this key at any OpenAI-compatible endpoint, including a model "
    "running on your own machine.":
        "Opcjonalny i raczej zamiennik klucza powyżej niż dodatek: czyszczenie idzie "
        "przez dostawcę wybranego w zakładce Czyszczenie. Tam też ten klucz można "
        "skierować na dowolny adres zgodny z OpenAI, łącznie z modelem działającym "
        "na własnej maszynie.",

    # --- settings: dictation -------------------------------------------------
    "Recognition language": "Język rozpoznawania",
    "A single language recognises better than Multilingual. Choose "
    "Multilingual only if you switch languages inside one sentence.":
        "Jeden wybrany język rozpoznaje się lepiej niż tryb wielojęzyczny. Wybierz "
        "wielojęzyczny tylko wtedy, gdy zmieniasz język w środku zdania.",
    "Push to talk": "Przytrzymanie",
    "Hold, speak, release.": "Przytrzymaj, mów, puść.",
    "Hands-free toggle": "Przełącznik",
    "Off": "Wył.",
    "Tap once to start, tap again to stop.":
        "Jedno naciśnięcie zaczyna, kolejne kończy.",
    "Combined entries fire only while both keys are held — safer when the "
    "free single keys are ones you type with.":
        "Kombinacje działają tylko wtedy, gdy oba klawisze są wciśnięte. Przydaje "
        "się, gdy wolne pojedyncze klawisze to te, którymi się pisze.",
    "Also toggle with the middle mouse button":
        "Przełączaj także środkowym przyciskiem myszy",
    "Play a sound when recording starts and stops":
        "Dźwięk na początku i na końcu nagrania",
    "Paste automatically (off: copy to clipboard only)":
        "Wklejaj od razu (wył.: tylko kopiuj do schowka)",

    # --- settings: cleanup ---------------------------------------------------
    "Clean up transcripts with an LLM": "Czyść transkrypcję przez LLM",
    "Provider": "Dostawca",
    "Model": "Model",
    "No {} key yet — add one on the Keys tab.":
        "Nie ma jeszcze klucza {} — dodaj go w zakładce Klucze.",
    "{} rejected the key — check it on the Keys tab.":
        "{} odrzucił klucz — sprawdź go w zakładce Klucze.",
    "Your vocabulary": "Własny słownik",
    "Edit vocabulary…": "Otwórz słownik…",
    "Names and jargon the recogniser keeps getting wrong. One per line, "
    "kept on this Mac.":
        "Nazwiska i żargon, które rozpoznawanie stale przekręca. Po jednym w wierszu, "
        "plik zostaje na tym Macu.",
    "Advanced": "Zaawansowane",
    "Endpoint": "Adres",
    "Leave as-is for the vendor's own API, or point it at any "
    "OpenAI-compatible endpoint.":
        "Zostaw bez zmian dla własnego API dostawcy albo wskaż dowolny adres zgodny "
        "z OpenAI.",

    # --- settings: permissions -----------------------------------------------
    "macOS asks for these once. Vexflow cannot record or type without them.":
        "macOS pyta o nie raz. Bez nich Vexflow nie nagra i nie napisze.",
    "Microphone": "Mikrofon",
    "Lets Vexflow hear you.": "Żeby Vexflow cię słyszał.",
    "Accessibility": "Dostępność",
    "Lets Vexflow see the hotkey and paste into the app you are using. "
    "Granting it takes effect only after Vexflow restarts.":
        "Żeby Vexflow widział skrót i wklejał w używanej właśnie aplikacji. Nadane "
        "uprawnienie zadziała dopiero po ponownym uruchomieniu Vexflow.",
    "Granted": "Nadane",
    "Not granted": "Nienadane",
    "Not requested yet": "Jeszcze nieproszone",
    "Asked on first use": "Pytanie przy pierwszym użyciu",
    "Open Settings": "Otwórz ustawienia",
    "Re-check": "Sprawdź ponownie",
    # Without "Vexflow": the full name overruns the button by four points, and the
    # button sits inside Vexflow's own window, where there is nothing else to restart.
    "Restart Vexflow": "Uruchom ponownie",
    "Keep a diagnostic log": "Prowadź dziennik diagnostyczny",
    "Off, so nothing about your dictation reaches the disk. Turn it on to "
    "chase a problem and off again afterwards — switching it off deletes the "
    "file. It records timings and errors, never what you said.":
        "Wyłączony, więc nic o dyktowaniu nie trafia na dysk. Włącz, gdy tropisz "
        "problem, i wyłącz potem — wyłączenie kasuje plik. Zapisuje czasy i błędy, "
        "nigdy tego, co zostało powiedziane.",
    "Transcript debug logging is ON for this run — dictated text is being "
    "written to the log. Restart without VEXFLOW_DEBUG_TRANSCRIPT to stop it.":
        "W tym uruchomieniu włączone jest diagnostyczne zapisywanie transkrypcji: "
        "podyktowany tekst trafia do dziennika. Uruchom ponownie bez "
        "VEXFLOW_DEBUG_TRANSCRIPT, aby to przerwać.",
    "VEXFLOW_DEBUG_TRANSCRIPT is set for this run: switching the log on would "
    "write what you dictate into it.":
        "W tym uruchomieniu ustawiono VEXFLOW_DEBUG_TRANSCRIPT: włączenie dziennika "
        "zapisałoby w nim to, co dyktujesz.",
    "Remove Vexflow from this Mac…": "Usuń Vexflow z tego Maca…",

    # --- uninstall dialogs ---------------------------------------------------
    "Remove Vexflow from this Mac?": "Usunąć Vexflow z tego Maca?",
    "This quits Vexflow, removes it from your login items and deletes the "
    "app. Your API keys and settings are kept unless you choose otherwise.":
        "Vexflow zakończy działanie, zniknie z elementów logowania, a aplikacja "
        "zostanie skasowana. Klucze i ustawienia zostają, o ile nie wybierzesz "
        "inaczej.",
    "Remove": "Usuń",
    "Cancel": "Anuluj",
    "Remove and Delete My Keys": "Usuń razem z kluczami",
    "Vexflow has been removed.": "Vexflow został usunięty.",
    "Login item removed, but deleting the app was cancelled.":
        "Usunięto z elementów logowania, ale kasowanie aplikacji anulowano.",
    "Login item removed, but the app could not be deleted.":
        "Usunięto z elementów logowania, ale aplikacji nie udało się skasować.",
    "Login item removed; deleting the app failed: ":
        "Usunięto z elementów logowania; kasowanie aplikacji nie powiodło się: ",
    "Microphone and Accessibility entries stay in System Settings until "
    "you remove them by hand.":
        "Wpisy w Mikrofonie i Dostępności zostaną w ustawieniach systemowych, dopóki "
        "nie usuniesz ich ręcznie.",

    # --- setup guide ---------------------------------------------------------
    "Welcome to ": "Witamy w ",
    "Set up ": "Konfiguracja ",
    "macOS needs to grant two permissions before dictation can work. "
    "This takes about a minute.":
        "Zanim dyktowanie zadziała, macOS musi nadać dwa uprawnienia. To około "
        "minuty.",
    "Allow microphone access": "Zezwól na dostęp do mikrofonu",
    "So Vexflow can hear you.": "Żeby Vexflow cię słyszał.",
    "Allow accessibility access": "Zezwól na dostęp w Dostępności",
    "So Vexflow can see the hotkey and paste the text.":
        "Żeby Vexflow widział skrót i wklejał tekst.",
    "macOS applies the accessibility grant only at launch.":
        "macOS uwzględnia to uprawnienie dopiero przy starcie.",
    "Allow": "Zezwól",
    "Restart": "Uruchom ponownie",
    "Step {} of {}": "Krok {} z {}",
    "Permissions are set.": "Uprawnienia nadane.",
    "Denied — turn it on in System Settings":
        "Odmowa — włącz w ustawieniach systemowych",
    "Requested on first use": "Pytanie przy pierwszym użyciu",
    "Hotkeys are live": "Skróty działają",
    "Restart to activate the hotkey": "Uruchom ponownie, aby skrót zadziałał",
    "Finish step 2 first": "Najpierw dokończ krok 2",
    "Close": "Zamknij",
    "Add your API key": "Dodaj klucz",

    # --- engine notices in the menu ------------------------------------------
    "Restarted after a dead microphone — please dictate again":
        "Uruchomiono ponownie po martwym mikrofonie — podyktuj jeszcze raz",
    "No Accessibility permission — hotkeys are dead":
        "Brak uprawnienia Dostępności — skróty martwe",
    "Microphone still dead after a restart — check System Settings > Sound":
        "Mikrofon martwy także po restarcie — zajrzyj do Ustawienia > Dźwięk",
    "Microphone is dead — restart Vexflow manually":
        "Mikrofon martwy — uruchom Vexflow ponownie ręcznie",
    "Microphone did not open — check input and permissions":
        "Mikrofon się nie otworzył — sprawdź wejście i uprawnienia",
    "Microphone is dead — restarting": "Mikrofon martwy — uruchamiam ponownie",
    "Microphone rebuilt mid-recording — the start may be lost":
        "Mikrofon odbudowany w trakcie nagrania — początek mógł przepaść",
    "Deepgram connection dropped — text lost":
        "Połączenie z Deepgram zerwane — tekst przepadł",
    "Deepgram unreachable — check your connection":
        "Deepgram nieosiągalny — sprawdź połączenie",
    "Copied — press Cmd-V to paste": "Skopiowano — wklej przez Cmd-V",
    "duration limit": "limit długości",
    "Deepgram connection dropped": "połączenie z Deepgram zerwane",
    "Stopped ({}) — text is on the clipboard, press Cmd-V":
        "Zatrzymano ({}) — tekst jest w schowku, naciśnij Cmd-V",

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
        "Dostarczane w stanie, w jakim jest, bez gwarancji jakiegokolwiek rodzaju, i "
        "używane wyłącznie na własne ryzyko.\n\n"
        "{app} jest klientem usług zewnętrznych, które wybierasz sam, w których masz "
        "własne konta i za które płacisz bezpośrednio. Usługi te nie są prowadzone "
        "przez {vendor} ani przed nią odpowiedzialne: ich warunki, ceny i "
        "postępowanie z twoimi danymi to sprawa między tobą a nimi, a tutaj nic nie "
        "jest mówione w ich imieniu. Wszystko, co wydane na twoich kluczach, jest "
        "twoje, i nie składa się żadnych zapewnień co do bezpieczeństwa "
        "wprowadzonego klucza.\n\n"
        "Pozostałe nazwy należą do ich właścicieli i pojawiają się wyłącznie po to, "
        "by wskazać, z czym to się łączy. Nie jest zgłaszane żadne powiązanie ani "
        "poparcie.",

    # --- languages -----------------------------------------------------------
    "English": "angielski",
    "Multilingual (code-switching)": "wielojęzyczny (zmiana w locie)",
    "Spanish": "hiszpański",
    "German": "niemiecki",
    "French": "francuski",
    "Portuguese": "portugalski",
    "Italian": "włoski",
    "Dutch": "niderlandzki",
    "Russian": "rosyjski",
    "Ukrainian": "ukraiński",
    "Polish": "polski",
    "Turkish": "turecki",
    "Hindi": "hindi",
    "Japanese": "japoński",

    # --- hotkeys -------------------------------------------------------------
    # Command, Option, Control and Shift stay: they are what is printed on the keys.
    "Right Command": "prawy Command",
    "Right Option": "prawy Option",
    "Left Command": "lewy Command",
    "Left Option": "lewy Option",
    "Left Control": "lewy Control",
    "Right Control": "prawy Control",
    "Left Shift": "lewy Shift",
    "Right Shift": "prawy Shift",
    "Control + Option": "Control + Option",
    "Control + Shift": "Control + Shift",
    "Command + Option": "Command + Option",
    "Option + Shift": "Option + Shift",
    "Control + Option + Shift": "Control + Option + Shift",

    # --- cleanup models ------------------------------------------------------
    # Model names are proper nouns; only what they are good for is translated.
    "Haiku 4.5 — fastest, cheapest": "Haiku 4.5 — najszybszy i najtańszy",
    "Sonnet 5 — balanced": "Sonnet 5 — złoty środek",
    "Opus 5 — most accurate": "Opus 5 — najdokładniejszy",
    "GPT-5.6 Luna — fastest, cheapest": "GPT-5.6 Luna — najszybszy i najtańszy",
    "GPT-5.6 Terra — balanced": "GPT-5.6 Terra — złoty środek",
    "GPT-5.6 Sol — most accurate": "GPT-5.6 Sol — najdokładniejszy",
}
