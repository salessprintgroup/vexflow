"""Portuguese interface strings.

The key is the English source string, so an entry that is missing here falls back to
English rather than to a bare identifier. Adding or fixing a language: see README.md
in this directory.
"""
TABLE = {
    # --- menu bar ------------------------------------------------------------
    "Ready": "Pronto",
    "Recording…": "Gravando…",
    "Paused": "Em pausa",
    "Stop recording": "Parar a gravação",
    "Pause": "Pausar",
    "Resume": "Retomar",
    "Language": "Idioma de reconhecimento",
    "LLM Cleanup": "Limpeza com LLM",
    "Clean up transcripts": "Limpar a transcrição",
    "Setup Guide…": "Primeiros passos…",
    "Settings…": "Ajustes…",
    "Open log": "Abrir o registro",
    "Vexflow on GitHub": "Vexflow no GitHub",
    "Built by ": "Feito por ",
    "Quit Vexflow": "Sair",
    "About ": "Sobre o ",
    "Hide ": "Ocultar ",
    "Quit ": "Sair do ",
    "Edit": "Editar",
    "Undo": "Desfazer",
    "Redo": "Refazer",
    "Cut": "Recortar",
    "Copy": "Copiar",
    "Paste": "Colar",
    "Select All": "Selecionar tudo",
    "Hold ": "Segure ",
    "tap ": "toque em ",
    "middle mouse button": "botão do meio do mouse",

    # --- key states, menu bar ------------------------------------------------
    "No Deepgram key — open Settings": "Sem chave da Deepgram — abra os ajustes",
    "Checking your Deepgram key…": "Verificando sua chave da Deepgram…",
    "Deepgram rejected your key — open Settings":
        "A Deepgram recusou a chave — abra os ajustes",
    "Can't reach Deepgram — check your connection":
        "Deepgram fora de alcance — verifique a conexão",
    "Balance: {}": "Saldo: {}",
    "Balance: {} — running low": "Saldo: {} — está acabando",
    "Balance: …": "Saldo: …",
    "Balance: checking…": "Saldo: verificando…",
    "Balance key rejected — open Settings":
        "Chave de saldo recusada — abra os ajustes",
    "Balance: can't reach Deepgram": "Saldo: Deepgram fora de alcance",
    " — no key": " — sem chave",
    " — checking the key…": " — verificando a chave…",
    " — key rejected": " — chave recusada",
    " — could not check the key": " — não foi possível verificar a chave",

    # --- macOS permission dialog ---------------------------------------------
    # Shown by macOS itself, so it follows the system language, not the setting.
    "Vexflow sends your speech to Deepgram with your own API key so it can be "
    "typed as text.":
        "O Vexflow envia sua voz para a Deepgram com a sua própria chave de API para devolvê-la como texto.",

    # --- settings window: frame ----------------------------------------------
    "{} Settings": "Ajustes do {}",
    "Interface language": "Idioma da interface",
    "Restart to apply": "Reiniciar",
    "Applied after the restart in step 3.":
        "Vale a partir do reinício do passo 3.",
    "Keys": "Chaves",
    "Dictation": "Ditado",
    "Cleanup": "Limpeza",
    "Permissions": "Permissões",
    "Done": "OK",

    # --- settings: keys ------------------------------------------------------
    "Speech to text": "Reconhecimento de fala",
    "Audio goes from this Mac straight to Deepgram using your own key. "
    "Fields marked * are required.":
        "O áudio sai deste Mac direto para a Deepgram com a sua própria chave. "
        "Os campos marcados com * são obrigatórios.",
    "Transcript cleanup": "Limpeza da transcrição",
    "Optional. A small model fixes punctuation, false starts and mangled "
    "names. Without a key you still get the raw transcript.":
        "Opcional. Um modelo pequeno corrige a pontuação, os tropeços e os nomes "
        "estropiados. Sem chave, você ainda fica com a transcrição bruta.",
    "Deepgram key": "Chave da Deepgram",
    "Balance key": "Chave do saldo",
    "Anthropic key": "Chave da Anthropic",
    "OpenAI key": "Chave da OpenAI",
    "Save": "Salvar",
    "Get key": "Obter",
    "paste key": "cole a chave",
    "paste a new key to replace": "cole uma chave nova para substituir",
    "{} characters — press Save": "{} caracteres — clique em Salvar",

    # --- settings: key statuses ----------------------------------------------
    "Not set": "Não definida",
    "Saved in Keychain": "Salva no Chaveiro",
    "Required — dictation does not work without it":
        "Obrigatória — sem ela não há ditado",
    "Checking with Deepgram…": "Verificando com a Deepgram…",
    "Verified — Deepgram accepted this key":
        "Verificada — a Deepgram aceitou esta chave",
    "Deepgram rejected this key. Check you copied all of it.":
        "A Deepgram recusou esta chave. Confira se você copiou ela inteira.",
    "Saved, but Deepgram could not be reached to check it":
        "Salva, mas a Deepgram não respondeu para verificar",
    "Deepgram rejected this key, or it has no billing:read scope":
        "A Deepgram recusou esta chave, ou ela não tem o escopo billing:read",
    "Checking with {}…": "Verificando com {}…",
    "Verified — {} accepted this key": "Verificada — {} aceitou esta chave",
    "{} rejected this key": "{} recusou esta chave",
    "{} rejected this key: {}": "{} recusou esta chave: {}",
    "Saved, but {} could not be reached to check it":
        "Salva, mas {} não respondeu para verificar",

    # --- settings: help popovers ---------------------------------------------
    "Open the console": "Abrir o console",
    "The one key Vexflow cannot work without. Your microphone audio goes from this "
    "Mac to the speech-to-text service under this key and comes back as text, with "
    "no server of ours in between. Create a key in your own account there and paste "
    "the whole string. It is kept in your login Keychain, never in a file — and, "
    "like any credential on any machine, it is yours to look after.":
        "A única chave sem a qual o Vexflow não funciona. O áudio do seu microfone "
        "sai deste Mac para o serviço de reconhecimento sob esta chave e volta como "
        "texto, sem nenhum servidor nosso no meio. Crie uma chave na sua própria "
        "conta lá e cole a string inteira. Ela fica no Chaveiro de início de sessão, "
        "nunca em um arquivo — e, como qualquer credencial em qualquer máquina, o "
        "cuidado com ela é seu.",
    "Optional, and a second key on purpose. Reading your account balance needs the "
    "billing:read scope, which the key above has no business holding — one key that "
    "spends and one that reads are worth keeping apart. Create a key with "
    "billing:read only and the menu bar shows the balance the service reports.":
        "Opcional, e uma segunda chave de propósito. Ler o saldo da conta exige o "
        "escopo billing:read, que a chave acima não tem por que carregar: uma chave "
        "que gasta e outra que lê a conta vale a pena manter separadas. Crie uma "
        "chave só com billing:read e a barra de menus mostra o saldo que o serviço "
        "informa.",
    "Optional. Drives the cleanup pass that repairs punctuation, false starts and "
    "mangled names. Only the transcript is sent, never the audio, and what the "
    "service does with it is between you and them. The key is checked the moment "
    "you save it, so a wrong one says so here instead of quietly doing nothing.":
        "Opcional. Move a passagem de limpeza que conserta a pontuação, os tropeços "
        "e os nomes estropiados. Só a transcrição é enviada, nunca o áudio, e o que "
        "o serviço faz com ela é entre você e ele. A chave é verificada na hora em "
        "que você salva, então uma errada avisa aqui mesmo em vez de ficar quieta "
        "sem fazer nada.",
    "Optional, and an alternative to the key above rather than an addition — "
    "cleanup uses whichever provider is selected on the Cleanup tab. That tab can "
    "also point this key at any OpenAI-compatible endpoint, including a model "
    "running on your own machine.":
        "Opcional, e mais uma alternativa à chave acima do que um acréscimo: a "
        "limpeza usa o provedor que estiver selecionado na aba Limpeza. É lá também "
        "que esta chave pode apontar para qualquer endereço compatível com OpenAI, "
        "inclusive um modelo rodando na sua própria máquina.",

    # --- settings: dictation -------------------------------------------------
    "Recognition language": "Idioma de reconhecimento",
    "A single language recognises better than Multilingual. Choose "
    "Multilingual only if you switch languages inside one sentence.":
        "Um único idioma é reconhecido melhor que o modo multilíngue. Escolha "
        "multilíngue só se você troca de idioma dentro de uma mesma frase.",
    "Push to talk": "Segurar para falar",
    "Hold, speak, release.": "Segure, fale, solte.",
    "Hands-free toggle": "Alternador",
    "Off": "Não",
    "Tap once to start, tap again to stop.":
        "Um toque começa, outro toque termina.",
    "Combined entries fire only while both keys are held — safer when the "
    "free single keys are ones you type with.":
        "As combinações só agem enquanto as duas teclas estão pressionadas. Ajuda "
        "quando as teclas simples que sobraram são as que você usa para escrever.",
    "Also toggle with the middle mouse button":
        "Alternar também com o botão do meio do mouse",
    "Play a sound when recording starts and stops":
        "Som no início e no fim da gravação",
    "Paste automatically (off: copy to clipboard only)":
        "Colar automaticamente (se não: só copiar)",

    # --- settings: cleanup ---------------------------------------------------
    "Clean up transcripts with an LLM": "Limpar a transcrição com um LLM",
    "Provider": "Provedor",
    "Model": "Modelo",
    "No {} key yet — add one on the Keys tab.":
        "Ainda não há chave da {} — adicione uma na aba Chaves.",
    "{} rejected the key — check it on the Keys tab.":
        "{} recusou a chave — confira na aba Chaves.",
    "Your vocabulary": "Seu vocabulário",
    "Edit vocabulary…": "Abrir o vocabulário…",
    "Names and jargon the recogniser keeps getting wrong. One per line, "
    "kept on this Mac.":
        "Nomes e jargões que o reconhecimento erra sempre. Um por linha, e o arquivo "
        "fica neste Mac.",
    "Advanced": "Avançado",
    "Endpoint": "Endereço",
    "Leave as-is for the vendor's own API, or point it at any "
    "OpenAI-compatible endpoint.":
        "Deixe como está para a API do próprio provedor, ou aponte para qualquer "
        "endereço compatível com OpenAI.",

    # --- settings: permissions -----------------------------------------------
    "macOS asks for these once. Vexflow cannot record or type without them.":
        "O macOS pede isso uma vez só. Sem elas o Vexflow não grava nem escreve.",
    "Microphone": "Microfone",
    "Lets Vexflow hear you.": "Para o Vexflow ouvir você.",
    "Accessibility": "Acessibilidade",
    "Lets Vexflow see the hotkey and paste into the app you are using. "
    "Granting it takes effect only after Vexflow restarts.":
        "Para o Vexflow ver a tecla de atalho e colar no app que você está usando. "
        "Depois de concedida, ela só vale quando o Vexflow reinicia.",
    "Granted": "Concedida",
    "Not granted": "Não concedida",
    "Not requested yet": "Ainda não solicitada",
    "Asked on first use": "Pedida no primeiro uso",
    "Open Settings": "Abrir os ajustes",
    "Re-check": "Verificar de novo",
    "Restart Vexflow": "Reiniciar o Vexflow",
    "Keep a diagnostic log": "Manter um registro de diagnóstico",
    "Off, so nothing about your dictation reaches the disk. Turn it on to "
    "chase a problem and off again afterwards — switching it off deletes the "
    "file. It records timings and errors, never what you said.":
        "Desligado, então nada do seu ditado chega ao disco. Ligue para caçar um "
        "problema e desligue depois: desligar apaga o arquivo. Ele anota tempos e "
        "erros, nunca o que você disse.",
    "Transcript debug logging is ON for this run — dictated text is being "
    "written to the log. Restart without VEXFLOW_DEBUG_TRANSCRIPT to stop it.":
        "Nesta execução o registro de depuração das transcrições está LIGADO — o "
        "texto ditado está indo para o registro. Reinicie sem "
        "VEXFLOW_DEBUG_TRANSCRIPT para parar.",
    "VEXFLOW_DEBUG_TRANSCRIPT is set for this run: switching the log on would "
    "write what you dictate into it.":
        "Nesta execução VEXFLOW_DEBUG_TRANSCRIPT está definido: ligar o registro "
        "faria o que você dita ir parar dentro dele.",
    "Remove Vexflow from this Mac…": "Remover o Vexflow deste Mac…",

    # --- uninstall dialogs ---------------------------------------------------
    "Remove Vexflow from this Mac?": "Remover o Vexflow deste Mac?",
    "This quits Vexflow, removes it from your login items and deletes the "
    "app. Your API keys and settings are kept unless you choose otherwise.":
        "O Vexflow fecha, sai dos itens de início e o app é apagado. Suas chaves e "
        "ajustes ficam, a menos que você escolha o contrário.",
    "Remove": "Remover",
    "Cancel": "Cancelar",
    "Remove and Delete My Keys": "Remover junto com as chaves",
    "Vexflow has been removed.": "O Vexflow foi removido.",
    "Login item removed, but deleting the app was cancelled.":
        "Saiu dos itens de início, mas apagar o app foi cancelado.",
    "Login item removed, but the app could not be deleted.":
        "Saiu dos itens de início, mas não foi possível apagar o app.",
    "Login item removed; deleting the app failed: ":
        "Saiu dos itens de início; apagar o app falhou: ",
    "Microphone and Accessibility entries stay in System Settings until "
    "you remove them by hand.":
        "As entradas de Microfone e Acessibilidade continuam nos Ajustes do Sistema "
        "até você removê-las na mão.",

    # --- setup guide ---------------------------------------------------------
    "Welcome to ": "Boas-vindas ao ",
    "Set up ": "Configurar o ",
    "macOS needs to grant two permissions before dictation can work. "
    "This takes about a minute.":
        "O macOS precisa conceder duas permissões antes de o ditado funcionar. Leva "
        "cerca de um minuto.",
    "Allow microphone access": "Permita o acesso ao microfone",
    "So Vexflow can hear you.": "Para o Vexflow ouvir você.",
    "Allow accessibility access": "Permita o acesso de acessibilidade",
    "So Vexflow can see the hotkey and paste the text.":
        "Para o Vexflow ver a tecla de atalho e colar o texto.",
    "macOS applies the accessibility grant only at launch.":
        "O macOS aplica essa permissão só na abertura.",
    "Allow": "Permitir",
    "Restart": "Reiniciar",
    "Step {} of {}": "Passo {} de {}",
    "Permissions are set.": "Permissões concedidas.",
    "Denied — turn it on in System Settings":
        "Negada — ligue nos Ajustes do Sistema",
    "Requested on first use": "Pedida no primeiro uso",
    "Hotkeys are live": "As teclas de atalho funcionam",
    "Restart to activate the hotkey": "Reinicie para ativar a tecla de atalho",
    "Finish step 2 first": "Termine antes o passo 2",
    "Close": "Fechar",
    "Add your API key": "Adicionar a chave",

    # --- engine notices in the menu ------------------------------------------
    "Restarted after a dead microphone — please dictate again":
        "Reiniciado depois de um microfone morto — dite de novo",
    "No Accessibility permission — hotkeys are dead":
        "Sem permissão de acessibilidade — teclas de atalho mortas",
    "Microphone still dead after a restart — check System Settings > Sound":
        "Microfone ainda morto após reiniciar — veja Ajustes do Sistema > Som",
    "Microphone is dead — restart Vexflow manually":
        "Microfone morto — reinicie o Vexflow na mão",
    "Microphone did not open — check input and permissions":
        "O microfone não abriu — confira a entrada e as permissões",
    "Microphone is dead — restarting": "Microfone morto — reiniciando",
    "Microphone rebuilt mid-recording — the start may be lost":
        "Microfone refeito no meio da gravação — o começo pode ter se perdido",
    "Deepgram connection dropped — text lost":
        "A conexão com a Deepgram caiu — texto perdido",
    "Deepgram unreachable — check your connection":
        "Deepgram fora de alcance — verifique a conexão",
    "Copied — press Cmd-V to paste": "Copiado — cole com Cmd-V",
    "duration limit": "limite de duração",
    "Deepgram connection dropped": "a conexão com a Deepgram caiu",
    "Stopped ({}) — text is on the clipboard, press Cmd-V":
        "Parado ({}) — o texto está na área de transferência, use Cmd-V",

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
        "Fornecido como está, sem garantia de nenhum tipo, e usado inteiramente por "
        "sua conta e risco.\n\n"
        "{app} é um cliente para serviços externos que você escolhe, nos quais tem "
        "conta e aos quais paga diretamente. Esses serviços não são operados pela "
        "{vendor} nem respondem a ela: os termos, os preços e o tratamento dos seus "
        "dados são assunto entre você e eles, e aqui nada é dito em nome deles. O "
        "que for gasto com as suas chaves é seu, e nenhum compromisso é assumido "
        "quanto à segurança de qualquer chave que você digitar.\n\n"
        "Os demais nomes pertencem aos seus donos e aparecem apenas para identificar "
        "a que isto se conecta. Nenhuma afiliação ou endosso é alegado.",

    # --- languages -----------------------------------------------------------
    "English": "Inglês",
    "Multilingual (code-switching)": "Multilíngue (troca no meio da fala)",
    "Spanish": "Espanhol",
    "German": "Alemão",
    "French": "Francês",
    "Portuguese": "Português",
    "Italian": "Italiano",
    "Dutch": "Neerlandês",
    "Russian": "Russo",
    "Ukrainian": "Ucraniano",
    "Polish": "Polonês",
    "Turkish": "Turco",
    "Hindi": "Híndi",
    "Japanese": "Japonês",

    # --- hotkeys -------------------------------------------------------------
    # Command, Option, Control and Shift stay: they are what is printed on the keys.
    "Right Command": "Command direito",
    "Right Option": "Option direito",
    "Left Command": "Command esquerdo",
    "Left Option": "Option esquerdo",
    "Left Control": "Control esquerdo",
    "Right Control": "Control direito",
    "Left Shift": "Shift esquerdo",
    "Right Shift": "Shift direito",
    "Control + Option": "Control + Option",
    "Control + Shift": "Control + Shift",
    "Command + Option": "Command + Option",
    "Option + Shift": "Option + Shift",
    "Control + Option + Shift": "Control + Option + Shift",

    # --- cleanup models ------------------------------------------------------
    # Model names are proper nouns; only what they are good for is translated.
    "Haiku 4.5 — fastest, cheapest": "Haiku 4.5 — a mais rápida e barata",
    "Sonnet 5 — balanced": "Sonnet 5 — equilibrada",
    "Opus 5 — most accurate": "Opus 5 — a mais precisa",
    "GPT-5.6 Luna — fastest, cheapest": "GPT-5.6 Luna — a mais rápida e barata",
    "GPT-5.6 Terra — balanced": "GPT-5.6 Terra — equilibrada",
    "GPT-5.6 Sol — most accurate": "GPT-5.6 Sol — a mais precisa",
}
