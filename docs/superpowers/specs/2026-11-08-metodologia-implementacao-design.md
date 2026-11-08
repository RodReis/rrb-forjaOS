# Spec — Metodologia executável de implementação do ForjaOS

**Data:** 2026-11-08 · **Status:** aprovada em conversa, aguardando revisão do arquivo · **Fase do PRD:** 0 (Fundação)

## 1. Problema

O PRD 1.0 define o quê; nada define *como* Claude Code e Codex devem trabalhar no repositório. Sem isso, cada sessão de agente inventa fluxo, tela e tokens. Os protótipos em `docs/telas/` são HTML/Tailwind gerados em datas diferentes, com três design systems e conteúdo pré-rename (`Jarvis`, `devos`, `nftables`, `24.04 LTS`), enquanto o produto final é QML/KDE, Plymouth, GRUB, Konsole e Rust.

## 2. Decisões tomadas (2026-11-08)

| # | Decisão | Consequência |
| --- | --- | --- |
| D0 | **Numeração de ADR:** ADR-025 permanece reservado ao resultado do spike Hermes (FR-097). Novos ADRs desta entrega começam em 026. | — |
| D1 | **Precedência:** layout, hierarquia, tokens, espaçamento e animação vêm do protótipo; textos, nomes, comandos, versões e componentes de sistema vêm do PRD. Divergência vira issue, nunca improviso. | ADR-028 |
| D2 | **Tema canônico:** escuro = *Cybernetic Forge*, claro = *Alabaster Forge*. *Cybernetic Obsidian* aposentado. Mono = JetBrains Mono em tudo; Fira Code proibida; Inter só em body de dados densos (tabelas, telemetria). | ADR-027, `brand/palette.json` |
| D3 | **Monorepo** neste repositório (`rrb-forjaOS`), pastas por componente. Revoga a tabela de 7 repositórios da §5.2 do PRD. Separação futura via `git subtree split` se necessário. | ADR-026 |
| D4 | **Escopo desta entrega:** só metodologia e governança. Fase 0 (Containerfile, CI, `check-branding.sh` real) é a primeira tarefa executada pelo fluxo criado aqui. | `roadmap.json` |
| D5 | **Metodologia executável (opção B):** documentos + comandos por etapa + scripts de verificação. `AGENTS.md` é a fonte única; `CLAUDE.md` importa com `@AGENTS.md`. | §4 |

## 3. Estrutura de arquivos entregue

```
rrb-forjaOS/
├─ AGENTS.md                      fonte única das regras de agente (Codex lê nativamente)
├─ CLAUDE.md                      "@AGENTS.md" + notas específicas do Claude Code
├─ .claude/commands/              plan.md code.md test.md review.md ship.md
├─ .github/PULL_REQUEST_TEMPLATE.md
├─ brand/palette.json             ÚNICA fonte de tokens (FR-051)
├─ image/ cli/ hero/ hero-mcp/ hero-memory/ brand/ site/
│  └─ AGENTS.md                   escopo, linguagem, testes e DoD da pasta (curto)
├─ docs/
│  ├─ PRD.md                      §5.2 ganha nota de revogação (ADR-026); tabela de status ligada a STATUS.md
│  ├─ adr/0026-monorepo.md
│  ├─ adr/0027-design-tokens-canonicos.md
│  ├─ adr/0028-precedencia-prototipo-prd.md
│  ├─ dev/METHODOLOGY.md          fluxo plan → code → test → review → ship, gates e checklists
│  ├─ design-system/DESIGN-RULES.md
│  ├─ design-system/telas/<slug>.md   uma spec por protótipo (16)
│  ├─ STATUS.md                   GERADO por scripts/roadmap.py
│  ├─ roadmap/roadmap.json        fonte única do histórico e do estado
│  ├─ roadmap/index.html          GERADO; layout do protótipo "docs" (Alabaster Forge)
│  └─ superpowers/specs/ plans/
└─ scripts/
   ├─ roadmap.py                  build (json → STATUS.md + index.html) e validate
   ├─ check-tokens.sh             falha se achar cor hex fora do palette.json em QML/CSS/SVG próprio
   ├─ check-agents-sync.sh        falha se .claude/commands divergir das seções de AGENTS.md
   └─ check-branding.sh           stub documentado; implementação real = tarefa Fase 0
```

## 4. Componentes

### 4.1 `AGENTS.md` (fonte única) e `CLAUDE.md`

- `AGENTS.md` na raiz: identidade do projeto (3 linhas), onde estão PRD/METHODOLOGY/DESIGN-RULES/STATUS, regras invioláveis (D1, D2, tiers do Policy Engine não se tocam, nada de `rm` no histórico), o fluxo em 5 etapas com os comandos de verificação, convenções de branch/commit/PR, e a regra de atualização do roadmap a cada entrega.
- `CLAUDE.md`: `@AGENTS.md` mais o mapeamento das etapas para `/plan`, `/code`, `/test`, `/review`, `/ship`.
- `AGENTS.md` por pasta de componente: só o que muda ali (linguagem, como rodar testes, DoD local). Codex e Claude Code leem hierarquicamente.
- Idioma: regras em pt-BR (idioma do time); nomes de arquivo, código e commits em inglês (PRD regra 4).

### 4.2 `.claude/commands/*.md`

Cinco comandos. Cada um é um prompt curto que (a) cita a seção correspondente de `docs/dev/METHODOLOGY.md`, (b) lista as pré-condições, (c) lista os scripts que devem passar. `check-agents-sync.sh` compara o bloco entre marcadores `<!-- flow:start -->`/`<!-- flow:end -->` de `AGENTS.md` com a concatenação dos comandos e falha em divergência.

### 4.3 `docs/dev/METHODOLOGY.md`

Cinco gates, nenhum pulável, cada um com entrada, saída, checklist e script:

1. **plan** — entrada: spec aprovada ou issue com `FR-xxx`. Saída: `docs/superpowers/plans/AAAA-MM-DD-<slug>.md` com tarefas ≤ 2 h, cada tarefa com arquivos, teste que prova e critério de pronto. Sem plano, sem branch.
2. **code** — branch `feat/FR-xxx-slug` (ou `fix/`, `adr/`, `docs/`). TDD em Rust e shell: teste falhando → implementação mínima → verde → refatorar. Commits convencionais (`feat(hero): …`), um commit por tarefa do plano. Para tela: começa por `docs/design-system/telas/<slug>.md`, nunca pelo `code.html`.
3. **test** — `cargo test`/`bats`/`shellcheck` conforme a pasta; `scripts/check-tokens.sh` quando há QML/CSS/SVG; captura de tela lado a lado (protótipo × implementação) anexada ao PR quando há tela; cobertura ≥ 70 % nos crates (NFR-041).
4. **review** — **revisão cruzada:** quem implementou não revisa. Claude Code implementa → Codex revisa, ou o inverso; o revisor roda `scripts/check-*.sh` e o checklist fixo (D1/D2, FR referenciado, testes, segurança, consumo declarado). Achados viram commits na mesma branch; a revisão só fecha quando o checklist está 100 %.
5. **ship** — PR pelo template; CI verde; *squash merge*; **no mesmo PR**: `scripts/roadmap.py` recebe a entrega (`add-delivery`) e regenera `STATUS.md` + `roadmap/index.html`. PR sem atualização de roadmap é bloqueado pelo template/checklist.

### 4.4 Design system

- `brand/palette.json`: tokens de cor (dark/light), tipografia (escala, famílias, pesos), raio, espaçamento, elevação/blur, dimensões fixas (overlay 520 px, dock 64 px, barra 40 px), semântica (success/warning/error/info/ai/mascot). Derivado dos `DESIGN.md` de Forge e Alabaster; onde eles divergem das telas, a tela do protótipo mais recente vence e a divergência fica anotada.
- `DESIGN-RULES.md`: princípios (nada genérico: zero Breeze padrão visível, zero cor fora do palette, zero fonte fora da lista); tabela de tradução token → CSS var → QML (`Kirigami.Theme`, `color scheme`) → KColorScheme (`.colors`) → Plymouth script → GRUB theme → Konsole `.colorscheme`; regras de ícone (Material Symbols no protótipo ↔ Breeze/próprio no produto, com tabela de equivalência por tela); grade 8 px; estados do mascote; acessibilidade AA (NFR-050); DoD visual.
- `telas/<slug>.md` (16 arquivos): FR de origem, tecnologia-alvo (QML/Plasma, SDDM QML, Plymouth, GRUB, Konsole, Astro/site, CLI), arquivos fonte (`code.html`, `screen.png`), inventário de regiões (o que é layout → copia; o que é conteúdo → PRD), substituições obrigatórias (`Jarvis`→`Guará`, `devos`→`forja`, `nftables`→`firewalld`, `24.04 LTS`→versão `AAAA.MM.DD`/`vX.Y`, `arm64`→remover, `Kernel 6.12`→"kernel Bazzite"), tokens usados, checklist de fidelidade, pendências conhecidas.

### 4.5 Roadmap e status

- `roadmap.json`: `{ project, updated_at, phases[ {id, name, weeks, dod, status} ], items[ {id, fr[], phase, title, status: todo|doing|done|blocked, pr?, merged_at?, notes?} ], deliveries[ {date, pr, items[], summary} ] }`.
- `scripts/roadmap.py build`: valida o schema (sem dependências externas, Python 3 stdlib), gera `docs/STATUS.md` (fase atual, feito, em andamento, **próxima tarefa**, bloqueios) e `docs/roadmap/index.html`.
- `index.html`: um arquivo, offline. Layout e tokens do protótipo `forjaos_docs_documenta_o_t_cnica_oficial` (Alabaster Forge) traduzidos para CSS estático — sem Tailwind CDN. Fontes via Google Fonts com fallback de sistema. Seções: cabeçalho fixo, menu lateral por fase, banner com fase atual, "Feito", "Onde estamos", "Falta fazer", linha do tempo de entregas, tabela por FR. Dados embutidos como `<script type="application/json">` gerado — agente nunca edita o HTML à mão.
- `roadmap.py add-delivery --pr N --items FR-… --summary "…"` é o comando que o gate *ship* exige.

### 4.6 ADRs e PRD

- ADR-026 (monorepo, revoga §5.2), ADR-027 (tokens canônicos; Obsidian aposentado; fontes), ADR-028 (precedência protótipo × PRD). Formato da §14.1 do PRD.
- PRD: §5.2 recebe nota "revogada por ADR-026 — ver `docs/adr/0026`"; cabeçalho ganha linha `Status operacional: ver docs/STATUS.md`. Nada mais é editado no PRD (regra "ADR revoga ADR").

## 5. Fora de escopo (esta entrega)

Containerfile, workflows do GitHub Actions, `check-branding.sh` real, qualquer código Rust/QML, reescrita dos `code.html` dos protótipos, site Astro.

## 6. Critérios de pronto desta entrega

- [ ] `python3 scripts/roadmap.py build` roda limpo e gera `STATUS.md` e `index.html` idênticos aos commitados.
- [ ] `scripts/check-agents-sync.sh` e `scripts/check-tokens.sh` executam e passam no estado atual.
- [ ] `index.html` abre offline e reproduz a hierarquia visual do protótipo docs (cabeçalho 64 px, sidebar 288 px, banner, cards, tabela, TOC à direita).
- [ ] 16 specs de tela presentes, cada uma com as substituições obrigatórias listadas.
- [ ] `CLAUDE.md` contém `@AGENTS.md`; `AGENTS.md` não referencia nada que não exista no repositório.
- [ ] Commit único por grupo lógico, mensagens convencionais, tudo em `main` (sem PR nesta entrega inicial — não há CI ainda; a partir da Fase 0 o gate *ship* vale integralmente).

## 7. Riscos

| Risco | Mitigação |
| --- | --- |
| Agente ignora o fluxo e vai direto ao código | `AGENTS.md` abre com os gates; PR template exige link do plano; `check-agents-sync.sh` no CI da Fase 0 |
| Tokens do `palette.json` divergem das telas ao longo do tempo | `check-tokens.sh` + regra: alterar token = ADR |
| Specs de tela ficam desatualizadas quando o protótipo é regenerado | Cada spec registra hash SHA-256 do `code.html` de origem; `roadmap.py validate` avisa se mudou |
| `STATUS.md`/HTML editados à mão | Cabeçalho "GERADO — não editar"; `roadmap.py build --check` falha se o commitado difere do gerado |
