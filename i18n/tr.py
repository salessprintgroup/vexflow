"""Turkish interface strings.

The key is the English source string, so an entry that is missing here falls back to
English rather than to a bare identifier. Adding or fixing a language: see README.md
in this directory.
"""
TABLE = {
    # --- menu bar ------------------------------------------------------------
    "Ready": "Hazır",
    "Recording…": "Kaydediliyor…",
    "Paused": "Duraklatıldı",
    "Stop recording": "Kaydı durdur",
    "Pause": "Duraklat",
    "Resume": "Sürdür",
    "Language": "Tanıma dili",
    "LLM Cleanup": "LLM temizliği",
    "Clean up transcripts": "Dökümü temizle",
    "Setup Guide…": "İlk adımlar…",
    "Settings…": "Ayarlar…",
    "Open log": "Günlüğü aç",
    "Vexflow on GitHub": "GitHub'da Vexflow",
    "Built by ": "Yapımcı: ",
    "Quit Vexflow": "Çık",
    "About ": "Hakkında: ",
    "Hide ": "Gizle: ",
    "Quit ": "Çık: ",
    "Edit": "Düzen",
    "Undo": "Geri al",
    "Redo": "Yinele",
    "Cut": "Kes",
    "Copy": "Kopyala",
    "Paste": "Yapıştır",
    "Select All": "Tümünü seç",
    "Hold ": "Basılı tut: ",
    "tap ": "dokun: ",
    "middle mouse button": "farenin orta düğmesi",

    # --- key states, menu bar ------------------------------------------------
    "No Deepgram key — open Settings": "Deepgram anahtarı yok — ayarları aç",
    "Checking your Deepgram key…": "Deepgram anahtarın denetleniyor…",
    "Deepgram rejected your key — open Settings":
        "Deepgram anahtarı kabul etmedi — ayarları aç",
    "Can't reach Deepgram — check your connection":
        "Deepgram'a ulaşılamıyor — bağlantını denetle",
    "Balance: {}": "Bakiye: {}",
    "Balance: {} — running low": "Bakiye: {} — tükeniyor",
    "Balance: …": "Bakiye: …",
    "Balance: checking…": "Bakiye: denetleniyor…",
    "Balance key rejected — open Settings":
        "Bakiye anahtarı kabul edilmedi — ayarları aç",
    "Balance: can't reach Deepgram": "Bakiye: Deepgram'a ulaşılamıyor",
    " — no key": " — anahtar yok",
    " — checking the key…": " — anahtar denetleniyor…",
    " — key rejected": " — anahtar kabul edilmedi",
    " — could not check the key": " — anahtar denetlenemedi",

    # --- macOS permission dialog ---------------------------------------------
    # Shown by macOS itself, so it follows the system language, not the setting.
    "Vexflow sends your speech to Deepgram with your own API key so it can be "
    "typed as text.":
        "Vexflow, konuşmanı metne dönüştürmek için kendi API anahtarınla Deepgram'a gönderir.",

    # --- settings window: frame ----------------------------------------------
    "{} Settings": "{} ayarları",
    "Interface language": "Arayüz dili",
    "Keys": "Anahtarlar",
    "Dictation": "Dikte",
    "Cleanup": "Temizlik",
    "Permissions": "İzinler",
    "Done": "Tamam",

    # --- settings: keys ------------------------------------------------------
    "Speech to text": "Konuşma tanıma",
    "Audio goes from this Mac straight to Deepgram using your own key. "
    "Fields marked * are required.":
        "Ses bu Mac'ten doğrudan Deepgram'a, senin kendi anahtarınla gider. "
        "Yıldızlı alanlar zorunludur.",
    "Transcript cleanup": "Döküm temizliği",
    "Optional. A small model fixes punctuation, false starts and mangled "
    "names. Without a key you still get the raw transcript.":
        "İsteğe bağlı. Küçük bir model noktalamayı, yanlış başlangıçları ve "
        "yamultulmuş isimleri düzeltir. Anahtar olmadan da ham döküm elinde kalır.",
    "Deepgram key": "Deepgram anahtarı",
    "Balance key": "Bakiye anahtarı",
    "Anthropic key": "Anthropic anahtarı",
    "OpenAI key": "OpenAI anahtarı",
    "Save": "Kaydet",
    "Get key": "Edin",
    "paste key": "anahtarı yapıştır",
    "paste a new key to replace": "değiştirmek için yeni anahtar yapıştır",
    "{} characters — press Save": "{} karakter — Kaydet'e bas",

    # --- settings: key statuses ----------------------------------------------
    "Not set": "Ayarlanmadı",
    "Saved in Keychain": "Anahtar Zinciri'ne kaydedildi",
    "Required — dictation does not work without it":
        "Zorunlu — bu olmadan dikte çalışmaz",
    "Checking with Deepgram…": "Deepgram'da denetleniyor…",
    "Verified — Deepgram accepted this key":
        "Doğrulandı — Deepgram bu anahtarı kabul etti",
    "Deepgram rejected this key. Check you copied all of it.":
        "Deepgram bu anahtarı kabul etmedi. Tamamını kopyaladığından emin ol.",
    "Saved, but Deepgram could not be reached to check it":
        "Kaydedildi, ama denetlemek için Deepgram'a ulaşılamadı",
    "Deepgram rejected this key, or it has no billing:read scope":
        "Deepgram bu anahtarı kabul etmedi ya da billing:read kapsamı yok",
    "Checking with {}…": "{} üzerinde denetleniyor…",
    "Verified — {} accepted this key": "Doğrulandı — {} bu anahtarı kabul etti",
    "{} rejected this key": "{} bu anahtarı kabul etmedi",
    "{} rejected this key: {}": "{} bu anahtarı kabul etmedi: {}",
    "Saved, but {} could not be reached to check it":
        "Kaydedildi, ama denetlemek için {} adresine ulaşılamadı",

    # --- settings: help popovers ---------------------------------------------
    "Open the console": "Konsolu aç",
    "The one key Vexflow cannot work without. Your microphone audio goes from this "
    "Mac to the speech-to-text service under this key and comes back as text, with "
    "no server of ours in between. Create a key in your own account there and paste "
    "the whole string. It is kept in your login Keychain, never in a file — and, "
    "like any credential on any machine, it is yours to look after.":
        "Vexflow'un onsuz çalışamadığı tek anahtar. Mikrofon sesin bu Mac'ten bu "
        "anahtarla konuşma tanıma servisine gider ve metin olarak döner; arada bize "
        "ait hiçbir sunucu yoktur. Oradaki kendi hesabında bir anahtar oluştur ve "
        "dizginin tamamını yapıştır. Anahtar giriş Anahtar Zinciri'nde durur, hiçbir "
        "zaman bir dosyada değil — ve her makinedeki her kimlik bilgisi gibi, ona "
        "göz kulak olmak sana kalır.",
    "Optional, and a second key on purpose. Reading your account balance needs the "
    "billing:read scope, which the key above has no business holding — one key that "
    "spends and one that reads are worth keeping apart. Create a key with "
    "billing:read only and the menu bar shows the balance the service reports.":
        "İsteğe bağlı ve bilerek ikinci bir anahtar. Hesap bakiyeni okumak "
        "billing:read kapsamını ister; yukarıdaki anahtarın bunu taşımak için bir "
        "nedeni yok: harcayan anahtarla hesabı okuyan anahtarı ayrı tutmakta fayda "
        "var. Yalnızca billing:read olan bir anahtar oluştur, menü çubuğu servisin "
        "bildirdiği bakiyeyi göstersin.",
    "Optional. Drives the cleanup pass that repairs punctuation, false starts and "
    "mangled names. Only the transcript is sent, never the audio, and what the "
    "service does with it is between you and them. The key is checked the moment "
    "you save it, so a wrong one says so here instead of quietly doing nothing.":
        "İsteğe bağlı. Noktalamayı, yanlış başlangıçları ve yamultulmuş isimleri "
        "onaran temizlik geçişini besler. Yalnızca döküm gönderilir, ses asla; "
        "servisin onunla ne yaptığı seninle onun arasındadır. Anahtar kaydettiğin "
        "anda denetlenir, böylece yanlış olan sessizce hiçbir şey yapmak yerine "
        "burada kendini belli eder.",
    "Optional, and an alternative to the key above rather than an addition — "
    "cleanup uses whichever provider is selected on the Cleanup tab. That tab can "
    "also point this key at any OpenAI-compatible endpoint, including a model "
    "running on your own machine.":
        "İsteğe bağlı ve yukarıdaki anahtara ek olmaktan çok onun yerine geçer: "
        "temizlik, Temizlik sekmesinde seçili olan sağlayıcıyı kullanır. Aynı "
        "sekmede bu anahtarı OpenAI uyumlu herhangi bir adrese, kendi makinende "
        "çalışan bir model dahil, yönlendirebilirsin.",

    # --- settings: dictation -------------------------------------------------
    "Recognition language": "Tanıma dili",
    "A single language recognises better than Multilingual. Choose "
    "Multilingual only if you switch languages inside one sentence.":
        "Tek bir dil, çok dilli kipten daha iyi tanınır. Çok dilliyi yalnızca bir "
        "cümlenin içinde dil değiştiriyorsan seç.",
    "Push to talk": "Basılı tutma",
    "Hold, speak, release.": "Basılı tut, konuş, bırak.",
    "Hands-free toggle": "Anahtarlama",
    "Off": "Kapalı",
    "Tap once to start, tap again to stop.":
        "Bir dokunuş başlatır, bir dokunuş daha bitirir.",
    "Combined entries fire only while both keys are held — safer when the "
    "free single keys are ones you type with.":
        "Bileşimler yalnızca iki tuş da basılıyken çalışır. Boştaki tek tuşlar "
        "yazarken kullandıkların olduğunda işe yarar.",
    "Also toggle with the middle mouse button":
        "Farenin orta düğmesiyle de anahtarla",
    "Play a sound when recording starts and stops":
        "Kaydın başında ve sonunda ses çal",
    "Paste automatically (off: copy to clipboard only)":
        "Kendiliğinden yapıştır (kapalı: yalnızca kopyala)",

    # --- settings: cleanup ---------------------------------------------------
    "Clean up transcripts with an LLM": "Dökümü bir LLM ile temizle",
    "Provider": "Sağlayıcı",
    "Model": "Model",
    "No {} key yet — add one on the Keys tab.":
        "Henüz {} anahtarı yok — Anahtarlar sekmesinden ekle.",
    "{} rejected the key — check it on the Keys tab.":
        "{} anahtarı kabul etmedi — Anahtarlar sekmesinden denetle.",
    "Your vocabulary": "Kendi sözlüğün",
    "Edit vocabulary…": "Sözlüğü aç…",
    "Names and jargon the recogniser keeps getting wrong. One per line, "
    "kept on this Mac.":
        "Tanımanın sürekli yanlış anladığı isimler ve terimler. Her satıra bir "
        "tane; dosya bu Mac'te kalır.",
    "Advanced": "Gelişmiş",
    "Endpoint": "Adres",
    "Leave as-is for the vendor's own API, or point it at any "
    "OpenAI-compatible endpoint.":
        "Sağlayıcının kendi API'si için olduğu gibi bırak ya da OpenAI uyumlu "
        "herhangi bir adrese yönlendir.",

    # --- settings: permissions -----------------------------------------------
    "macOS asks for these once. Vexflow cannot record or type without them.":
        "macOS bunları bir kez sorar. Bunlar olmadan Vexflow ne kaydedebilir ne "
        "yazabilir.",
    "Microphone": "Mikrofon",
    "Lets Vexflow hear you.": "Vexflow seni duysun diye.",
    "Accessibility": "Erişilebilirlik",
    "Lets Vexflow see the hotkey and paste into the app you are using. "
    "Granting it takes effect only after Vexflow restarts.":
        "Vexflow kısayolu görsün ve kullandığın uygulamaya yapıştırsın diye. "
        "Verildikten sonra ancak Vexflow yeniden başlayınca geçerli olur.",
    "Granted": "Verildi",
    "Not granted": "Verilmedi",
    "Not requested yet": "Henüz istenmedi",
    "Asked on first use": "İlk kullanımda sorulur",
    "Open Settings": "Ayarları aç",
    "Re-check": "Yeniden denetle",
    "Restart Vexflow": "Vexflow'u yeniden başlat",
    "Keep a diagnostic log": "Tanılama günlüğü tut",
    "Off, so nothing about your dictation reaches the disk. Turn it on to "
    "chase a problem and off again afterwards — switching it off deletes the "
    "file. It records timings and errors, never what you said.":
        "Kapalı, böylece diktenle ilgili hiçbir şey diske ulaşmaz. Bir sorunun "
        "peşine düşerken aç, sonra yine kapat — kapatmak dosyayı siler. Süreleri ve "
        "hataları yazar, söylediklerini asla.",
    "Transcript debug logging is ON for this run — dictated text is being "
    "written to the log. Restart without VEXFLOW_DEBUG_TRANSCRIPT to stop it.":
        "Bu çalıştırmada döküm hata ayıklama günlüğü AÇIK — dikte edilen metin "
        "günlüğe yazılıyor. Durdurmak için VEXFLOW_DEBUG_TRANSCRIPT olmadan yeniden "
        "başlat.",
    "VEXFLOW_DEBUG_TRANSCRIPT is set for this run: switching the log on would "
    "write what you dictate into it.":
        "Bu çalıştırmada VEXFLOW_DEBUG_TRANSCRIPT tanımlı: günlüğü açmak dikte "
        "ettiklerini içine yazar.",
    "Remove Vexflow from this Mac…": "Vexflow'u bu Mac'ten kaldır…",

    # --- uninstall dialogs ---------------------------------------------------
    "Remove Vexflow from this Mac?": "Vexflow bu Mac'ten kaldırılsın mı?",
    "This quits Vexflow, removes it from your login items and deletes the "
    "app. Your API keys and settings are kept unless you choose otherwise.":
        "Vexflow kapanır, giriş öğelerinden çıkar ve uygulama silinir. Başka türlü "
        "seçmedikçe anahtarların ve ayarların kalır.",
    "Remove": "Kaldır",
    "Cancel": "Vazgeç",
    "Remove and Delete My Keys": "Anahtarlarla birlikte kaldır",
    "Vexflow has been removed.": "Vexflow kaldırıldı.",
    "Login item removed, but deleting the app was cancelled.":
        "Giriş öğelerinden çıkarıldı, ama uygulamayı silmekten vazgeçildi.",
    "Login item removed, but the app could not be deleted.":
        "Giriş öğelerinden çıkarıldı, ama uygulama silinemedi.",
    "Login item removed; deleting the app failed: ":
        "Giriş öğelerinden çıkarıldı; uygulamayı silme başarısız oldu: ",
    "Microphone and Accessibility entries stay in System Settings until "
    "you remove them by hand.":
        "Mikrofon ve Erişilebilirlik kayıtları, sen elle kaldırana kadar Sistem "
        "Ayarları'nda kalır.",

    # --- setup guide ---------------------------------------------------------
    "Welcome to ": "Hoş geldin: ",
    "Set up ": "Kurulum: ",
    "macOS needs to grant two permissions before dictation can work. "
    "This takes about a minute.":
        "Dikte çalışmadan önce macOS'in iki izin vermesi gerekir. Bu yaklaşık bir "
        "dakika sürer.",
    "Allow microphone access": "Mikrofon erişimine izin ver",
    "So Vexflow can hear you.": "Vexflow seni duysun diye.",
    "Allow accessibility access": "Erişilebilirlik erişimine izin ver",
    "So Vexflow can see the hotkey and paste the text.":
        "Vexflow kısayolu görsün ve metni yapıştırsın diye.",
    "macOS applies the accessibility grant only at launch.":
        "macOS bu izni yalnızca açılışta uygular.",
    "Allow": "İzin ver",
    "Restart": "Yeniden başlat",
    "Step {} of {}": "Adım {} / {}",
    "Permissions are set.": "İzinler verildi.",
    "Denied — turn it on in System Settings":
        "Reddedildi — Sistem Ayarları'ndan aç",
    "Requested on first use": "İlk kullanımda sorulur",
    "Hotkeys are live": "Kısayollar çalışıyor",
    "Restart to activate the hotkey": "Kısayolun çalışması için yeniden başlat",
    "Finish step 2 first": "Önce 2. adımı bitir",
    "Close": "Kapat",
    "Add your API key": "Anahtar ekle",

    # --- engine notices in the menu ------------------------------------------
    "Restarted after a dead microphone — please dictate again":
        "Ölü mikrofondan sonra yeniden başladı — yeniden dikte et",
    "No Accessibility permission — hotkeys are dead":
        "Erişilebilirlik izni yok — kısayollar ölü",
    "Microphone still dead after a restart — check System Settings > Sound":
        "Mikrofon yeniden başlatmadan sonra da ölü — Sistem Ayarları > Ses'e bak",
    "Microphone is dead — restart Vexflow manually":
        "Mikrofon ölü — Vexflow'u elle yeniden başlat",
    "Microphone did not open — check input and permissions":
        "Mikrofon açılmadı — girişi ve izinleri denetle",
    "Microphone is dead — restarting": "Mikrofon ölü — yeniden başlatılıyor",
    "Microphone rebuilt mid-recording — the start may be lost":
        "Mikrofon kayıt ortasında yeniden kuruldu — baş taraf kaybolmuş olabilir",
    "Deepgram connection dropped — text lost":
        "Deepgram bağlantısı koptu — metin kayboldu",
    "Deepgram unreachable — check your connection":
        "Deepgram'a ulaşılamıyor — bağlantını denetle",
    "Copied — press Cmd-V to paste": "Kopyalandı — Cmd-V ile yapıştır",
    "duration limit": "süre sınırı",
    "Deepgram connection dropped": "Deepgram bağlantısı koptu",
    "Stopped ({}) — text is on the clipboard, press Cmd-V":
        "Durdu ({}) — metin panoda, Cmd-V'ye bas",

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
        "Olduğu gibi sunulur, hiçbir türden garanti verilmez ve tamamen kendi "
        "sorumluluğunda kullanılır.\n\n"
        "{app}, senin seçtiğin, hesabının bulunduğu ve doğrudan ödeme yaptığın dış "
        "servisler için bir istemcidir. Bu servisler {vendor} tarafından "
        "işletilmez ve ona karşı sorumlu değildir: koşulları, fiyatları ve "
        "verilerini nasıl ele aldıkları seninle onlar arasındadır; burada onların "
        "adına hiçbir şey söylenmez. Anahtarlarınla yapılan harcamalar sana aittir "
        "ve girdiğin hiçbir anahtarın güvenliği konusunda taahhüt verilmez.\n\n"
        "Diğer adlar sahiplerine aittir ve yalnızca bunun neye bağlandığını "
        "belirtmek için görünür. Herhangi bir bağlantı ya da onay iddia edilmez.",

    # --- languages -----------------------------------------------------------
    "English": "İngilizce",
    "Multilingual (code-switching)": "Çok dilli (anlık geçiş)",
    "Spanish": "İspanyolca",
    "German": "Almanca",
    "French": "Fransızca",
    "Portuguese": "Portekizce",
    "Italian": "İtalyanca",
    "Dutch": "Felemenkçe",
    "Russian": "Rusça",
    "Ukrainian": "Ukraynaca",
    "Polish": "Lehçe",
    "Turkish": "Türkçe",
    "Hindi": "Hintçe",
    "Japanese": "Japonca",

    # --- hotkeys -------------------------------------------------------------
    # Command, Option, Control and Shift stay: they are what is printed on the keys.
    "Right Command": "Sağ Command",
    "Right Option": "Sağ Option",
    "Left Command": "Sol Command",
    "Left Option": "Sol Option",
    "Left Control": "Sol Control",
    "Right Control": "Sağ Control",
    "Left Shift": "Sol Shift",
    "Right Shift": "Sağ Shift",
    "Control + Option": "Control + Option",
    "Control + Shift": "Control + Shift",
    "Command + Option": "Command + Option",
    "Option + Shift": "Option + Shift",
    "Control + Option + Shift": "Control + Option + Shift",

    # --- cleanup models ------------------------------------------------------
    # Model names are proper nouns; only what they are good for is translated.
    "Haiku 4.5 — fastest, cheapest": "Haiku 4.5 — en hızlı, en ucuz",
    "Sonnet 5 — balanced": "Sonnet 5 — dengeli",
    "Opus 5 — most accurate": "Opus 5 — en isabetli",
    "GPT-5.6 Luna — fastest, cheapest": "GPT-5.6 Luna — en hızlı, en ucuz",
    "GPT-5.6 Terra — balanced": "GPT-5.6 Terra — dengeli",
    "GPT-5.6 Sol — most accurate": "GPT-5.6 Sol — en isabetli",
}
