"""Ukrainian interface strings.

The key is the English source string, so an entry that is missing here falls back to
English rather than to a bare identifier. Adding or fixing a language: see README.md
in this directory.
"""
TABLE = {
    # --- menu bar ------------------------------------------------------------
    "Ready": "Готовий",
    "Recording…": "Запис…",
    "Paused": "На паузі",
    "Stop recording": "Зупинити запис",
    "Pause": "Пауза",
    "Resume": "Продовжити",
    "Language": "Мова розпізнавання",
    "LLM Cleanup": "Очищення LLM",
    "Clean up transcripts": "Чистити розшифровку",
    "Setup Guide…": "Перший запуск…",
    "Settings…": "Налаштування…",
    "Open log": "Відкрити журнал",
    "Vexflow on GitHub": "Vexflow на GitHub",
    "Built by ": "Зроблено в ",
    "Quit Vexflow": "Вийти",
    "About ": "Про програму ",
    "Hide ": "Сховати ",
    "Quit ": "Вийти з ",
    "Edit": "Редагування",
    "Undo": "Скасувати",
    "Redo": "Повторити",
    "Cut": "Вирізати",
    "Copy": "Копіювати",
    "Paste": "Вставити",
    "Select All": "Вибрати все",
    "Hold ": "Утримуй ",
    "tap ": "натисни ",
    "middle mouse button": "середня кнопка миші",

    # --- key states, menu bar ------------------------------------------------
    "No Deepgram key — open Settings": "Немає ключа Deepgram — відкрий налаштування",
    "Checking your Deepgram key…": "Перевіряю ключ Deepgram…",
    "Deepgram rejected your key — open Settings":
        "Deepgram не прийняв ключ — відкрий налаштування",
    "Can't reach Deepgram — check your connection":
        "Deepgram недоступний — перевір зв'язок",
    "Balance: {}": "Баланс: {}",
    "Balance: {} — running low": "Баланс: {} — добігає кінця",
    "Balance: …": "Баланс: …",
    "Balance: checking…": "Баланс: перевіряю…",
    "Balance key rejected — open Settings":
        "Ключ балансу не прийнято — відкрий налаштування",
    "Balance: can't reach Deepgram": "Баланс: Deepgram недоступний",
    " — no key": " — немає ключа",
    " — checking the key…": " — перевіряю ключ…",
    " — key rejected": " — ключ не прийнято",
    " — could not check the key": " — не вдалося перевірити ключ",

    # --- macOS permission dialog ---------------------------------------------
    # Shown by macOS itself, so it follows the system language, not the setting.
    "Vexflow sends your speech to Deepgram with your own API key so it can be "
    "typed as text.":
        "Vexflow надсилає вашу мову в Deepgram за вашим власним ключем, щоб повернути її текстом.",

    # --- settings window: frame ----------------------------------------------
    "{} Settings": "{} — налаштування",
    "Interface language": "Мова інтерфейсу",
    "Keys": "Ключі",
    "Dictation": "Диктування",
    "Cleanup": "Очищення",
    "Permissions": "Доступи",
    "Done": "Готово",

    # --- settings: keys ------------------------------------------------------
    "Speech to text": "Розпізнавання мовлення",
    "Audio goes from this Mac straight to Deepgram using your own key. "
    "Fields marked * are required.":
        "Звук іде з цього Mac просто в Deepgram за твоїм ключем. "
        "Поля із зірочкою обов'язкові.",
    "Transcript cleanup": "Очищення розшифровки",
    "Optional. A small model fixes punctuation, false starts and mangled "
    "names. Without a key you still get the raw transcript.":
        "За бажанням. Невелика модель виправляє пунктуацію, обмовки та перекручені "
        "імена. Без ключа лишиться сира розшифровка.",
    "Deepgram key": "Ключ Deepgram",
    "Balance key": "Ключ для балансу",
    "Anthropic key": "Ключ Anthropic",
    "OpenAI key": "Ключ OpenAI",
    "Save": "Зберегти",
    "Get key": "Отримати",
    "paste key": "встав ключ",
    "paste a new key to replace": "встав новий ключ, щоб замінити",
    "{} characters — press Save": "символів: {} — натисни «Зберегти»",

    # --- settings: key statuses ----------------------------------------------
    "Not set": "Не задано",
    "Saved in Keychain": "Збережено у в'язці ключів",
    "Required — dictation does not work without it":
        "Обов'язковий — без нього диктування не працює",
    "Checking with Deepgram…": "Перевіряю в Deepgram…",
    "Verified — Deepgram accepted this key": "Перевірено — Deepgram прийняв ключ",
    "Deepgram rejected this key. Check you copied all of it.":
        "Deepgram не прийняв ключ. Перевір, чи скопіював його повністю.",
    "Saved, but Deepgram could not be reached to check it":
        "Збережено, але перевірити не вдалося — Deepgram недоступний",
    "Deepgram rejected this key, or it has no billing:read scope":
        "Deepgram не прийняв ключ, або в нього немає права billing:read",
    "Checking with {}…": "Перевіряю в {}…",
    "Verified — {} accepted this key": "Перевірено — {} прийняв ключ",
    "{} rejected this key": "{} не прийняв ключ",
    "{} rejected this key: {}": "{} не прийняв ключ: {}",
    "Saved, but {} could not be reached to check it":
        "Збережено, але перевірити не вдалося — {} недоступний",

    # --- settings: help popovers ---------------------------------------------
    "Open the console": "Відкрити консоль",
    "The one key Vexflow cannot work without. Your microphone audio goes from this "
    "Mac to the speech-to-text service under this key and comes back as text, with "
    "no server of ours in between. Create a key in your own account there and paste "
    "the whole string. It is kept in your login Keychain, never in a file — and, "
    "like any credential on any machine, it is yours to look after.":
        "Єдиний ключ, без якого Vexflow не працює. Звук із мікрофона йде з цього Mac "
        "у сервіс розпізнавання за цим ключем і повертається текстом; нашого сервера "
        "в цьому ланцюжку немає. Створи ключ у власному акаунті там і встав рядок "
        "повністю. Він лежить у в'язці ключів, не у файлі — і, як будь-який ключ на "
        "будь-якій машині, лишається твоєю турботою.",
    "Optional, and a second key on purpose. Reading your account balance needs the "
    "billing:read scope, which the key above has no business holding — one key that "
    "spends and one that reads are worth keeping apart. Create a key with "
    "billing:read only and the menu bar shows the balance the service reports.":
        "За бажанням, і це навмисно другий ключ. Щоб читати баланс, потрібне право "
        "billing:read, якого в ключа вище бути не повинно: ключ, який витрачає, і "
        "ключ, який читає рахунок, краще тримати окремо. Створи ключ лише з "
        "billing:read — і в рядку меню з'явиться баланс, який віддає сервіс.",
    "Optional. Drives the cleanup pass that repairs punctuation, false starts and "
    "mangled names. Only the transcript is sent, never the audio, and what the "
    "service does with it is between you and them. The key is checked the moment "
    "you save it, so a wrong one says so here instead of quietly doing nothing.":
        "За бажанням. Живить прохід очищення, який виправляє пунктуацію, обмовки та "
        "перекручені імена. Іде лише текст розшифровки, звук — ніколи; що сервіс із "
        "ним робить, вирішуєте ти і він. Ключ перевіряється одразу під час "
        "збереження, тому про хибний буде сказано тут же.",
    "Optional, and an alternative to the key above rather than an addition — "
    "cleanup uses whichever provider is selected on the Cleanup tab. That tab can "
    "also point this key at any OpenAI-compatible endpoint, including a model "
    "running on your own machine.":
        "За бажанням, і це заміна ключу вище, а не доповнення: очищення працює через "
        "того постачальника, який вибраний на вкладці «Очищення». Там же цей ключ "
        "можна спрямувати на будь-яку адресу, сумісну з OpenAI, включно з моделлю на "
        "твоїй машині.",

    # --- settings: dictation -------------------------------------------------
    "Recognition language": "Мова розпізнавання",
    "A single language recognises better than Multilingual. Choose "
    "Multilingual only if you switch languages inside one sentence.":
        "Одна вибрана мова розпізнається точніше, ніж багатомовний режим. Бери "
        "багатомовний, лише якщо перемикаєш мови всередині фрази.",
    "Push to talk": "Утримання",
    "Hold, speak, release.": "Затисни, говори, відпусти.",
    "Hands-free toggle": "Перемикач",
    "Off": "Вимк",
    "Tap once to start, tap again to stop.":
        "Натисни — почнеться запис, натисни ще раз — завершиться.",
    "Combined entries fire only while both keys are held — safer when the "
    "free single keys are ones you type with.":
        "Сполучення спрацьовують, лише поки затиснуті обидві клавіші. Це рятує, коли "
        "всі вільні одиночні клавіші — ті, якими ти друкуєш.",
    "Also toggle with the middle mouse button":
        "Перемикати ще й середньою кнопкою миші",
    "Play a sound when recording starts and stops":
        "Звук на початку і в кінці запису",
    "Paste automatically (off: copy to clipboard only)":
        "Вставляти одразу (вимк — лише копіювати в буфер)",

    # --- settings: cleanup ---------------------------------------------------
    "Clean up transcripts with an LLM": "Чистити розшифровку через LLM",
    "Provider": "Постачальник",
    "Model": "Модель",
    "No {} key yet — add one on the Keys tab.":
        "Ключа {} ще немає — додай його на вкладці «Ключі».",
    "{} rejected the key — check it on the Keys tab.":
        "{} не прийняв ключ — перевір його на вкладці «Ключі».",
    "Your vocabulary": "Власний словник",
    "Edit vocabulary…": "Відкрити словник…",
    "Names and jargon the recogniser keeps getting wrong. One per line, "
    "kept on this Mac.":
        "Імена і жаргон, які розпізнавання стабільно перекручує. По одному в рядку, "
        "файл лишається на цьому Mac.",
    "Advanced": "Для досвідчених",
    "Endpoint": "Адреса",
    "Leave as-is for the vendor's own API, or point it at any "
    "OpenAI-compatible endpoint.":
        "Залиш як є для штатного API постачальника або вкажи будь-яку адресу, "
        "сумісну з OpenAI.",

    # --- settings: permissions -----------------------------------------------
    "macOS asks for these once. Vexflow cannot record or type without them.":
        "macOS запитає про них один раз. Без них Vexflow не запише і не надрукує.",
    "Microphone": "Мікрофон",
    "Lets Vexflow hear you.": "Щоб Vexflow тебе чув.",
    "Accessibility": "Універсальний доступ",
    "Lets Vexflow see the hotkey and paste into the app you are using. "
    "Granting it takes effect only after Vexflow restarts.":
        "Щоб Vexflow бачив гарячу клавішу і вставляв текст у відкриту програму. "
        "Виданий доступ підхопиться лише після перезапуску Vexflow.",
    "Granted": "Видано",
    "Not granted": "Не видано",
    "Not requested yet": "Ще не запитувався",
    "Asked on first use": "Запитають при першому зверненні",
    "Open Settings": "Відкрити налаштування",
    "Re-check": "Перевірити знову",
    "Restart Vexflow": "Перезапустити Vexflow",
    "Keep a diagnostic log": "Вести діагностичний журнал",
    "Off, so nothing about your dictation reaches the disk. Turn it on to "
    "chase a problem and off again afterwards — switching it off deletes the "
    "file. It records timings and errors, never what you said.":
        "Вимкнений, тому на диск про твоє диктування не потрапляє нічого. Увімкни, "
        "коли ловиш проблему, і вимкни після — вимкнення стирає файл. У журналі "
        "тайминги і помилки, сказаного там немає ніколи.",
    "Transcript debug logging is ON for this run — dictated text is being "
    "written to the log. Restart without VEXFLOW_DEBUG_TRANSCRIPT to stop it.":
        "Для цього запуску ввімкнено налагоджувальний запис розшифровок: "
        "надиктований текст пишеться в журнал. Перезапусти без "
        "VEXFLOW_DEBUG_TRANSCRIPT, щоб припинити.",
    "VEXFLOW_DEBUG_TRANSCRIPT is set for this run: switching the log on would "
    "write what you dictate into it.":
        "Для цього запуску задано VEXFLOW_DEBUG_TRANSCRIPT: якщо ввімкнути журнал, "
        "надиктоване потраплятиме в нього.",
    "Remove Vexflow from this Mac…": "Видалити Vexflow з цього Mac…",

    # --- uninstall dialogs ---------------------------------------------------
    "Remove Vexflow from this Mac?": "Видалити Vexflow з цього Mac?",
    "This quits Vexflow, removes it from your login items and deletes the "
    "app. Your API keys and settings are kept unless you choose otherwise.":
        "Vexflow закриється, піде з автозапуску, і програму буде видалено. Ключі та "
        "налаштування лишаться, якщо не вибрати інше.",
    "Remove": "Видалити",
    "Cancel": "Скасувати",
    "Remove and Delete My Keys": "Видалити разом із ключами",
    "Vexflow has been removed.": "Vexflow видалено.",
    "Login item removed, but deleting the app was cancelled.":
        "З автозапуску прибрано, але видалення програми скасовано.",
    "Login item removed, but the app could not be deleted.":
        "З автозапуску прибрано, але видалити програму не вдалося.",
    "Login item removed; deleting the app failed: ":
        "З автозапуску прибрано; видалити програму не вдалося: ",
    "Microphone and Accessibility entries stay in System Settings until "
    "you remove them by hand.":
        "Записи в «Мікрофон» та «Універсальний доступ» лишаться в системних "
        "параметрах, доки не прибереш їх вручну.",

    # --- setup guide ---------------------------------------------------------
    "Welcome to ": "Перший запуск — ",
    "Set up ": "Налаштування ",
    "macOS needs to grant two permissions before dictation can work. "
    "This takes about a minute.":
        "Перш ніж диктування запрацює, macOS має видати два доступи. Це приблизно "
        "хвилина.",
    "Allow microphone access": "Дозволь доступ до мікрофона",
    "So Vexflow can hear you.": "Щоб Vexflow тебе чув.",
    "Allow accessibility access": "Дозволь універсальний доступ",
    "So Vexflow can see the hotkey and paste the text.":
        "Щоб Vexflow бачив гарячу клавішу і вставляв текст.",
    "macOS applies the accessibility grant only at launch.":
        "macOS підхоплює виданий доступ лише під час запуску.",
    "Allow": "Дозволити",
    "Restart": "Перезапустити",
    "Step {} of {}": "Крок {} з {}",
    "Permissions are set.": "Доступи видано.",
    "Denied — turn it on in System Settings":
        "Заборонено — увімкни в системних параметрах",
    "Requested on first use": "Запитають при першому зверненні",
    "Hotkeys are live": "Гарячі клавіші працюють",
    "Restart to activate the hotkey": "Перезапусти, щоб клавіша запрацювала",
    "Finish step 2 first": "Спершу закінчи крок 2",
    "Close": "Закрити",
    "Add your API key": "Додати ключ",

    # --- engine notices in the menu ------------------------------------------
    "Restarted after a dead microphone — please dictate again":
        "Перезапустився після відмови мікрофона — продиктуй ще раз",
    "No Accessibility permission — hotkeys are dead":
        "Немає універсального доступу — гарячі клавіші мертві",
    "Microphone still dead after a restart — check System Settings > Sound":
        "Мікрофон мертвий і після перезапуску — подивись «Параметри» → «Звук»",
    "Microphone is dead — restart Vexflow manually":
        "Мікрофон мертвий — перезапусти Vexflow вручну",
    "Microphone did not open — check input and permissions":
        "Мікрофон не відкрився — перевір вхід і доступи",
    "Microphone is dead — restarting": "Мікрофон мертвий — перезапускаюся",
    "Microphone rebuilt mid-recording — the start may be lost":
        "Мікрофон перестворено посеред запису — початок міг загубитися",
    "Deepgram connection dropped — text lost":
        "Зв'язок із Deepgram обірвався — текст втрачено",
    "Deepgram unreachable — check your connection":
        "Deepgram недоступний — перевір зв'язок",
    "Copied — press Cmd-V to paste": "Скопійовано — встав через Cmd-V",
    "duration limit": "межа тривалості",
    "Deepgram connection dropped": "зв'язок із Deepgram обірвався",
    "Stopped ({}) — text is on the clipboard, press Cmd-V":
        "Зупинено ({}) — текст у буфері обміну, встав через Cmd-V",

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
        "Постачається «як є», без гарантій будь-якого роду, і використовується "
        "цілком на твій власний ризик.\n\n"
        "{app} — клієнт до зовнішніх сервісів, які ти вибираєш сам, де в тебе свої "
        "акаунти і своя оплата. Ці сервіси не керуються {vendor} і не підзвітні їй: "
        "їхні умови, ціни та поводження з твоїми даними — справа між тобою і ними, і "
        "тут нічого не говориться від їхнього імені. Усе, що витрачено за твоїми "
        "ключами, — твоє, і жодних обіцянок щодо збереження введеного ключа не "
        "дається.\n\n"
        "Інші назви належать своїм власникам і згадані лише щоб позначити, з чим це "
        "працює. Афілійованості та схвалення немає.",

    # --- languages -----------------------------------------------------------
    "English": "Англійська",
    "Multilingual (code-switching)": "Багатомовний (перемикання на льоту)",
    "Spanish": "Іспанська",
    "German": "Німецька",
    "French": "Французька",
    "Portuguese": "Португальська",
    "Italian": "Італійська",
    "Dutch": "Нідерландська",
    "Russian": "Російська",
    "Ukrainian": "Українська",
    "Polish": "Польська",
    "Turkish": "Турецька",
    "Hindi": "Гінді",
    "Japanese": "Японська",

    # --- hotkeys -------------------------------------------------------------
    # Command, Option, Control and Shift stay: they are what is printed on the keys.
    "Right Command": "Правий Command",
    "Right Option": "Правий Option",
    "Left Command": "Лівий Command",
    "Left Option": "Лівий Option",
    "Left Control": "Лівий Control",
    "Right Control": "Правий Control",
    "Left Shift": "Лівий Shift",
    "Right Shift": "Правий Shift",
    "Control + Option": "Control + Option",
    "Control + Shift": "Control + Shift",
    "Command + Option": "Command + Option",
    "Option + Shift": "Option + Shift",
    "Control + Option + Shift": "Control + Option + Shift",

    # --- cleanup models ------------------------------------------------------
    # Model names are proper nouns; only what they are good for is translated.
    "Haiku 4.5 — fastest, cheapest": "Haiku 4.5 — найшвидша й найдешевша",
    "Sonnet 5 — balanced": "Sonnet 5 — золота середина",
    "Opus 5 — most accurate": "Opus 5 — найточніша",
    "GPT-5.6 Luna — fastest, cheapest": "GPT-5.6 Luna — найшвидша й найдешевша",
    "GPT-5.6 Terra — balanced": "GPT-5.6 Terra — золота середина",
    "GPT-5.6 Sol — most accurate": "GPT-5.6 Sol — найточніша",
}
