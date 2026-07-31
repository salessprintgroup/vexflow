"""Russian interface strings.

The key is the English source string, so an entry that is missing here falls back to
English rather than to a bare identifier. Adding or fixing a language: see README.md
in this directory.
"""
TABLE = {
    # --- menu bar ------------------------------------------------------------
    "Ready": "Готов",
    "Recording…": "Запись…",
    "Paused": "На паузе",
    "Stop recording": "Остановить запись",
    "Pause": "Пауза",
    "Resume": "Возобновить",
    "Language": "Язык распознавания",
    "LLM Cleanup": "Очистка LLM",
    "Clean up transcripts": "Чистить расшифровку",
    "Setup Guide…": "Первый запуск…",
    "Settings…": "Настройки…",
    "Open log": "Открыть лог",
    "Vexflow on GitHub": "Vexflow на GitHub",
    "Built by ": "Сделано в ",
    "Quit Vexflow": "Выйти",
    "About ": "О программе ",
    "Hide ": "Скрыть ",
    "Quit ": "Выйти из ",
    "Edit": "Правка",
    "Undo": "Отменить",
    "Redo": "Повторить",
    "Cut": "Вырезать",
    "Copy": "Копировать",
    "Paste": "Вставить",
    "Select All": "Выделить всё",
    "Hold ": "Удерживай ",
    "tap ": "нажми ",
    "middle mouse button": "средняя кнопка мыши",

    # --- key states, menu bar ------------------------------------------------
    "No Deepgram key — open Settings": "Нет ключа Deepgram — открой настройки",
    "Checking your Deepgram key…": "Проверяю ключ Deepgram…",
    "Deepgram rejected your key — open Settings":
        "Deepgram не принял ключ — открой настройки",
    "Can't reach Deepgram — check your connection":
        "Deepgram недоступен — проверь связь",
    "Balance: {}": "Баланс: {}",
    "Balance: {} — running low": "Баланс: {} — на исходе",
    "Balance: …": "Баланс: …",
    "Balance: checking…": "Баланс: проверяю…",
    "Balance key rejected — open Settings":
        "Ключ баланса не принят — открой настройки",
    "Balance: can't reach Deepgram": "Баланс: Deepgram недоступен",
    " — no key": " — нет ключа",
    " — checking the key…": " — проверяю ключ…",
    " — key rejected": " — ключ не принят",
    " — could not check the key": " — не удалось проверить ключ",

    # --- macOS permission dialog ---------------------------------------------
    # Shown by macOS itself, so it follows the system language, not the setting.
    "Vexflow sends your speech to Deepgram with your own API key so it can be "
    "typed as text.":
        "Vexflow отправляет вашу речь в Deepgram по вашему собственному ключу, чтобы вернуть её текстом.",

    # --- settings window: frame ----------------------------------------------
    "{} Settings": "{} — настройки",
    "Interface language": "Язык интерфейса",
    "Keys": "Ключи",
    "Dictation": "Диктовка",
    "Cleanup": "Очистка",
    "Permissions": "Доступы",
    "Done": "Готово",

    # --- settings: keys ------------------------------------------------------
    "Speech to text": "Распознавание речи",
    "Audio goes from this Mac straight to Deepgram using your own key. "
    "Fields marked * are required.":
        "Звук уходит с этого Mac прямо в Deepgram по твоему ключу. "
        "Поля со звёздочкой обязательны.",
    "Transcript cleanup": "Очистка расшифровки",
    "Optional. A small model fixes punctuation, false starts and mangled "
    "names. Without a key you still get the raw transcript.":
        "По желанию. Небольшая модель правит пунктуацию, оговорки и перевранные "
        "имена. Без ключа останется сырая расшифровка.",
    "Deepgram key": "Ключ Deepgram",
    "Balance key": "Ключ для баланса",
    "Anthropic key": "Ключ Anthropic",
    "OpenAI key": "Ключ OpenAI",
    "Save": "Сохранить",
    "Get key": "Получить",
    "paste key": "вставь ключ",
    "paste a new key to replace": "вставь новый ключ, чтобы заменить",
    "{} characters — press Save": "символов: {} — нажми «Сохранить»",

    # --- settings: key statuses ----------------------------------------------
    "Not set": "Не задан",
    "Saved in Keychain": "Сохранён в связке ключей",
    "Required — dictation does not work without it":
        "Обязателен — без него диктовка не работает",
    "Checking with Deepgram…": "Проверяю в Deepgram…",
    "Verified — Deepgram accepted this key": "Проверен — Deepgram принял ключ",
    "Deepgram rejected this key. Check you copied all of it.":
        "Deepgram не принял ключ. Проверь, что скопировал его целиком.",
    "Saved, but Deepgram could not be reached to check it":
        "Сохранён, но проверить не вышло — Deepgram недоступен",
    "Deepgram rejected this key, or it has no billing:read scope":
        "Deepgram не принял ключ, либо у него нет права billing:read",
    "Checking with {}…": "Проверяю в {}…",
    "Verified — {} accepted this key": "Проверен — {} принял ключ",
    "{} rejected this key": "{} не принял ключ",
    "{} rejected this key: {}": "{} не принял ключ: {}",
    "Saved, but {} could not be reached to check it":
        "Сохранён, но проверить не вышло — {} недоступен",

    # --- settings: help popovers ---------------------------------------------
    "Open the console": "Открыть консоль",
    "The one key Vexflow cannot work without. Your microphone audio goes from this "
    "Mac to the speech-to-text service under this key and comes back as text, with "
    "no server of ours in between. Create a key in your own account there and paste "
    "the whole string. It is kept in your login Keychain, never in a file — and, "
    "like any credential on any machine, it is yours to look after.":
        "Единственный ключ, без которого Vexflow не работает. Звук с микрофона "
        "уходит с этого Mac в сервис распознавания по этому ключу и возвращается "
        "текстом; нашего сервера в этой цепочке нет. Заведи ключ в своём аккаунте "
        "там и вставь строку целиком. Он лежит в связке ключей, не в файле — и, как "
        "любой ключ на любой машине, остаётся твоей заботой.",
    "Optional, and a second key on purpose. Reading your account balance needs the "
    "billing:read scope, which the key above has no business holding — one key that "
    "spends and one that reads are worth keeping apart. Create a key with "
    "billing:read only and the menu bar shows the balance the service reports.":
        "По желанию, и это намеренно второй ключ. Чтобы читать баланс, нужно право "
        "billing:read, которого у ключа выше быть не должно: ключ, который тратит, и "
        "ключ, который читает счёт, лучше держать врозь. Заведи ключ только с "
        "billing:read — и в строке меню появится баланс, который отдаёт сервис.",
    "Optional. Drives the cleanup pass that repairs punctuation, false starts and "
    "mangled names. Only the transcript is sent, never the audio, and what the "
    "service does with it is between you and them. The key is checked the moment "
    "you save it, so a wrong one says so here instead of quietly doing nothing.":
        "По желанию. Питает проход очистки, который правит пунктуацию, оговорки и "
        "перевранные имена. Уходит только текст расшифровки, звук — никогда; что "
        "сервис с ним делает, решаешь ты и он. Ключ проверяется сразу при "
        "сохранении, поэтому про неверный будет сказано здесь же.",
    "Optional, and an alternative to the key above rather than an addition — "
    "cleanup uses whichever provider is selected on the Cleanup tab. That tab can "
    "also point this key at any OpenAI-compatible endpoint, including a model "
    "running on your own machine.":
        "По желанию, и это замена ключу выше, а не дополнение: очистка работает "
        "через того поставщика, который выбран на вкладке «Очистка». Там же этот "
        "ключ можно направить на любой адрес, совместимый с OpenAI, включая модель "
        "на твоей машине.",

    # --- settings: dictation -------------------------------------------------
    "Recognition language": "Язык распознавания",
    "A single language recognises better than Multilingual. Choose "
    "Multilingual only if you switch languages inside one sentence.":
        "Один выбранный язык распознаётся точнее, чем мультиязычный режим. Бери "
        "мультиязычный, только если переключаешь языки внутри фразы.",
    "Push to talk": "Удержание",
    "Hold, speak, release.": "Зажми, говори, отпусти.",
    "Hands-free toggle": "Переключатель",
    "Off": "Выкл",
    "Tap once to start, tap again to stop.":
        "Нажми — начнётся запись, нажми ещё раз — закончится.",
    "Combined entries fire only while both keys are held — safer when the "
    "free single keys are ones you type with.":
        "Сочетания срабатывают, только пока зажаты обе клавиши. Это спасает, когда "
        "все свободные одиночные клавиши — те, которыми ты печатаешь.",
    "Also toggle with the middle mouse button":
        "Переключать ещё и средней кнопкой мыши",
    "Play a sound when recording starts and stops":
        "Звук в начале и в конце записи",
    "Paste automatically (off: copy to clipboard only)":
        "Вставлять сразу (выкл — только копировать в буфер)",

    # --- settings: cleanup ---------------------------------------------------
    "Clean up transcripts with an LLM": "Чистить расшифровку через LLM",
    "Provider": "Поставщик",
    "Model": "Модель",
    "No {} key yet — add one on the Keys tab.":
        "Ключа {} ещё нет — добавь его на вкладке «Ключи».",
    "{} rejected the key — check it on the Keys tab.":
        "{} не принял ключ — проверь его на вкладке «Ключи».",
    "Your vocabulary": "Свой словарь",
    "Edit vocabulary…": "Открыть словарь…",
    "Names and jargon the recogniser keeps getting wrong. One per line, "
    "kept on this Mac.":
        "Имена и жаргон, которые распознавание стабильно перевирает. По одному в "
        "строке, файл остаётся на этом Mac.",
    "Advanced": "Для продвинутых",
    "Endpoint": "Адрес",
    "Leave as-is for the vendor's own API, or point it at any "
    "OpenAI-compatible endpoint.":
        "Оставь как есть для штатного API поставщика или укажи любой адрес, "
        "совместимый с OpenAI.",

    # --- settings: permissions -----------------------------------------------
    "macOS asks for these once. Vexflow cannot record or type without them.":
        "macOS спросит про них один раз. Без них Vexflow не запишет и не напечатает.",
    "Microphone": "Микрофон",
    "Lets Vexflow hear you.": "Чтобы Vexflow тебя слышал.",
    "Accessibility": "Универсальный доступ",
    "Lets Vexflow see the hotkey and paste into the app you are using. "
    "Granting it takes effect only after Vexflow restarts.":
        "Чтобы Vexflow видел горячую клавишу и вставлял текст в открытую программу. "
        "Выданный доступ подхватится только после перезапуска Vexflow.",
    "Granted": "Выдан",
    "Not granted": "Не выдан",
    "Not requested yet": "Ещё не запрашивался",
    "Asked on first use": "Спросят при первом обращении",
    "Open Settings": "Открыть настройки",
    "Re-check": "Проверить снова",
    "Restart Vexflow": "Перезапустить Vexflow",
    "Keep a diagnostic log": "Вести диагностический лог",
    "Off, so nothing about your dictation reaches the disk. Turn it on to "
    "chase a problem and off again afterwards — switching it off deletes the "
    "file. It records timings and errors, never what you said.":
        "Выключен, поэтому на диск про твою диктовку не попадает ничего. Включи, "
        "когда ловишь проблему, и выключи после — выключение стирает файл. В логе "
        "тайминги и ошибки, сказанного там нет никогда.",
    "Transcript debug logging is ON for this run — dictated text is being "
    "written to the log. Restart without VEXFLOW_DEBUG_TRANSCRIPT to stop it.":
        "Для этого запуска включена отладочная запись расшифровок: надиктованный "
        "текст пишется в лог. Перезапусти без VEXFLOW_DEBUG_TRANSCRIPT, чтобы "
        "прекратить.",
    "VEXFLOW_DEBUG_TRANSCRIPT is set for this run: switching the log on would "
    "write what you dictate into it.":
        "Для этого запуска задан VEXFLOW_DEBUG_TRANSCRIPT: если включить лог, "
        "надиктованное будет попадать в него.",
    "Remove Vexflow from this Mac…": "Удалить Vexflow с этого Mac…",

    # --- uninstall dialogs ---------------------------------------------------
    "Remove Vexflow from this Mac?": "Удалить Vexflow с этого Mac?",
    "This quits Vexflow, removes it from your login items and deletes the "
    "app. Your API keys and settings are kept unless you choose otherwise.":
        "Vexflow закроется, уйдёт из автозапуска, и программа будет удалена. Ключи "
        "и настройки останутся, если не выбрать другое.",
    "Remove": "Удалить",
    "Cancel": "Отмена",
    "Remove and Delete My Keys": "Удалить вместе с ключами",
    "Vexflow has been removed.": "Vexflow удалён.",
    "Login item removed, but deleting the app was cancelled.":
        "Из автозапуска убран, но удаление программы отменено.",
    "Login item removed, but the app could not be deleted.":
        "Из автозапуска убран, но удалить программу не вышло.",
    "Login item removed; deleting the app failed: ":
        "Из автозапуска убран; удалить программу не вышло: ",
    "Microphone and Accessibility entries stay in System Settings until "
    "you remove them by hand.":
        "Записи в «Микрофон» и «Универсальный доступ» останутся в системных "
        "настройках, пока не уберёшь их вручную.",

    # --- setup guide ---------------------------------------------------------
    "Welcome to ": "Первый запуск — ",
    "Set up ": "Настройка ",
    "macOS needs to grant two permissions before dictation can work. "
    "This takes about a minute.":
        "Прежде чем диктовка заработает, macOS должна выдать два доступа. Это "
        "примерно минута.",
    "Allow microphone access": "Разреши доступ к микрофону",
    "So Vexflow can hear you.": "Чтобы Vexflow тебя слышал.",
    "Allow accessibility access": "Разреши универсальный доступ",
    "So Vexflow can see the hotkey and paste the text.":
        "Чтобы Vexflow видел горячую клавишу и вставлял текст.",
    "macOS applies the accessibility grant only at launch.":
        "macOS подхватывает выданный доступ только при запуске.",
    "Allow": "Разрешить",
    "Restart": "Перезапустить",
    "Step {} of {}": "Шаг {} из {}",
    "Permissions are set.": "Доступы выданы.",
    "Denied — turn it on in System Settings":
        "Запрещён — включи в системных настройках",
    "Requested on first use": "Спросят при первом обращении",
    "Hotkeys are live": "Горячие клавиши работают",
    "Restart to activate the hotkey": "Перезапусти, чтобы клавиша заработала",
    "Finish step 2 first": "Сначала закончи шаг 2",
    "Close": "Закрыть",
    "Add your API key": "Добавить ключ",

    # --- engine notices in the menu ------------------------------------------
    "Restarted after a dead microphone — please dictate again":
        "Перезапустился после отказа микрофона — продиктуй ещё раз",
    "No Accessibility permission — hotkeys are dead":
        "Нет универсального доступа — горячие клавиши мертвы",
    "Microphone still dead after a restart — check System Settings > Sound":
        "Микрофон мёртв и после перезапуска — посмотри «Настройки» → «Звук»",
    "Microphone is dead — restart Vexflow manually":
        "Микрофон мёртв — перезапусти Vexflow вручную",
    "Microphone did not open — check input and permissions":
        "Микрофон не открылся — проверь вход и доступы",
    "Microphone is dead — restarting": "Микрофон мёртв — перезапускаюсь",
    "Microphone rebuilt mid-recording — the start may be lost":
        "Микрофон пересоздан посреди записи — начало могло потеряться",
    "Deepgram connection dropped — text lost":
        "Связь с Deepgram оборвалась — текст потерян",
    "Deepgram unreachable — check your connection":
        "Deepgram недоступен — проверь связь",
    "Copied — press Cmd-V to paste": "Скопировано — вставь через Cmd-V",
    "duration limit": "предел длительности",
    "Deepgram connection dropped": "связь с Deepgram оборвалась",
    "Stopped ({}) — text is on the clipboard, press Cmd-V":
        "Остановлено ({}) — текст в буфере обмена, вставь через Cmd-V",

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
        "Поставляется «как есть», без гарантий любого рода, и используется целиком "
        "на твой собственный риск.\n\n"
        "{app} — клиент к внешним сервисам, которые ты выбираешь сам, где у тебя свои "
        "аккаунты и своя оплата. Эти сервисы не управляются {vendor} и не подотчётны "
        "ей: их условия, цены и обращение с твоими данными — дело между тобой и ними, "
        "и здесь ничего не говорится от их имени. Всё, что потрачено по твоим ключам, "
        "— твоё, и никаких обещаний насчёт сохранности введённого ключа не даётся.\n\n"
        "Остальные названия принадлежат своим владельцам и упомянуты только чтобы "
        "обозначить, с чем это работает. Аффилированности и одобрения нет.",

    # --- languages -----------------------------------------------------------
    "English": "Английский",
    "Multilingual (code-switching)": "Мультиязычный (переключение на лету)",
    "Spanish": "Испанский",
    "German": "Немецкий",
    "French": "Французский",
    "Portuguese": "Португальский",
    "Italian": "Итальянский",
    "Dutch": "Нидерландский",
    "Russian": "Русский",
    "Ukrainian": "Украинский",
    "Polish": "Польский",
    "Turkish": "Турецкий",
    "Hindi": "Хинди",
    "Japanese": "Японский",

    # --- hotkeys -------------------------------------------------------------
    # Command, Option, Control and Shift stay: they are what is printed on the keys.
    "Right Command": "Правый Command",
    "Right Option": "Правый Option",
    "Left Command": "Левый Command",
    "Left Option": "Левый Option",
    "Left Control": "Левый Control",
    "Right Control": "Правый Control",
    "Left Shift": "Левый Shift",
    "Right Shift": "Правый Shift",
    "Control + Option": "Control + Option",
    "Control + Shift": "Control + Shift",
    "Command + Option": "Command + Option",
    "Option + Shift": "Option + Shift",
    "Control + Option + Shift": "Control + Option + Shift",

    # --- cleanup models ------------------------------------------------------
    # Model names are proper nouns; only what they are good for is translated.
    "Haiku 4.5 — fastest, cheapest": "Haiku 4.5 — самая быстрая и дешёвая",
    "Sonnet 5 — balanced": "Sonnet 5 — золотая середина",
    "Opus 5 — most accurate": "Opus 5 — самая точная",
    "GPT-5.6 Luna — fastest, cheapest": "GPT-5.6 Luna — самая быстрая и дешёвая",
    "GPT-5.6 Terra — balanced": "GPT-5.6 Terra — золотая середина",
    "GPT-5.6 Sol — most accurate": "GPT-5.6 Sol — самая точная",
}
