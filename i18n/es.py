"""Spanish interface strings.

The key is the English source string, so an entry that is missing here falls back to
English rather than to a bare identifier. Adding or fixing a language: see README.md
in this directory.
"""
TABLE = {
    # --- menu bar ------------------------------------------------------------
    "Ready": "Listo",
    "Recording…": "Grabando…",
    "Paused": "En pausa",
    "Stop recording": "Detener la grabación",
    "Pause": "Pausar",
    "Resume": "Reanudar",
    "Language": "Idioma de reconocimiento",
    "LLM Cleanup": "Limpieza con LLM",
    "Clean up transcripts": "Limpiar la transcripción",
    "Setup Guide…": "Primeros pasos…",
    "Settings…": "Ajustes…",
    "Open log": "Abrir el registro",
    "Vexflow on GitHub": "Vexflow en GitHub",
    "Built by ": "Hecho por ",
    "Quit Vexflow": "Salir",
    "About ": "Acerca de ",
    "Hide ": "Ocultar ",
    "Quit ": "Salir de ",
    "Edit": "Edición",
    "Undo": "Deshacer",
    "Redo": "Rehacer",
    "Cut": "Cortar",
    "Copy": "Copiar",
    "Paste": "Pegar",
    "Select All": "Seleccionar todo",
    "Hold ": "Mantén ",
    "tap ": "pulsa ",
    "middle mouse button": "botón central del ratón",

    # --- key states, menu bar ------------------------------------------------
    "No Deepgram key — open Settings": "Sin clave de Deepgram: abre los ajustes",
    "Checking your Deepgram key…": "Comprobando tu clave de Deepgram…",
    "Deepgram rejected your key — open Settings":
        "Deepgram rechazó la clave: abre los ajustes",
    "Can't reach Deepgram — check your connection":
        "Deepgram no responde: revisa la conexión",
    "Balance: {}": "Saldo: {}",
    "Balance: {} — running low": "Saldo: {}, se está agotando",
    "Balance: …": "Saldo: …",
    "Balance: checking…": "Saldo: comprobando…",
    "Balance key rejected — open Settings":
        "Clave de saldo rechazada: abre los ajustes",
    "Balance: can't reach Deepgram": "Saldo: Deepgram no responde",
    " — no key": " — sin clave",
    " — checking the key…": " — comprobando la clave…",
    " — key rejected": " — clave rechazada",
    " — could not check the key": " — no se pudo comprobar la clave",

    # --- macOS permission dialog ---------------------------------------------
    # Shown by macOS itself, so it follows the system language, not the setting.
    "Vexflow sends your speech to Deepgram with your own API key so it can be "
    "typed as text.":
        "Vexflow envía tu voz a Deepgram con tu propia clave de API para devolverla como texto.",

    # --- settings window: frame ----------------------------------------------
    "{} Settings": "Ajustes de {}",
    "Interface language": "Idioma de la interfaz",
    "Keys": "Claves",
    "Dictation": "Dictado",
    "Cleanup": "Limpieza",
    "Permissions": "Permisos",
    "Done": "OK",

    # --- settings: keys ------------------------------------------------------
    "Speech to text": "Reconocimiento de voz",
    "Audio goes from this Mac straight to Deepgram using your own key. "
    "Fields marked * are required.":
        "El audio sale de este Mac directamente a Deepgram con tu propia clave. "
        "Los campos marcados con * son obligatorios.",
    "Transcript cleanup": "Limpieza de la transcripción",
    "Optional. A small model fixes punctuation, false starts and mangled "
    "names. Without a key you still get the raw transcript.":
        "Opcional. Un modelo pequeño corrige la puntuación, los titubeos y los "
        "nombres mal oídos. Sin clave sigues teniendo la transcripción en bruto.",
    "Deepgram key": "Clave de Deepgram",
    "Balance key": "Clave del saldo",
    "Anthropic key": "Clave de Anthropic",
    "OpenAI key": "Clave de OpenAI",
    "Save": "Guardar",
    "Get key": "Obtener",
    "paste key": "pega la clave",
    "paste a new key to replace": "pega una clave nueva para sustituirla",
    "{} characters — press Save": "{} caracteres: pulsa Guardar",

    # --- settings: key statuses ----------------------------------------------
    "Not set": "Sin definir",
    "Saved in Keychain": "Guardada en el llavero",
    "Required — dictation does not work without it":
        "Obligatoria: sin ella no hay dictado",
    "Checking with Deepgram…": "Comprobando con Deepgram…",
    "Verified — Deepgram accepted this key":
        "Verificada: Deepgram aceptó esta clave",
    "Deepgram rejected this key. Check you copied all of it.":
        "Deepgram rechazó esta clave. Comprueba que la copiaste entera.",
    "Saved, but Deepgram could not be reached to check it":
        "Guardada, pero Deepgram no respondió para comprobarla",
    "Deepgram rejected this key, or it has no billing:read scope":
        "Deepgram rechazó esta clave, o no tiene el permiso billing:read",
    "Checking with {}…": "Comprobando con {}…",
    "Verified — {} accepted this key": "Verificada: {} aceptó esta clave",
    "{} rejected this key": "{} rechazó esta clave",
    "{} rejected this key: {}": "{} rechazó esta clave: {}",
    "Saved, but {} could not be reached to check it":
        "Guardada, pero {} no respondió para comprobarla",

    # --- settings: help popovers ---------------------------------------------
    "Open the console": "Abrir la consola",
    "The one key Vexflow cannot work without. Your microphone audio goes from this "
    "Mac to the speech-to-text service under this key and comes back as text, with "
    "no server of ours in between. Create a key in your own account there and paste "
    "the whole string. It is kept in your login Keychain, never in a file — and, "
    "like any credential on any machine, it is yours to look after.":
        "La única clave sin la que Vexflow no funciona. El audio del micrófono sale "
        "de este Mac hacia el servicio de reconocimiento con esta clave y vuelve "
        "convertido en texto, sin ningún servidor nuestro por medio. Crea una clave "
        "en tu propia cuenta allí y pega la cadena entera. Se guarda en tu llavero de "
        "inicio de sesión, nunca en un archivo y, como cualquier credencial en "
        "cualquier máquina, queda bajo tu cuidado.",
    "Optional, and a second key on purpose. Reading your account balance needs the "
    "billing:read scope, which the key above has no business holding — one key that "
    "spends and one that reads are worth keeping apart. Create a key with "
    "billing:read only and the menu bar shows the balance the service reports.":
        "Opcional, y una segunda clave a propósito. Leer el saldo de tu cuenta exige "
        "el permiso billing:read, que la clave de arriba no tiene por qué llevar: una "
        "clave que gasta y otra que lee la cuenta conviene tenerlas separadas. Crea "
        "una clave solo con billing:read y la barra de menús mostrará el saldo que "
        "informa el servicio.",
    "Optional. Drives the cleanup pass that repairs punctuation, false starts and "
    "mangled names. Only the transcript is sent, never the audio, and what the "
    "service does with it is between you and them. The key is checked the moment "
    "you save it, so a wrong one says so here instead of quietly doing nothing.":
        "Opcional. Alimenta la pasada de limpieza que arregla la puntuación, los "
        "titubeos y los nombres mal oídos. Solo se envía la transcripción, nunca el "
        "audio, y lo que el servicio haga con ella es cosa entre tú y ellos. La clave "
        "se comprueba al guardarla, así que una equivocada lo dice aquí mismo en vez "
        "de quedarse callada sin hacer nada.",
    "Optional, and an alternative to the key above rather than an addition — "
    "cleanup uses whichever provider is selected on the Cleanup tab. That tab can "
    "also point this key at any OpenAI-compatible endpoint, including a model "
    "running on your own machine.":
        "Opcional, y una alternativa a la clave de arriba más que un añadido: la "
        "limpieza usa el proveedor que esté seleccionado en la pestaña Limpieza. Ahí "
        "mismo puedes apuntar esta clave a cualquier dirección compatible con OpenAI, "
        "incluido un modelo que corra en tu propia máquina.",

    # --- settings: dictation -------------------------------------------------
    "Recognition language": "Idioma de reconocimiento",
    "A single language recognises better than Multilingual. Choose "
    "Multilingual only if you switch languages inside one sentence.":
        "Un solo idioma se reconoce mejor que el modo multilingüe. Elige "
        "multilingüe solo si cambias de idioma dentro de una misma frase.",
    "Push to talk": "Mantener pulsado",
    "Hold, speak, release.": "Mantén, habla, suelta.",
    "Hands-free toggle": "Conmutador",
    "Off": "No",
    "Tap once to start, tap again to stop.":
        "Pulsa una vez para empezar y otra para parar.",
    "Combined entries fire only while both keys are held — safer when the "
    "free single keys are ones you type with.":
        "Las combinaciones actúan solo mientras mantienes las dos teclas. Va mejor "
        "cuando las teclas sueltas que quedan libres son de las que usas al escribir.",
    "Also toggle with the middle mouse button":
        "Conmutar también con el botón central del ratón",
    "Play a sound when recording starts and stops":
        "Sonido al empezar y al terminar la grabación",
    "Paste automatically (off: copy to clipboard only)":
        "Pegar automáticamente (si no, solo copiar al portapapeles)",

    # --- settings: cleanup ---------------------------------------------------
    "Clean up transcripts with an LLM": "Limpiar la transcripción con un LLM",
    "Provider": "Proveedor",
    "Model": "Modelo",
    "No {} key yet — add one on the Keys tab.":
        "Aún no hay clave de {}: añádela en la pestaña Claves.",
    "{} rejected the key — check it on the Keys tab.":
        "{} rechazó la clave: revísala en la pestaña Claves.",
    "Your vocabulary": "Tu vocabulario",
    "Edit vocabulary…": "Abrir el vocabulario…",
    "Names and jargon the recogniser keeps getting wrong. One per line, "
    "kept on this Mac.":
        "Nombres y jerga que el reconocedor sigue equivocando. Uno por línea, y el "
        "archivo se queda en este Mac.",
    "Advanced": "Avanzado",
    "Endpoint": "Dirección",
    "Leave as-is for the vendor's own API, or point it at any "
    "OpenAI-compatible endpoint.":
        "Déjalo como está para la API propia del proveedor, o apúntalo a cualquier "
        "dirección compatible con OpenAI.",

    # --- settings: permissions -----------------------------------------------
    "macOS asks for these once. Vexflow cannot record or type without them.":
        "macOS los pide una sola vez. Sin ellos Vexflow no puede grabar ni escribir.",
    "Microphone": "Micrófono",
    "Lets Vexflow hear you.": "Para que Vexflow te oiga.",
    "Accessibility": "Accesibilidad",
    "Lets Vexflow see the hotkey and paste into the app you are using. "
    "Granting it takes effect only after Vexflow restarts.":
        "Para que Vexflow vea la tecla rápida y pegue en la app que estés usando. "
        "El permiso concedido no surte efecto hasta que Vexflow se reinicia.",
    "Granted": "Concedido",
    "Not granted": "No concedido",
    "Not requested yet": "Aún no solicitado",
    "Asked on first use": "Se pide al usarlo por primera vez",
    "Open Settings": "Abrir los ajustes",
    "Re-check": "Volver a comprobar",
    "Restart Vexflow": "Reiniciar Vexflow",
    "Keep a diagnostic log": "Mantener un registro de diagnóstico",
    "Off, so nothing about your dictation reaches the disk. Turn it on to "
    "chase a problem and off again afterwards — switching it off deletes the "
    "file. It records timings and errors, never what you said.":
        "Desactivado, así que nada de tu dictado llega al disco. Actívalo para "
        "perseguir un problema y desactívalo después: al apagarlo se borra el "
        "archivo. Anota tiempos y errores, nunca lo que dijiste.",
    "Transcript debug logging is ON for this run — dictated text is being "
    "written to the log. Restart without VEXFLOW_DEBUG_TRANSCRIPT to stop it.":
        "En esta ejecución está activo el registro de depuración de transcripciones: "
        "el texto dictado se está escribiendo en el registro. Reinicia sin "
        "VEXFLOW_DEBUG_TRANSCRIPT para detenerlo.",
    "VEXFLOW_DEBUG_TRANSCRIPT is set for this run: switching the log on would "
    "write what you dictate into it.":
        "En esta ejecución está definido VEXFLOW_DEBUG_TRANSCRIPT: si activas el "
        "registro, lo que dictes acabará dentro.",
    "Remove Vexflow from this Mac…": "Eliminar Vexflow de este Mac…",

    # --- uninstall dialogs ---------------------------------------------------
    "Remove Vexflow from this Mac?": "¿Eliminar Vexflow de este Mac?",
    "This quits Vexflow, removes it from your login items and deletes the "
    "app. Your API keys and settings are kept unless you choose otherwise.":
        "Vexflow se cierra, sale de los ítems de inicio y se elimina la app. Tus "
        "claves y ajustes se conservan salvo que elijas lo contrario.",
    "Remove": "Eliminar",
    "Cancel": "Cancelar",
    "Remove and Delete My Keys": "Eliminar junto con las claves",
    "Vexflow has been removed.": "Vexflow se ha eliminado.",
    "Login item removed, but deleting the app was cancelled.":
        "Se quitó del inicio, pero se canceló la eliminación de la app.",
    "Login item removed, but the app could not be deleted.":
        "Se quitó del inicio, pero no se pudo eliminar la app.",
    "Login item removed; deleting the app failed: ":
        "Se quitó del inicio; la eliminación de la app falló: ",
    "Microphone and Accessibility entries stay in System Settings until "
    "you remove them by hand.":
        "Las entradas de Micrófono y Accesibilidad siguen en Ajustes del Sistema "
        "hasta que las quites a mano.",

    # --- setup guide ---------------------------------------------------------
    "Welcome to ": "Te damos la bienvenida a ",
    "Set up ": "Configurar ",
    "macOS needs to grant two permissions before dictation can work. "
    "This takes about a minute.":
        "macOS tiene que conceder dos permisos antes de que el dictado funcione. "
        "Es cosa de un minuto.",
    "Allow microphone access": "Permite el acceso al micrófono",
    "So Vexflow can hear you.": "Para que Vexflow te oiga.",
    "Allow accessibility access": "Permite el acceso de accesibilidad",
    "So Vexflow can see the hotkey and paste the text.":
        "Para que Vexflow vea la tecla rápida y pegue el texto.",
    "macOS applies the accessibility grant only at launch.":
        "macOS aplica ese permiso solo al arrancar.",
    "Allow": "Permitir",
    "Restart": "Reiniciar",
    "Step {} of {}": "Paso {} de {}",
    "Permissions are set.": "Permisos concedidos.",
    "Denied — turn it on in System Settings":
        "Denegado: actívalo en Ajustes del Sistema",
    "Requested on first use": "Se pide al usarlo por primera vez",
    "Hotkeys are live": "Las teclas rápidas funcionan",
    "Restart to activate the hotkey": "Reinicia para activar la tecla rápida",
    "Finish step 2 first": "Termina antes el paso 2",
    "Close": "Cerrar",
    "Add your API key": "Añadir la clave",

    # --- engine notices in the menu ------------------------------------------
    "Restarted after a dead microphone — please dictate again":
        "Reiniciado tras un micrófono muerto: dicta otra vez",
    "No Accessibility permission — hotkeys are dead":
        "Sin permiso de accesibilidad: las teclas rápidas no responden",
    "Microphone still dead after a restart — check System Settings > Sound":
        "El micrófono sigue muerto tras reiniciar: mira Ajustes del Sistema > Sonido",
    "Microphone is dead — restart Vexflow manually":
        "Micrófono muerto: reinicia Vexflow a mano",
    "Microphone did not open — check input and permissions":
        "El micrófono no abrió: revisa la entrada y los permisos",
    "Microphone is dead — restarting": "Micrófono muerto: reiniciando",
    "Microphone rebuilt mid-recording — the start may be lost":
        "Micrófono rehecho a mitad de grabación: puede faltar el principio",
    "Deepgram connection dropped — text lost":
        "Se cortó la conexión con Deepgram: texto perdido",
    "Deepgram unreachable — check your connection":
        "Deepgram no responde: revisa la conexión",
    "Copied — press Cmd-V to paste": "Copiado: pega con Cmd-V",
    "duration limit": "límite de duración",
    "Deepgram connection dropped": "se cortó la conexión con Deepgram",
    "Stopped ({}) — text is on the clipboard, press Cmd-V":
        "Detenido ({}): el texto está en el portapapeles, pega con Cmd-V",

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
        "Se entrega tal cual, sin garantía de ningún tipo, y se usa enteramente bajo "
        "tu propio riesgo.\n\n"
        "{app} es un cliente de servicios externos que tú eliges, en los que tienes "
        "cuenta y a los que pagas directamente. Esos servicios no los opera {vendor} "
        "ni responden ante ella: sus condiciones, sus precios y el trato que den a "
        "tus datos son asunto entre ellos y tú, y aquí no se dice nada en su nombre. "
        "Lo que se gaste con tus claves es tuyo, y no se da ninguna garantía sobre la "
        "seguridad de ninguna clave que introduzcas.\n\n"
        "Los demás nombres pertenecen a sus dueños y aparecen solo para identificar "
        "con qué se conecta esto. No se afirma afiliación ni respaldo alguno.",

    # --- languages -----------------------------------------------------------
    "English": "Inglés",
    "Multilingual (code-switching)": "Multilingüe (cambio sobre la marcha)",
    "Spanish": "Español",
    "German": "Alemán",
    "French": "Francés",
    "Portuguese": "Portugués",
    "Italian": "Italiano",
    "Dutch": "Neerlandés",
    "Russian": "Ruso",
    "Ukrainian": "Ucraniano",
    "Polish": "Polaco",
    "Turkish": "Turco",
    "Hindi": "Hindi",
    "Japanese": "Japonés",

    # --- hotkeys -------------------------------------------------------------
    # Command, Option, Control and Shift stay: they are what is printed on the keys.
    "Right Command": "Command derecho",
    "Right Option": "Option derecho",
    "Left Command": "Command izquierdo",
    "Left Option": "Option izquierdo",
    "Left Control": "Control izquierdo",
    "Right Control": "Control derecho",
    "Left Shift": "Shift izquierdo",
    "Right Shift": "Shift derecho",
    "Control + Option": "Control + Option",
    "Control + Shift": "Control + Shift",
    "Command + Option": "Command + Option",
    "Option + Shift": "Option + Shift",
    "Control + Option + Shift": "Control + Option + Shift",

    # --- cleanup models ------------------------------------------------------
    # Model names are proper nouns; only what they are good for is translated.
    "Haiku 4.5 — fastest, cheapest": "Haiku 4.5: la más rápida y barata",
    "Sonnet 5 — balanced": "Sonnet 5: equilibrada",
    "Opus 5 — most accurate": "Opus 5: la más precisa",
    "GPT-5.6 Luna — fastest, cheapest": "GPT-5.6 Luna: la más rápida y barata",
    "GPT-5.6 Terra — balanced": "GPT-5.6 Terra: equilibrada",
    "GPT-5.6 Sol — most accurate": "GPT-5.6 Sol: la más precisa",
}
