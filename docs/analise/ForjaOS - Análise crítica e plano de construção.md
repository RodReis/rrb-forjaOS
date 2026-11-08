# ForjaOS (DeveloperOS) — Análise crítica e plano de construção

Nov 8, 2026 · @Rodrigo Reis

## Veredito

**Não construa do zero. Construa o DeveloperOS como uma imagem bootc/OCI derivada do Universal Blue (base Bazzite), e trate HERO e a Memória como dois produtos separados que rodam nela.** "Do zero" (LFS, kernel próprio, repositórios próprios) multiplica o esforço por uma ordem de grandeza e não entrega nada que o usuário final perceba — o diferencial que você descreveu está 100% na camada de cima: curadoria, integração, HERO, memória e identidade visual.

O que está sólido no briefing: o público (dev + gamer) existe e está mal servido por uma única distro; a tese "IA nativa no SO" ainda não tem dono no Linux (Omarchy chegou perto, mas é teclado-only e sem voz); as decisões caras do assistente (engines de voz, licenças de wake word, Policy Engine) já foram tomadas e validadas no rrb-jarvisOS — o código fica para trás, as decisões vêm junto.

O que está frágil e precisa mudar antes de começar:

1. **"Do zero" é a premissa errada.** Uma distro é 99% software de terceiros. O trabalho real é escolher a base certa e automatizar o build. Com bootc, o SO vira literalmente um `Containerfile` — exatamente a sua stack (Docker/DevOps).
2. **São 9 produtos, não 1.** Distro, assistente de voz, grafo de memória, segurança/monitoramento, marca, instalador dual-boot, integrações de IA, tema e documentação. Solo e meio período, isso não fecha em paralelo; o plano abaixo serializa.
3. **"Alta performance e baixo consumo" contradiz "ouvindo tudo" + LLM local + guardar memória de tudo.** Um Qwen3 8B residente consome 5–6 GB de VRAM/RAM; indexar "tudo" é I/O constante. Resolve-se com wake word em ONNX (dezenas de MB), LLM carregado sob demanda e captura de memória por escopo — não "tudo".
4. **"Tudo nativo" esbarra em licença.** Unity Hub, Claude Code e o userspace NVIDIA são proprietários: não podem ser *embarcados* na ISO de uma distro comunitária; entram por instalador de primeiro boot. Godot, Codex CLI, Ollama, Hermes Agent e os kernel modules abertos da NVIDIA podem.
5. **O nome é fraco.** "DeveloperOS" é genérico, difícil de registrar como marca e já existe um `DevOS-Developer-OS` no GitHub com a mesma descrição. Decisão sua, mas trato isso como risco na seção 10.

Prazo realista (você, meio período, sem equipe): imagem instalável com tema e stack dev em **6–8 semanas**; HERO v0 (texto + comandos de sistema) em **+10 semanas**; voz, memória/grafo e segurança em **+3–4 meses**. Um 1.0 publicável para a comunidade fica em **9–12 meses**. Qualquer plano que prometa menos está ignorando o HERO.

## Premissas frágeis e como o plano as corrige

| Premissa do briefing | Problema | Correção adotada no plano |
| --- | --- | --- |
| "Criar do zero" | Kernel, toolchain, repositório, instalador, segurança e atualizações são anos-pessoa. Nenhuma distro de sucesso dos últimos 10 anos (Bazzite, CachyOS, Omarchy, Pop!\_OS) partiu do zero. | Derivar de Fedora Atomic via Universal Blue. O SO é um `Containerfile` + GitHub Actions; atualizações e rollback vêm de graça. |
| "Alta performance e baixo consumo" + assistente "ouvindo tudo" + LLM local | Whisper + Qwen3 8B residentes ocupam 6–8 GB. Em uma RTX 5060 8 GB isso compete com o jogo. Electron custaria 150–300 MB ocioso; por isso o assistente nasce em Rust + QML. | HERO em camadas: wake word ONNX sempre ligado (< 50 MB, CPU); STT/LLM carregados sob demanda e descarregados após 5 min; "modo jogo" que suspende tudo exceto wake word. Metas numéricas na seção 8. |
| "Guardar memória de tudo" | Captura total (tela, teclado, arquivos) é o modelo do Windows Recall: pesado, controverso e difícil de tornar útil. | Captura por fontes nomeadas: histórico de shell, git, conversas com HERO, notas, janelas ativas (título + app, não conteúdo). Cada fonte é um plugin que o usuário liga. |
| "Integração nativa" com Unity, Claude CLI, Codex, API keys | Unity Hub e Claude Code são proprietários; não entram em ISO redistribuída. Chaves de API em `.bashrc` são um vazamento esperando acontecer. | Assistente de primeiro boot (`ujust`/wizard) instala o que não pode ser embarcado. Chaves no keyring do sistema (KWallet/libsecret) via `secret-tool`, expostas aos CLIs por wrapper. |
| "Detecção de ataques" em desktop | IDS em desktop pessoal é teatro na maior parte dos casos: o vetor real é pacote npm malicioso, extensão de VS Code e `curl \| bash`. | SELinux ligado (herdado do Fedora), firewalld, Secure Boot com módulos assinados, auditd + painel de logs. Sandbox de dev (distrobox/toolbox) como padrão para `npm install`. CrowdSec/Wazuh como opcional, não default. |
| Um único projeto | 9 frentes competem pelo mesmo tempo. Sem corte, nada chega a 1.0. | 3 repositórios com releases independentes: `developeros-image`, `hero`, `hero-memory`. A distro não espera o HERO para ser útil. |
| Interface "moderna e clean" como diferencial | Tema não segura usuário; Omarchy e Bluefin já são bonitos. O que segura é o fluxo (instalar → codar/jogar em 10 min) e o HERO. | Tema Plasma + wallpaper + ícones são Fase 1, mas o critério de pronto é funcional: "do pendrive ao `docker compose up` e ao Steam em menos de 15 minutos". |

Um ponto que o briefing não menciona e que define o projeto: **quem mantém depois do 1.0**. Distro é compromisso recorrente (CVE no kernel, quebra de driver NVIDIA a cada release do Fedora). A escolha de base abaixo foi feita para que a manutenção pesada (kernel, drivers, codecs, Steam) continue sendo do Universal Blue e você mantenha só a camada DeveloperOS.

## Decisão de base: distro-mãe, modelo de build e desktop

**Escolha: Fedora Atomic via Universal Blue, imagem derivada de `bazzite-dx-nvidia-open` (KDE Plasma 6), com um spin secundário `developeros-tiling` (niri ou Hyprland) para quem quer o estilo Omarchy.** A razão decisiva não é gosto: é que o build vira um `Containerfile` publicado no GHCR, o update é atômico com rollback, e kernel/NVIDIA/Steam/codecs continuam mantidos por outro time.

### Distro-mãe

| Opção | A favor | Contra | Veredito |
| --- | --- | --- | --- |
| **Fedora Atomic + Universal Blue (bootc/OCI)** | Build = Containerfile + GitHub Actions; rollback nativo; Bazzite já resolve NVIDIA, Steam, Proton, controles; Bluefin-DX já resolve Docker/Podman, VS Code, devcontainers, brew; template oficial para imagens customizadas; dezenas de derivados comunitários provam o caminho | `/usr` imutável: `dnf install` não é o fluxo padrão (usa-se distrobox, brew, flatpak ou camada na imagem); curva para quem vem de Ubuntu; dependência do ritmo do Fedora (release a cada 6 meses) | **Escolhido.** O modelo de build é a sua competência central e o custo de manutenção é o menor de todos. |
| Arch (modelo Omarchy/CachyOS) | Rolling, kernel e Mesa mais novos, AUR, melhor para gaming de ponta; público dev já está lá | Omarchy já ocupa exatamente o nicho "Arch para dev com agentes de IA" e tem US$ 10 M de apoio; rolling quebra driver NVIDIA com frequência; sem rollback atômico; você mantém repositório próprio | Competir de frente com Omarchy, solo, é má aposta. Oferecer o spin tiling cobre quem gosta do estilo. |
| NixOS | Reprodutibilidade total, declarativo | Curva íngreme para o público-alvo; binários proprietários (Unity, CUDA) exigem `nix-ld`/FHS env; UX de instalador fraca | Não para um produto com apelo visual e dual boot fácil. |
| Debian/Ubuntu LTS | Estabilidade, familiaridade | Kernel/Mesa velhos para gaming em hardware novo; snaps; Pop!\_OS já é o derivado dev/gaming desse ramo | Descartado. |

### Desktop

| Opção | Estado em nov/2026 | Veredito |
| --- | --- | --- |
| **KDE Plasma 6** | Maduro, Wayland + NVIDIA ok, HDR/VRR para jogos, padrão do Bazzite, altamente temável (o visual "clean" é trabalho de tema, não de DE) | **Padrão.** Menor risco, maior alcance. |
| COSMIC (System76, Rust) | Estável desde dez/2025 (1.0), hoje em 1.2/1.3; leve; tiling nativo; ainda com lacunas de applets e configuração; já há imagens ublue com COSMIC (Razorfin, bluefin-cosmic-dx) | Candidato forte para o 2.0. Acompanhar; não apostar o 1.0 nele. |
| Hyprland / niri | Estética e produtividade de teclado que o público dev adora; Omarchy provou a demanda | Suporte NVIDIA histórico ruim (melhorou); zero descoberta para quem vem do Windows; manutenção de configs é cara |
| GNOME | Padrão do Bluefin; polido | Extensões quebram a cada versão; pior para gaming (sem VRR estável por anos) |

### Como fica o build

```
developeros-image/
├─ Containerfile          # FROM ghcr.io/ublue-os/bazzite-dx-nvidia-open:stable
├─ build_files/           # scripts: pacotes, tema, HERO, ujust recipes
├─ system_files/          # /etc e /usr/share overlays (plasma, sddm, wallpapers, branding)
├─ recipes/               # ujust: install-unity, install-claude-code, setup-ai-keys
├─ iso/                   # bootc-image-builder → ISO Anaconda com dual boot
└─ .github/workflows/     # build diário, assinatura cosign, publish GHCR, ISO em release
```

Variantes publicadas: `developeros` (AMD/Intel), `developeros-nvidia-open` (Turing+), `developeros-tiling`. Quem já roda Bazzite/Bluefin troca com `bootc switch ghcr.io/<org>/developeros-nvidia-open:stable` sem reinstalar — esse é o canal de adoção mais barato que existe.

## Mapa requisito → solução

Regra do mapa: **"Pronto"** = herdado da base ou pacote existente, custo só de integração; **"Próprio"** = código que você escreve e mantém. Quanto mais "Próprio", mais tarde na fila.

| # | Requisito | Pronto (herdado/pacote) | Próprio (você escreve) | Risco principal |
| --- | --- | --- | --- | --- |
| 1 | Dev + jogos: Docker, git, Unity, Godot, DevOps, LLM local, Claude/Codex CLI, API keys | Docker CE e Podman (Bluefin-DX); Steam/Proton/gamescope (Bazzite); Godot (Flatpak, MIT); Ollama (rpm/container); Hermes Agent (MIT, pip/uv); Codex CLI (Apache-2.0, npm); `gh auth` + git-credential-libsecret; VS Code/Zed; devcontainers; k9s, kubectl, terraform via brew | Recipes `ujust install-unity-hub`, `ujust install-claude-code`, `ujust setup-ai-keys`; wrapper que injeta chaves do keyring no ambiente dos CLIs; perfil "gamedev" (Godot + Blender + Unity Hub + drivers) | Unity Hub e Claude Code proprietários → só instalador, nunca embarcado. Codex CLI pode ser embarcado. |
| 2 | Performance e baixo consumo | Kernel Bazzite (fsync, sched tuning), zram, `power-profiles-daemon`, Plasma 6 (\~1,2–1,6 GB ocioso) | Perfil "Jogo" que suspende HERO/memória/Ollama; orçamento de RAM por serviço próprio (seção 8); remover bloatware do Bazzite que não serve a dev (ex.: emuladores por padrão) | Seus próprios serviços (HERO, memória) são a maior ameaça à meta, não a base. |
| 3 | UX/UI moderna e clean | Plasma 6 + SDDM + Plymouth temáveis; Kvantum; Papirus/Tela ícones | Tema Plasma "DeveloperOS" (cores, blur, cantos), tema SDDM, Plymouth com logo, wallpapers, layout padrão do painel, atalhos; tema correspondente para VS Code/Zed/terminal (um tema só, aplicado em tudo — o truque do Omarchy) | Tema é trabalho de design; medir por teste com 5 usuários, não por gosto. |
| 4 | Redes, Wi-Fi, Bluetooth, NVIDIA, logs, monitoramento, ataques | NetworkManager, BlueZ, PipeWire (herdados); NVIDIA open kernel modules assinados pelo ublue (Turing+); journald; Cockpit; btop/nvtop; firewalld; SELinux enforcing; auditd | Painel "Saúde do sistema" dentro do HERO (lê journald, `nvidia-smi`, firewalld, auditd e resume em linguagem natural); alertas: login SSH novo, porta aberta nova, pacote com CVE crítica | GPUs Pascal e anteriores (GTX 10xx) ficam de fora do driver aberto 590+; declarar requisito mínimo RTX 20xx. |
| 5 | Dual boot com Windows | Instalador Anaconda (bootc-image-builder) particiona ao lado do Windows; GRUB/systemd-boot detecta Windows; Secure Boot funciona com a chave do ublue (enroll MOK no 1º boot) | Guia ilustrado + script pós-instalação: `timedatectl set-local-rtc 1` (relógio), aviso para desligar Fast Startup e BitLocker suspendido, montagem NTFS somente leitura por padrão | Relógio e BitLocker são 80% dos chamados de suporte de dual boot. Não reinventar instalador. |
| 6 | Licenciamento para distribuição | Fedora e ublue são redistribuíveis; NVIDIA permite redistribuição do driver em distros | Escolha de licença para código próprio; remoção de marcas Fedora/Bazzite (obrigatória); `THIRD_PARTY_LICENSES.md` gerado no build | Detalhado na seção 5. |
| 7 | Nome, logo, layout, wallpaper | — | Identidade visual completa (logo, paleta, tipografia, mascote HERO em 5 estados, wallpapers 4K claro/escuro, ícone de app) | Nome genérico e colisão com `DevOS` existente. Sugestão: manter "DeveloperOS" como descritor e registrar um nome próprio por cima (ex.: o nome do mascote). |
| 8 | Central de comando (Jarvis) | faster-whisper, Piper, Ollama, openWakeWord (código), MCP SDKs, D-Bus/systemd como superfície de controle | HERO: assistente novo e nativo em Rust + QML, herdando as decisões do rrb-jarvisOS (seção 6) | Maior bloco de código próprio do projeto. Define o cronograma. |
| 9 | Memória de tudo (Obsidian/graphify) | Vault Markdown compatível com Obsidian/Logseq; graphify (MIT) para código; SQLite + sqlite-vec para busca; Sigma.js/Cosmograph para o grafo | Coletores por fonte (shell, git, HERO, janelas); indexador; visualizador de grafo leve; API local consumida pelo HERO e pelos CLIs via MCP | Escopo. "Tudo" não fecha; "estas 5 fontes" fecha. |

Três consequências desse mapa: (a) os itens 1–5 e 7 são majoritariamente integração e saem na Fase 1–2; (b) os itens 8 e 9 são produtos de software e dominam o cronograma; (c) o item 6 é barato mas bloqueante — resolve-se antes do primeiro release público, não depois.

## Licenciamento e marca

**Uma distro não tem "uma licença": ela é um agregado. O que você controla é (a) o que embarca na imagem, (b) a licença do código próprio e (c) a marca.** Não sou advogado; o que segue é o que os textos das licenças dizem e o que as distros existentes praticam — valide com um advogado antes do primeiro release público.

### O que pode ir na imagem e o que só entra no 1º boot

| Componente | Licença | Embarcar na ISO? | Como entra |
| --- | --- | --- | --- |
| Fedora / Universal Blue base | GPL, MIT, Apache-2.0 (agregado); imagens ublue Apache-2.0 | Sim | `FROM` no Containerfile |
| NVIDIA kernel modules abertos | MIT/GPL-2.0 | Sim | Já vem na variante `-nvidia-open` |
| NVIDIA userspace (libGL, CUDA runtime) | Proprietária; licença permite redistribuição como parte de distro Linux | Sim (Bazzite e Pop!\_OS fazem) | Herdado da base |
| Steam | Proprietária; redistribuição do instalador é praxe (Bazzite, Pop!\_OS) | Sim, como instalador | Herdado |
| Godot | MIT | Sim | Flatpak ou rpm |
| Ollama | MIT | Sim | rpm/binário na imagem |
| Hermes Agent (Nous) | MIT | Sim | uv/pip na imagem ou recipe |
| Codex CLI (OpenAI) | Apache-2.0 | Sim | npm/binário na imagem |
| Claude Code (Anthropic) | Termos comerciais; não é open source | **Não** | `ujust install-claude-code` (instalador oficial no 1º boot) |
| Unity Hub / Editor | EULA Unity | **Não** | `ujust install-unity-hub` (download do site da Unity) |
| faster-whisper + modelos Whisper | MIT | Sim (modelos baixados no 1º uso, como já faz o jarvisOS) | Runtime na imagem, modelo sob demanda |
| Piper (TTS) | MIT; **vozes pt-BR têm licenças individuais** | Verificar voz a voz | Modelo sob demanda |
| openWakeWord | Código Apache-2.0; **modelos prontos CC BY-NC-SA (não comercial)** | Modelo próprio treinado, sim | Reaproveitar o modelo "Ei, amigo" do jarvisOS |
| Qwen3 / Llama via Ollama | Apache-2.0 / Llama Community | Download sob demanda | `ollama pull` no wizard |
| graphify | MIT | Sim | uv na imagem |

### Marca (trademark) — obrigações herdadas

- **Fedora:** derivados não podem usar nome nem logo da Fedora; podem dizer "baseado em Fedora". Remover `fedora-logos`, `fedora-release` branding e qualquer referência visual. O ublue já faz isso nas imagens dele; você faz o mesmo com a marca Bazzite/Bluefin.
- **Universal Blue / Bazzite:** código Apache-2.0, mas o projeto pede que derivados não se apresentem como Bazzite. Rebranding completo é requisito da Fase 1, não polimento.
- **NVIDIA, Steam, Unity, Claude, Codex:** uso nominativo ("compatível com", "instala") é permitido; logos deles no seu material de marketing não, sem autorização.

### Licença do código próprio e dos ativos

| Artefato | Recomendação | Por quê |
| --- | --- | --- |
| `developeros-image` (Containerfile, scripts, recipes) | **Apache-2.0** | Mesma licença do ublue, zero atrito para contribuição cruzada; inclui concessão de patente |
| `hero` (assistente) e `hero-memory` | **Apache-2.0 (decidido em 08/11)** | O Hermes Agent (MIT) mostra que permissiva não impede tração. AGPL protege contra apropriação, mas afasta empresas. |
| Wallpapers, ícones, tema | **CC BY-SA 4.0** | Padrão em distros; permite remix com atribuição |
| Nome e logo DeveloperOS / mascote HERO | **Fora de licença aberta; política de marca própria** (modelo Fedora/Mozilla) | É o único ativo que impede alguém de publicar um fork com o seu nome. Registro no INPI custa pouco e vale fazer cedo. |

Gerar `THIRD_PARTY_LICENSES.md` automaticamente no CI (lista de rpms + licenças via `rpm -qa --qf`) e publicar junto da ISO. Isso é o que separa um projeto distribuível de um hobby.

## HERO — Central de Comando por voz

**HERO é um projeto novo e nativo: daemon em Rust (`herod`) + plasmoid e plugin KRunner em QML, sem Electron. O rrb-jarvisOS sai do projeto como código e fica como herança documental** — seus ADRs migram para o repo `hero` e valem até serem revogados: faster-whisper small pt-BR, Piper, wake word própria com openWakeWord (Porcupine fechou o free tier; os modelos prontos do openWakeWord são não comerciais), Qwen3 via Ollama só local na rota de voz, mascote com estados e lip-sync por visemes, Policy Engine com `AuditEvent`, um único dono do microfone, e o invariante **conversa por voz não executa ação sem Policy Engine**. HERO é o nome do motor; o mascote tem o nome que o usuário escolher na instalação — padrão **Guará**, o lobo-guará do cerrado.

### Stack nativa (decidida em 08/11)

| Camada | Decisão | Por quê |
| --- | --- | --- |
| Daemon | Rust (`herod`), unit systemd de usuário com `MemoryMax` e `CPUQuota` | Memória previsível, sem runtime JS; crates maduras para ONNX (`ort`), PipeWire (`pipewire-rs`), D-Bus (`zbus`) e MCP (`rmcp`) |
| Shell visual | QML + KDE Frameworks: plasmoid do mascote na barra, overlay por Super+Espaço, plugin KRunner | É o que faz parecer parte do Plasma, não um app aberto; um tema só para o sistema inteiro |
| Áudio | PipeWire: HERO é um nó; o indicador de microfone do Plasma acende sozinho | Resolve "um único dono do microfone" por construção |
| Wake word | openWakeWord em ONNX Runtime, CPU | 40–60 MB residentes, sempre ligado sem custo perceptível |
| STT / TTS | faster-whisper small pt-BR e Piper como processos filhos sob demanda | Herdado; carregados após a wake word, descarregados após 5 min |
| Tela bloqueada | `logind` e `kscreenlocker` via D-Bus; bloqueado responde só por voz | Herdado do jarvisOS |
| Ações | MCP servers locais (stdio) + Policy Engine em tiers | Mesma superfície para Claude Code, Codex e Hermes |
| Mascote | Personagem 2D vetorial (lobo-guará) com 5 estados e lip-sync por visemes | Identidade de marca; outro personagem entra no mesmo contrato `VisemeEvent[]` |

**Nome escolhido na instalação — a restrição real:** a persona pode ter qualquer nome de graça (é texto no prompt), mas a wake word não. Cada palavra exige um modelo openWakeWord treinado com áudio sintético (o pipeline Piper que o jarvisOS já definiu), e isso leva de 20 a 60 min em GPU. Decisão: o instalador oferece uma lista curada com modelos já treinados e embarcados — Guará (padrão), Tupã, Jaci, Iara, Ipê, Boto, Curió, Arara — e um campo "nome personalizado" que treina em segundo plano após o primeiro boot, com Guará ativo até o modelo ficar pronto. Nomes de uma sílaba ou comuns em conversa ("Ana", "João") geram falso positivo e o instalador avisa.

### Cérebro: roteamento, não um modelo só

| Rota | Modelo padrão | Quando | Custo em VRAM |
| --- | --- | --- | --- |
| `wake-word` | openWakeWord ONNX (CPU) | Sempre ligado | \~0 (40–60 MB RAM) |
| `conversa-de-voz` | Qwen3 8B Q4 via Ollama, só local | Após wake word; descarregado após 5 min ocioso | \~5,5 GB (RTX 5060 8 GB: cabe sem jogo; com jogo, não) |
| `conversa-de-voz` (hardware fraco) | Qwen3 4B Q4 | GPU ≤ 8 GB com jogo aberto, ou sem GPU dedicada | \~3 GB |
| `pesquisa` / `criação` | Claude API, OpenAI API ou Codex/Claude Code em sessão | Usuário escolhe o provedor por rota no painel; chave vem do keyring | 0 local |
| `código` | Delegar a Claude Code / Codex CLI / Hermes Agent via terminal gerenciado | "HERO, abre o projeto X e roda os testes" | 0 local |
| `saúde-do-sistema` | Modelo local pequeno + dados estruturados | Resumo de logs, GPU, rede, firewall | Pequeno |

Sobre **Hermes Agent**: não é um LLM nem um substituto do Ollama — é um runtime de agente (MIT) com memória persistente e skills, que usa Ollama ou APIs por baixo. Ele compete com o loop de agente que o jarvisOS já tem. Decisão para a Fase 3: spike de 1 semana comparando manter o loop próprio vs. adotar Hermes como motor da rota `código`/`pesquisa`. Não adotar antes de medir.

### MCP como coluna vertebral

O HERO é um cliente MCP. As capacidades do SO viram servers MCP locais (stdio, sem rede), e **os mesmos servers ficam disponíveis para Claude Code, Codex e Hermes**. Uma integração, quatro consumidores:

- `hero-system`: processos, serviços systemd, journald, firewalld, NetworkManager, BlueZ, `nvidia-smi`, pacotes (`rpm-ostree`/`bootc` status). Cada tool tem tier no Policy Engine (ler = livre; alterar = aprovação; destrutivo = bloqueado por padrão).
- `hero-desktop`: janelas, notificações, MPRIS (mídia), clipboard, screenshots (com indicador), atalhos — via D-Bus do Plasma.
- `hero-dev`: Docker/Podman (containers, compose, logs), git/gh, projetos conhecidos, terminais gerenciados para os CLIs de IA.
- `hero-memory`: o vault e o grafo da seção 7.

### Invariantes que não se negociam no porte

1. Áudio nunca persiste; wake word e STT rodam locais; nada sai da máquina na rota de voz a menos que o usuário tenha escolhido um provedor cloud para aquela rota.
2. Indicador permanente de escuta (plasmoid + LED do PipeWire), kill switch alcançável, hotkey de mute, `AuditEvent` em journald ao ligar/desligar.
3. Nenhuma ação com efeito sem Policy Engine; catálogo de ações cresce por fatia com decisão registrada (a lição da F04: ampliar o catálogo reabre o modelo de aprovação).
4. HERO é opcional e removível: `systemctl --user disable hero` deixa um DeveloperOS perfeitamente usual. Quem não quer assistente não paga por ele.

&#91;embedded content: arquitetura do HERO · 5 camadas, do microfone ao sistema\]

Leitura: as entradas chegam ao serviço HERO, o roteador escolhe o cérebro por rota, e qualquer tool call volta pelo Policy Engine antes de tocar o sistema via MCP. Os servers da camada 4 são o único ponto de contato com o SO — e são reutilizados pelos CLIs de IA.

### Leitura do mockup (08/11)

O mockup mapeia quase 1:1 em Plasma 6, o que confirma a escolha de desktop. Metade dos elementos já existe como plasmoid nativo; o que é código próprio está marcado.

| Elemento do mockup | Implementação | Ajuste em relação ao desenho |
| --- | --- | --- |
| Barra superior: projeto/branch, relógio, GPU e temperatura, Wi-Fi, BT, "Escudo", bateria | Painel Plasma no topo; plasmoids nativos para rede/BT/bateria + 3 próprios (projeto git, GPU, Escudo) | "Jarvis local" vira o indicador do HERO com o nome escolhido — "Jarvis" é marca Marvel/Disney |
| Central de Comando lateral | Plasmoid em overlay, aberto por Super+Espaço, pela wake word ou pelo mascote | Não fica fixo: 520 px em 1920 é 27 % da tela. Fecha ao clicar fora e lembra a última aba |
| Card do assistente: orbe, transcrição, ações executadas, waveform | Topo do overlay; estados do mascote dirigidos por `VisemeEvent[]` | Orbe vira o lobo-guará; cada ação executada mostra o tier do Policy Engine (lido, alterado, aprovado) |
| Tiles Wi-Fi, Bluetooth, VPN, Modo Jogo, Firewall, Não perturbe | Nativos: NetworkManager, BlueZ, Não perturbe. Próprios: Modo Jogo (`hero-game.target`), Firewall (firewalld), VPN (WireGuard via NM) | Zero código para metade dos tiles |
| Desempenho: CPU, RAM, GPU, VRAM | `hero-system` lendo `/proc` e NVML; gráfico leve em QML | Amostra a cada 2 s; para quando o overlay fecha |
| Containers (Docker) | `hero-dev` via socket do Docker/Podman | Igual ao desenho |
| IA · modelos | `hero-system` (API do Ollama) + estado dos CLIs (chave presente ou não) | Igual ao desenho |
| Segurança e logs: CrowdSec, Suricata, journald | Padrão: journald + firewalld + auditd. CrowdSec e Suricata como módulo "Escudo", opt-in | Suricata exige modo promíscuo e CPU constante: fora do padrão, contradiz a meta de consumo |
| Rede: down/up, latência, dispositivos na LAN | NM + ping periódico + varredura ARP sob demanda | Varredura da LAN só por pedido, nunca em loop |
| Terminal: `devos doctor`, `devos ai`, `devos install unity`, `devos up` | CLI `forja` (Rust) que encapsula bootc, ujust, podman e o HERO | A melhor ideia do mockup: uma porta de entrada só, documentável e testável. Renomeada de `devos` para `forja` |
| Dock inferior: Code, Git, Dock, Unity, Godot, AI, Mon, Web, Apps | Painel Plasma inferior com lançadores | Unity só aparece depois de `forja install unity` |

## Memória do sistema (vault + grafo)

**Escopo: um vault Markdown compatível com Obsidian/Logseq, alimentado por coletores nomeados, indexado em SQLite e exibido como grafo leve. Não é "gravar tudo".** Captura total (tela, teclado, todo arquivo) é cara em I/O e disco, difícil de tornar útil e é o que afundou a recepção do Windows Recall. O que um dev realmente quer recuperar é "o que eu fiz, onde, por quê" — e isso vem de cinco fontes estruturadas.

### Fontes (cada uma é um plugin que o usuário liga)

| Fonte | O que entra | Como | Custo |
| --- | --- | --- | --- |
| Shell | Comandos, diretório, exit code, duração | `atuin` (já faz isso, SQLite, open source) ou hook próprio em zsh/fish | Desprezível |
| Git | Commits, branches, repos tocados, PRs via `gh` | Hooks `post-commit` + varredura diária | Desprezível |
| HERO | Conversas, decisões, ações aprovadas | O próprio HERO escreve notas diárias | Desprezível |
| Janelas e apps | Título da janela ativa + app + tempo (não o conteúdo) | D-Bus do KWin, amostragem a cada 30 s | Baixo |
| Projetos de código | Grafo de entidades e relações do código | graphify (MIT, tree-sitter, local) por repositório, sob demanda | Médio, só quando roda |
| Notas manuais | O que o usuário escreve | Pasta do vault aberta no Obsidian, Logseq ou no visualizador próprio | Zero |

Fora do escopo do 1.0: OCR de tela, conteúdo de navegador, e-mail. Podem virar plugins depois, cada um com sua decisão registrada.

### Formato e armazenamento

- `~/DeveloperOS/vault/` com `daily/AAAA-MM-DD.md`, `projects/<repo>.md`, `hero/`, `graph/` — Markdown puro com `[[wikilinks]]` e frontmatter YAML. Abre em qualquer editor; o usuário é dono do dado, sem formato proprietário.
- Índice em `~/.local/share/hero/memory.db` (SQLite + FTS5 para texto + `sqlite-vec` para embeddings locais via Ollama `nomic-embed-text` ou similar). Índice é derivável: apagar e reconstruir a partir do vault sempre funciona.
- Grafo: nós = notas, repos, commits, comandos, conversas; arestas = wikilinks + co-ocorrência temporal + relações do graphify. Exportado como `graph.json` (o mesmo formato que o graphify já produz, para não inventar outro).

### Visualizador

Um app pequeno (Tauri ou Qt/QML, não Electron) com três telas: linha do tempo do dia, grafo (Sigma.js/graphology ou Cosmograph, WebGL, aguenta dezenas de milhares de nós sem travar) e busca. Meta: abrir em < 1 s, < 150 MB de RAM com grafo de 10 mil nós. Obsidian é proprietário e não pode ser embarcado; Logseq é AGPL e pode entrar como opção no wizard, mas o visualizador próprio existe porque ele lê fontes que não são notas.

### Quem consome

O server `hero-memory` (MCP) expõe `search`, `timeline`, `related(entity)` e `remember(note)`. HERO usa para contexto de conversa ("o que eu estava fazendo ontem no projeto X?"); Claude Code e Codex usam para contexto de projeto; graphify já instala hook para o Claude Code preferir o grafo ao grep. É a mesma ideia do seu `rrb-proplan` e do sistema de memória dos agentes atuais, só que no nível do SO.

## Performance: metas mensuráveis

**"Alta performance" sem número é slogan. Estas são as metas que o CI mede em VM e em uma máquina de referência (Ryzen 7 9800X3D + RTX 5060 8 GB, que é o seu hardware) a cada build.** Falhar uma meta bloqueia o release `stable`; `testing` pode falhar.

| Métrica | Meta 1.0 | Referência hoje | Como medir |
| --- | --- | --- | --- |
| Boot (firmware → SDDM) | ≤ 12 s em NVMe | Bazzite \~10–15 s | `systemd-analyze` no CI (VM) e na máquina de referência |
| RAM ociosa após login (sem HERO) | ≤ 1,6 GB | Plasma 6 em Fedora: 1,2–1,6 GB | `free -m` 60 s após login, 3 amostras |
| RAM ociosa com HERO ligado (só wake word) | ≤ +80 MB (daemon Rust + plasmoid QML) | — | `smem` por processo |
| VRAM com HERO ocioso | 0 MB (modelos descarregados) | — | `nvidia-smi` após 5 min sem uso |
| Latência wake word → "escutando" | ≤ 300 ms | openWakeWord: \~80 ms por frame | Log de `AuditEvent` com timestamps |
| Latência fim da fala → início da resposta (local, Qwen3 8B já carregado) | ≤ 2,5 s | Whisper small \~0,8 s + primeiro token \~0,5 s + TTS \~0,6 s | Idem |
| Carga a frio do LLM (Ollama) | ≤ 6 s | 8B Q4 em NVMe: 3–6 s | Idem |
| Impacto em jogo com HERO em "modo jogo" | ≤ 1 % de FPS | — | MangoHud, 3 jogos de referência, com/sem HERO |
| Indexação de memória | ≤ 2 % CPU médio, I/O só em idle | — | `systemd-run` com `CPUQuota` e `IOSchedulingClass=idle` já impostos no unit |
| Tamanho da ISO | ≤ 6 GB | Bazzite \~5 GB | CI |
| Atualização | Atômica, com rollback em 1 comando | bootc herdado | `bootc rollback` testado no CI |

Decisões de engenharia que sustentam as metas:

- Todo serviço próprio é um unit systemd de usuário com `MemoryMax`, `CPUQuota` e `Nice` declarados. Se estourar, o systemd mata — o usuário não percebe um desktop lento.
- "Modo jogo" é um target systemd (`hero-game.target`) ativado pelo gamescope/Steam: para indexação, descarrega Ollama, mantém só wake word.
- Zero serviços de rede escutando por padrão (`ss -tlnp` vazio exceto loopback). Cockpit e SSH desligados até o usuário ligar.
- Nada de Electron em lugar nenhum do 1.0: o assistente nasce em Rust + QML.

## Roadmap por fases

**Seis fases, serializadas, cada uma com um critério de pronto que pode ser verificado por outra pessoa.** Estimativas assumem você sozinho em meio período (\~15–20 h/semana); com um segundo dev as fases 3 e 4 correm em paralelo e o total cai para \~6 meses.

&#91;embedded content: roadmap · 6 fases serializadas, 6 gates\]

Bandas de largura igual, não em escala; a duração está escrita em cada uma. Fases 3 e 4 somam 14–18 semanas: é onde um segundo dev muda o jogo.

| Fase | Duração | Entregáveis | Critério de pronto (gate) |
| --- | --- | --- | --- |
| **0 — Fundação** | 2 semanas | Decisões da seção 10 registradas como ADRs; org no GitHub com 3 repos; nome e identidade visual v1 (logo, paleta, tipografia, mascote estático); escolha de licenças; `THIRD_PARTY_LICENSES` no CI | Containerfile `FROM bazzite-dx-nvidia-open` builda no GitHub Actions, assinado com cosign, publicado no GHCR |
| **1 — Imagem instalável** | 4–6 semanas | Rebranding completo (zero Fedora/Bazzite visível); tema Plasma + SDDM + Plymouth + wallpapers; layout padrão; ISO via bootc-image-builder; 3 variantes; guia de dual boot; `ujust` recipes (Unity Hub, Claude Code, chaves no keyring) | Do pendrive a `docker compose up` + Steam rodando em < 15 min, em dual boot na sua máquina e em VM; metas de boot e RAM da seção 8 passando |
| **2 — Experiência dev/gamedev** | 3–4 semanas | Wizard de 1º boot (perfis: web, backend, gamedev, devops, IA); Godot, Ollama, Hermes, Codex embarcados; wrapper de chaves; devcontainers e distrobox prontos; perfil "gamedev" com Blender/Godot/Unity Hub; painel de saúde (Cockpit tematizado) | 5 usuários externos instalam sem suporte e completam o wizard; CVE scan da imagem limpo |
| **3 — HERO v0 (texto + sistema)** | 8–10 semanas | Daemon herod em Rust + plasmoid QML (código novo, decisões herdadas do jarvisOS); servers MCP `hero-system`, `hero-desktop`, `hero-dev`; Policy Engine e `AuditEvent` em journald; plasmoid + KRunner; spike Hermes vs. loop próprio | "Abre o projeto X, sobe o compose e me mostra os logs" funciona por texto com aprovação; HERO desligado não deixa rastro de consumo |
| **4 — HERO voz + Memória** | 8–10 semanas | Wake word "Ei, Guará" (e lista curada de nomes) via PipeWire; STT/TTS sob demanda; modo jogo; mascote animado; coletores shell/git/HERO/janelas; vault + índice SQLite; `hero-memory` MCP; visualizador v0 (Tauri/Qt) | Metas de latência e VRAM da seção 8; "o que eu fiz ontem no projeto X?" responde com fontes; FPS em jogo não cai > 1 % |
| **5 — Segurança, docs e release público** | 4 semanas | Secure Boot documentado; firewalld/SELinux/auditd verificados; alertas de segurança no HERO; site, docs, changelog, canal de updates `stable`/`testing`; revisão jurídica de licenças e marca; treinamento em segundo plano de wake word para nome personalizado | Release 1.0 com ISO + imagem OCI; 50 instalações externas sem bug bloqueante em 30 dias |

O que fica fora do 1.0 e vai para o backlog do 2.0: COSMIC como desktop alternativo, spin tiling completo, visão (câmera/Frigate), OCR de tela, integrações Gmail/Agenda/Spotify do jarvisOS, loja de skills do HERO, suporte ARM.

Dois cortes que recomendo já aceitar: (1) **não fazer instalador próprio** — Anaconda com dual boot é feio, mas funciona e é mantido por outros; (2) **não fazer app store própria** — Discover + Flathub + brew + `ujust` cobrem tudo.

## Decisões fechadas em 08/11/2026

Cada linha vira um ADR em `forjaos-image/docs/adr/`. Reabrir uma decisão exige um ADR novo que revogue o anterior, com a razão escrita.

| # | Decisão | Escolha | Consequência imediata |
| --- | --- | --- | --- |
| 1 | Base | Fedora Atomic via Universal Blue, `FROM bazzite-dx-nvidia-open` | Repo `forjaos-image`; build em GitHub Actions; rebranding total de Fedora/Bazzite |
| 2 | Desktop | KDE Plasma 6 padrão; spin tiling (niri/Hyprland) só no 2.0 | Tema, SDDM, Plymouth e plasmoids em QML |
| 3 | Nome do SO | **ForjaOS** ("DeveloperOS" como descritor) | Verificar INPI e domínios (forjaos.dev, forjaos.com.br) antes do logo; CLI chama-se `forja` |
| 4 | Assistente | Projeto novo e nativo em Rust + QML; rrb-jarvisOS sai como código, entra como ADRs | Fase 3 passa de 6–8 para 8–10 semanas; some a migração Electron → nativo da Fase 5 |
| 5 | Nome do mascote | Escolhido na instalação; padrão **Guará** | Lista curada com wake words pré-treinadas + nome personalizado treinado em segundo plano; HERO segue como nome do motor |
| 6 | Licenças | Imagem, MCP servers, HERO e memória: **Apache-2.0**; artes CC BY-SA 4.0; nome e logo sob política de marca própria | `LICENSE` em todos os repos; `THIRD_PARTY_LICENSES.md` gerado no CI |
| 7 | Rota de voz | 100 % local; cloud opt-in por rota, nunca para a fala | Qwen3 4B em GPUs de 8 GB com jogo aberto |
| 8 | Hardware mínimo | NVIDIA RTX 20xx+ (driver aberto) ou AMD RDNA2+, 8 GB VRAM, 16 GB RAM, NVMe | GTX 10xx fora; declarar na página de download |
| 9 | Hermes Agent | Não adotar antes do spike de 1 semana na Fase 3 | Loop próprio é o padrão até lá |
| 10 | Equipe e sustentação | Solo, 100 % comunitário | Prazo 10–12 meses; sem versão paga; registro de marca fica opcional (ainda recomendo: é barato e é o único ativo que protege o nome) |

Renomeações decorrentes: `developeros-image` → `forjaos-image`; `devos` do mockup → `forja`; variantes `forjaos`, `forjaos-nvidia-open`, `forjaos-tiling`. Os servers MCP mantêm o prefixo `hero-`.

Próximo passo: gerar o repo `forjaos-image` (Containerfile, workflow, primeiro `ujust`) e o esqueleto do `hero` (`herod` em Rust + plasmoid QML vazio) — imagem bootando em VM nesta semana.

## Fontes consultadas

- Universal Blue — [image-template](https://github.com/ublue-os/image-template) e derivados comunitários ([Razorfin: Bazzite + COSMIC](https://github.com/RazorfinOS-org/Razorfin), [bluefin-cosmic-dx](https://github.com/ericrocha97/bluefin), [hyprblue/hyprbazzite](https://github.com/ashebanow/hyprblue))
- COSMIC — [LWN: Going boldly into the COSMIC desktop environment](https://lwn.net/Articles/1050268/) (dez/2025) e [Wikipedia: COSMIC desktop](https://en.wikipedia.org/wiki/COSMIC_desktop) (1.2.0, jul/2026)
- Omarchy — [The New Stack: What is Omarchy Linux](https://thenewstack.io/what-is-omarchy-linux-and-why-is-37signals-moving-to-it/) e [The Register: Omarchy distro gains serious backing](https://www.theregister.com/a/5293026)
- NVIDIA — [Phoronix: open kernel driver default for Turing+](https://www.phoronix.com/news/NVIDIA-R560-Open-Default) e [Tom's Hardware: transição para módulos abertos](https://www.tomshardware.com/pc-components/gpu-drivers/nvidia-transitioning-to-open-source-gpu-kernel-modules-for-linux); Arch adotou open por padrão no driver 590 (dez/2025)
- Hermes Agent — [repositório NousResearch/hermes-agent](https://github.com/nousresearch/hermes-agent) (MIT, fev/2026)
- graphify — [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) (MIT) e [guia Claude Code](https://graphify.com/blog/how-to-give-claude-code-a-code-knowledge-graph)
- Colisão de nome — [DevOS-Developer-OS no GitHub](https://github.com/DevOS-Developer-OS)
- Decisões do rrb-jarvisOS (SPECs Voz-01/02/03 e Escuta-01–04): engines, licenças de wake word, Policy Engine, hardware de referência — do histórico do projeto
