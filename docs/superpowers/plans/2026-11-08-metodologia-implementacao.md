# Metodologia executável — Plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar a governança executável do ForjaOS: `AGENTS.md`/`CLAUDE.md`, comandos por etapa, metodologia, design system canônico com spec por tela, roadmap gerado (JSON → STATUS.md + HTML) e scripts de verificação — conforme `docs/superpowers/specs/2026-11-08-metodologia-implementacao-design.md`.

**Architecture:** Monorepo com pastas por componente. `AGENTS.md` é a fonte única de regras (Codex nativo; Claude Code via `@AGENTS.md`). `brand/palette.json` é a fonte única de tokens. `docs/roadmap/roadmap.json` é a fonte única de estado; `scripts/roadmap.py` gera `STATUS.md` e `roadmap/index.html`. Scripts `check-*.sh` fazem as regras verificáveis.

**Tech Stack:** Markdown, JSON, Python 3.10 stdlib (sem dependências), Bash 5, HTML/CSS estático (sem CDN). Testes: `unittest` (Python) e scripts bash em `scripts/tests/`.

**Ambiente de execução:** arquivos vivem em `C:\Desenv\Projetos\rrb-forjaOS` (montado em `$HOME/mnt/rrb-forjaOS` no `device_bash`). Sem `shellcheck`/`bats` disponíveis; testes de shell são bash puro.

---

## Mapa de arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `AGENTS.md` | Regras de agente (fonte única). Bloco `<!-- flow:start -->…<!-- flow:end -->` espelha os comandos |
| `CLAUDE.md` | `@AGENTS.md` + mapeamento de slash commands |
| `.claude/commands/{plan,code,test,review,ship}.md` | Um prompt por gate |
| `{image,cli,hero,hero-mcp,hero-memory,brand,site}/AGENTS.md` | Escopo local, linguagem, testes, DoD |
| `.github/PULL_REQUEST_TEMPLATE.md` | Checklist dos gates + link do plano + roadmap atualizado |
| `brand/palette.json` | Tokens (dark/light, tipografia, raio, espaçamento, elevação, dimensões, semântica) |
| `docs/adr/0026-monorepo.md`, `0027-design-tokens-canonicos.md`, `0028-precedencia-prototipo-prd.md` | Decisões D3, D2, D1 |
| `docs/PRD.md` | Nota de revogação em §5.2; linha de status no cabeçalho |
| `docs/dev/METHODOLOGY.md` | 5 gates, entrada/saída/checklist/script |
| `docs/design-system/DESIGN-RULES.md` | Regras, tabela de tradução, ícones, DoD visual |
| `docs/design-system/telas/<slug>.md` ×16 | Spec por protótipo |
| `docs/roadmap/roadmap.json` | Estado e histórico |
| `docs/roadmap/index.html`, `docs/STATUS.md` | Gerados |
| `scripts/roadmap.py` | `build`, `build --check`, `validate`, `add-delivery` |
| `scripts/roadmap_template.html` | Template HTML com placeholders `{{...}}` |
| `scripts/check-tokens.sh` | Hex fora do palette em QML/CSS/SVG/HTML próprio → falha |
| `scripts/check-agents-sync.sh` | Bloco flow do AGENTS.md ≡ concatenação dos comandos |
| `scripts/check-branding.sh` | Stub: imprime o que fará e sai 0 |
| `scripts/tests/test_roadmap.py`, `scripts/tests/test_check_tokens.sh`, `scripts/tests/test_check_agents_sync.sh` | Testes |

---

### Task 1: Esqueleto do monorepo + ADRs + nota no PRD

**Files:**
- Create: `image/.gitkeep`, `cli/.gitkeep`, `hero/.gitkeep`, `hero-mcp/.gitkeep`, `hero-memory/.gitkeep`, `brand/.gitkeep`, `site/.gitkeep`, `docs/adr/`, `docs/dev/`, `docs/design-system/telas/`, `docs/roadmap/`, `scripts/tests/`, `.claude/commands/`, `.github/`
- Create: `docs/adr/0026-monorepo.md`, `docs/adr/0027-design-tokens-canonicos.md`, `docs/adr/0028-precedencia-prototipo-prd.md`
- Modify: `docs/PRD.md` (cabeçalho: tabela; §5.2: nota)

- [ ] **Step 1: Criar pastas**

```bash
cd "$HOME/mnt/rrb-forjaOS"
mkdir -p image cli hero hero-mcp hero-memory brand site docs/adr docs/dev docs/design-system/telas docs/roadmap scripts/tests .claude/commands .github
for d in image cli hero hero-mcp hero-memory brand site; do touch "$d/.gitkeep"; done
```

- [ ] **Step 2: Escrever os 3 ADRs** (formato §14.1: Contexto · Decisão · Alternativas · Consequências · Status)

`docs/adr/0026-monorepo.md`: contexto = equipe solo, 7 repos = 7 CIs, 7 releases, versionamento cruzado; decisão = monorepo `rrb-forjaOS` com pastas `image/ cli/ hero/ hero-mcp/ hero-memory/ brand/ site/`, cada uma com `AGENTS.md` e release por tag prefixada (`cli-v0.1.0`, `hero-v0.1.0`, `image-2026.11.08`); alternativas = 7 repos (PRD §5.2), git submodules; consequências = revoga tabela §5.2 do PRD; `forjaos-image` → `image/` etc.; separação futura via `git subtree split`; Status = `aceito`.

`docs/adr/0027-design-tokens-canonicos.md`: contexto = 3 DESIGN.md e telas com fontes inconsistentes; decisão = dark *Cybernetic Forge*, light *Alabaster Forge*, `brand/palette.json` fonte única, JetBrains Mono para mono, Plus Jakarta Sans para UI, Inter só em body de dados densos, Fira Code proibida, *Cybernetic Obsidian* aposentado (mantido em `docs/telas/design/` só como histórico); alternativas = Obsidian, manter 3; consequências = `check-tokens.sh`; alterar token exige ADR; Status = `aceito`.

`docs/adr/0028-precedencia-prototipo-prd.md`: contexto = protótipos com `Jarvis`, `devos`, `nftables`, `24.04 LTS`, `arm64`, `Kernel 6.12`; decisão = layout/hierarquia/tokens/espaçamento/animação do protótipo; texto/nomes/comandos/versões/componentes do PRD; divergência vira issue com label `area/brand` e nunca improviso; tabela de substituições obrigatórias (Jarvis→Guará/HERO, devos→forja, devos-term→forja-term, nftables→firewalld, 24.04 LTS→`AAAA.MM.DD`/`vX.Y.Z`, arm64→remover, Kernel 6.12.x→"kernel Bazzite", "Escudo ativo" só se `forja install escudo`); Status = `aceito`.

- [ ] **Step 3: Editar o PRD** — adicionar linha na tabela do cabeçalho `| Status operacional | ver docs/STATUS.md (gerado) e docs/roadmap/index.html |` e, logo abaixo do título `### 5.2 Repositórios`, o parágrafo: `> **Revogado por ADR-026 (2026-11-08):** o projeto é um monorepo em rrb-forjaOS; a tabela abaixo permanece como registro histórico. Mapeamento: forjaos-image → image/, forja-cli → cli/, hero → hero/, hero-mcp → hero-mcp/, hero-memory → hero-memory/, forjaos-brand → brand/, forjaos-site → site/.`

- [ ] **Step 4: Verificar**

Run: `grep -c "Revogado por ADR-026" docs/PRD.md && ls docs/adr`
Expected: `1` e os 3 arquivos.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "adr: monorepo (026), canonical design tokens (027), prototype vs PRD precedence (028)"
```

---

### Task 2: `brand/palette.json` + `scripts/check-tokens.sh`

**Files:**
- Create: `brand/palette.json`, `scripts/check-tokens.sh`, `scripts/tests/test_check_tokens.sh`

- [ ] **Step 1: Escrever o teste do script**

`scripts/tests/test_check_tokens.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/hero/ui"
# caso 1: cor do palette -> passa
printf 'Rectangle { color: "#00e5ff" }\n' > "$TMP/hero/ui/ok.qml"
if ! "$ROOT/scripts/check-tokens.sh" "$TMP"; then echo "FAIL: cor válida reprovada"; exit 1; fi
# caso 2: cor fora do palette -> falha
printf 'Rectangle { color: "#ff00aa" }\n' > "$TMP/hero/ui/bad.qml"
if "$ROOT/scripts/check-tokens.sh" "$TMP"; then echo "FAIL: cor inválida aprovada"; exit 1; fi
# caso 3: docs/telas é ignorado
mkdir -p "$TMP/docs/telas/x"; rm "$TMP/hero/ui/bad.qml"
printf '<div style="color:#ff00aa">' > "$TMP/docs/telas/x/code.html"
if ! "$ROOT/scripts/check-tokens.sh" "$TMP"; then echo "FAIL: docs/telas não foi ignorado"; exit 1; fi
echo "PASS test_check_tokens"
```

- [ ] **Step 2: Rodar — deve falhar** (`scripts/check-tokens.sh` não existe)

Run: `bash scripts/tests/test_check_tokens.sh`
Expected: erro "No such file".

- [ ] **Step 3: Escrever `brand/palette.json`**

Estrutura (valores vêm de `docs/telas/design/cybernetic_forge/DESIGN.md` e `alabaster_forge/DESIGN.md`, mais os valores de superfície que o corpo dos DESIGN.md e as telas usam — `#0A0D14`, `#10141E`, `#161B26`, `#1E2433`, `#070A11`, `#00E5FF`, `#38BDF8`, `#8B5CF6`, `#6366F1`, `#F97316`, `#FB923C`, `#10B981`, `#F43F5E`, `#F59E0B`, `#0EA5E9`, `#94A3B8`, `#F1F5F9`; light: `#f8fafc`, `#ffffff`, `#f1f5f9`, `#e2e8f0`, `#cbd5e1`, `#0284c7`, `#4f46e5`, `#ea580c`, `#0f172a`, `#334155`, `#64748b`, `#e0f2fe`):

```json
{
  "$schema": "./palette.schema.json",
  "name": "ForjaOS",
  "version": "1.0.0",
  "adr": "ADR-027",
  "themes": {
    "dark":  { "name": "Cybernetic Forge", "source": "docs/telas/design/cybernetic_forge/DESIGN.md", "colors": { "...": "tokens m3 + surface.*, accent.*, semantic.*" } },
    "light": { "name": "Alabaster Forge",  "source": "docs/telas/design/alabaster_forge/DESIGN.md",  "colors": { "...": "idem" } }
  },
  "typography": { "families": { "ui": "Plus Jakarta Sans", "mono": "JetBrains Mono", "dense": "Inter" }, "forbidden": ["Fira Code"], "scale": { "display-lg": {...}, "...": {} } },
  "radius": { "sm": 4, "md": 8, "lg": 12, "xl": 16, "full": 9999 },
  "spacing": { "unit": 8, "xs": 4, "sm": 8, "md": 12, "lg": 20, "xl": 32, "gutter": 12, "margin": 16 },
  "elevation": { "dark": { "L1": {...}, "L2": {...}, "L3": {...} }, "light": { "L1": {...}, "L2": {...}, "L3": {...} } },
  "dimensions": { "overlay_width": 520, "topbar_height": 40, "dock_height": 64, "dock_bottom_offset": 12, "toolbar_compact": 40, "toolbar_standard": 48, "tree_row": 28, "chip_height": 22 },
  "mascot": { "states": ["idle","listening","thinking","speaking","error"], "accent": "#F97316" }
}
```
(Na execução, cada `{...}` é preenchido com os valores literais dos DESIGN.md; nenhum `{...}` pode sobrar no arquivo final.)

- [ ] **Step 4: Escrever `scripts/check-tokens.sh`**

```bash
#!/usr/bin/env bash
# Falha se encontrar cor hex (#rgb/#rrggbb/#rrggbbaa) fora de brand/palette.json
# em arquivos próprios (.qml .css .scss .svg .html .colors .colorscheme .json .toml .rs .py).
# Ignora: docs/telas (protótipos históricos), .git, node_modules, target, brand/palette.json.
set -euo pipefail
ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
PALETTE="$(cd "$(dirname "$0")/.." && pwd)/brand/palette.json"
[[ -f "$PALETTE" ]] || { echo "check-tokens: palette não encontrado em $PALETTE"; exit 2; }
allowed="$(grep -oiE '#[0-9a-f]{6}([0-9a-f]{2})?|#[0-9a-f]{3}\b' "$PALETTE" | tr 'A-F' 'a-f' | sort -u)"
status=0
while IFS= read -r -d '' f; do
  while IFS= read -r hex; do
    h="$(printf '%s' "$hex" | tr 'A-F' 'a-f')"
    if ! grep -qx "$h" <<<"$allowed"; then
      echo "check-tokens: $f: cor fora do palette: $hex"; status=1
    fi
  done < <(grep -oiE '#[0-9a-f]{6}([0-9a-f]{2})?\b|#[0-9a-f]{3}\b' "$f" || true)
done < <(find "$ROOT" \( -path '*/.git' -o -path '*/docs/telas' -o -path '*/node_modules' -o -path '*/target' -o -path '*/brand/palette.json' -o -path '*/docs/roadmap/index.html' -o -path '*/scripts/roadmap_template.html' \) -prune -o -type f \( -name '*.qml' -o -name '*.css' -o -name '*.scss' -o -name '*.svg' -o -name '*.html' -o -name '*.colors' -o -name '*.colorscheme' -o -name '*.toml' -o -name '*.rs' -o -name '*.py' \) -print0)
[[ $status -eq 0 ]] && echo "check-tokens: OK"
exit $status
```
(`index.html` e o template são gerados a partir do palette; excluídos para não duplicar a checagem — o teste do `roadmap.py` garante que só usam tokens.)

- [ ] **Step 5: Rodar o teste**

Run: `chmod +x scripts/*.sh scripts/tests/*.sh && bash scripts/tests/test_check_tokens.sh`
Expected: `PASS test_check_tokens`

- [ ] **Step 6: Validar JSON**

Run: `python3 -c "import json;d=json.load(open('brand/palette.json'));print(len(d['themes']['dark']['colors']),len(d['themes']['light']['colors']))"`
Expected: dois inteiros ≥ 40; nenhum erro.

- [ ] **Step 7: Commit**

```bash
git add brand/palette.json scripts/check-tokens.sh scripts/tests/test_check_tokens.sh
git commit -m "feat(brand): canonical palette.json and check-tokens script (ADR-027)"
```

---

### Task 3: `docs/dev/METHODOLOGY.md`

**Files:**
- Create: `docs/dev/METHODOLOGY.md`

- [ ] **Step 1: Escrever o documento** com estas seções, nesta ordem, cada gate com os quatro blocos **Entrada / Saída / Checklist / Comando de verificação**:

0. *Por que existe* (3 linhas) e *Regras invioláveis*: nenhum gate é pulado; quem implementa não revisa; PRD manda no conteúdo, protótipo no layout (ADR-028); tokens só do palette (ADR-027); nada de `rm`/`dd`/firewall fora do tier (FR-093); roadmap atualizado no mesmo PR.
1. **plan** — Entrada: spec aprovada em `docs/superpowers/specs/` ou issue com `FR-xxx`. Saída: `docs/superpowers/plans/AAAA-MM-DD-<slug>.md` (header do writing-plans; tarefas ≤ 2 h; cada tarefa: arquivos exatos, teste que prova, DoD). Checklist: cada tarefa cita um `FR-`/`NFR-`/`ADR-`; tela → cita `docs/design-system/telas/<slug>.md`; nenhum "TBD". Comando: `grep -L "FR-\|NFR-\|ADR-" docs/superpowers/plans/<arquivo>` deve ser vazio.
2. **code** — Branch `feat|fix|adr|docs/FR-xxx-slug`. TDD: teste falha → mínimo → passa → refatora; um commit por tarefa; commits convencionais `tipo(escopo): resumo` com escopo = pasta (`image`, `cli`, `hero`, `hero-mcp`, `hero-memory`, `brand`, `site`, `docs`). Para telas: ler a spec da tela **antes** do `code.html`; aplicar a tabela de substituições; copiar medidas, nunca cores soltas. Comando: `git log --format=%s origin/main..HEAD | grep -vE '^(feat|fix|adr|docs|test|chore|refactor)\([a-z-]+\): '` vazio.
3. **test** — por pasta: Rust `cargo test && cargo clippy -- -D warnings && cargo fmt --check`; Shell `bash scripts/tests/*.sh`; Python `python3 -m unittest discover -s scripts/tests`; QML/CSS/SVG `scripts/check-tokens.sh`; tela → captura lado a lado `docs/design-system/telas/<slug>/compare-AAAA-MM-DD.png` (protótipo esquerda, implementação direita, mesma resolução) anexada ao PR; cobertura ≥ 70 % (`cargo llvm-cov`) nos crates (NFR-041).
4. **review** — Revisão cruzada: a sessão que implementou abre o PR e **para**; outra ferramenta (Claude Code ↔ Codex) revisa com o checklist: (a) FR coberto, (b) ADR-028 aplicado, (c) tokens só do palette, (d) testes existem e provam o comportamento, (e) consumo declarado (`MemoryMax`, `CPUQuota`) em qualquer unit systemd, (f) nenhum segredo/chave em arquivo, (g) SELinux/firewall intocados fora de tier, (h) roadmap atualizado. Achado → commit na branch com prefixo `fix(review):`. Revisão fecha com comentário "review: 8/8".
5. **ship** — PR pelo template; CI verde (a partir da Fase 0); *squash merge*; `python3 scripts/roadmap.py add-delivery --pr N --items FR-xxx,... --summary "..."` → `python3 scripts/roadmap.py build` → commit `docs(roadmap): deliver PR #N`. Sem isso o PR não mergeia.
6. *Mapa de comandos*: tabela gate → `/plan /code /test /review /ship` (Claude Code) → seção equivalente do `AGENTS.md` (Codex).
7. *Exceções*: hotfix de segurança pode pular *plan* mas não *test/review*; registra no PR "hotfix: motivo".

- [ ] **Step 2: Verificar que todo gate tem os 4 blocos**

Run: `grep -c "^\*\*Entrada" docs/dev/METHODOLOGY.md; grep -c "^\*\*Comando" docs/dev/METHODOLOGY.md`
Expected: `5` e `5`.

- [ ] **Step 3: Commit**

```bash
git add docs/dev/METHODOLOGY.md && git commit -m "docs(dev): implementation methodology with five mandatory gates"
```

---

### Task 4: `docs/design-system/DESIGN-RULES.md`

**Files:**
- Create: `docs/design-system/DESIGN-RULES.md`

- [ ] **Step 1: Escrever** com as seções:

1. *Fonte da verdade*: `brand/palette.json`; `docs/telas/*/screen.png` + `code.html` = referência de layout; `DESIGN.md` de Forge/Alabaster = racional. Precedência ADR-028.
2. *Proibições ("nada de tela genérica")*: Breeze padrão visível em qualquer superfície própria; cor hex fora do palette; fontes fora de {Plus Jakarta Sans, JetBrains Mono, Inter(dense)}; `#000000` puro; pill `rounded-full` fora de toggles/status dots; ícones Material Symbols no produto (só no protótipo); texto `Jarvis`/`devos`; placeholders lorem.
3. *Grade e dimensões*: unidade 8 px (4 px micro); raio 8 px padrão, 4 px aninhado, 12–16 px shells flutuantes; overlay 520 px, barra superior 40 px, dock 64 px a 12 px da borda, linha de árvore 28 px, chip 22 px.
4. *Tabela de tradução de tokens* (uma linha por token principal): `palette.json` → CSS var (`--fj-surface-l1`) → QML (`Kirigami.Theme.backgroundColor` / propriedade em `brand/qml/ForjaTheme.qml`) → KColorScheme (`[Colors:Window] BackgroundNormal=`) → Konsole `.colorscheme` (`[Background] Color=`) → Plymouth script (`Window.SetBackgroundTopColor`) → GRUB theme (`desktop-color`, `selected_item_color`) → Tailwind (site).
5. *Ícones*: protótipo usa Material Symbols; produto usa Breeze (KDE) **recolorido pelos tokens** ou SVG próprio em `brand/icons/`; tabela de equivalência mantida em cada spec de tela.
6. *Tipografia*: escala completa do palette com uso (display → títulos de wizard/landing; headline-sm → títulos de janela; label-sm uppercase 0.04em → status; code-md → telemetria; números tabulares obrigatórios em métricas).
7. *Elevação*: L1/L2/L3 por tema (valores do palette), blur 12/16/24 px, borda ghost `rgba(255,255,255,0.08)` → ativa `rgba(0,229,255,0.35)`.
8. *Mascote*: 5 estados, cor de acento `#F97316`, camadas SVG nomeadas (`eyes`, `mouth`, `ears`, `body`, `glow`) conforme FR-054; visemes 12–15.
9. *Acessibilidade*: contraste AA (checar pares no palette: `on-surface`/`surface` etc.), navegação por teclado, foco visível `0 0 0 3px` no tom primário.
10. *DoD visual*: (a) captura lado a lado na mesma resolução; (b) `check-tokens.sh` OK; (c) medidas-chave conferidas na spec da tela; (d) tabela de substituições aplicada; (e) revisor cruzado marca "visual: fiel".
11. *Como ler uma spec de tela* (estrutura do template da Task 5).

- [ ] **Step 2: Verificar seções**

Run: `grep -c '^## ' docs/design-system/DESIGN-RULES.md`
Expected: `11`.

- [ ] **Step 3: Commit**

```bash
git add docs/design-system/DESIGN-RULES.md && git commit -m "docs(design): design rules, token translation table and visual DoD"
```

---

### Task 5: Specs das 16 telas

**Files:**
- Create: `docs/design-system/telas/_TEMPLATE.md` e 16 arquivos `docs/design-system/telas/<slug>.md`

- [ ] **Step 1: Template**

```markdown
# Tela: <nome legível>

| Campo | Valor |
| --- | --- |
| Slug | `<slug>` |
| Protótipo | `docs/telas/<slug>/code.html` (sha256 `<12 hex>`) · `screen.png` |
| Requisitos | FR-xxx, … |
| Tema | dark (Cybernetic Forge) / light (Alabaster Forge) |
| Tecnologia-alvo | … |
| Pasta do monorepo | … |
| Status | spec · em implementação · implementada (PR #) |

## Regiões (layout → copiar)
| Região | Medidas/tokens | Observação |

## Conteúdo (PRD → substituir)
| No protótipo | Na implementação | Fonte |

## Ícones
| Material Symbol | Breeze / próprio |

## Checklist de fidelidade
- [ ] …

## Pendências e divergências conhecidas
```

- [ ] **Step 2: Tabela-mestra das 16 telas** (usar para preencher cada spec; hash = `sha256sum docs/telas/<slug>/code.html | cut -c1-12`):

| Slug | FR | Tema | Tecnologia-alvo | Pasta |
| --- | --- | --- | --- | --- |
| forjaos_splash_plymouth | FR-056 | dark | Plymouth theme (script) | brand/plymouth |
| forjaos_bootloader_grub | FR-002, FR-008 | dark | GRUB theme (`theme.txt`, PNGs) | brand/grub |
| forjaos_sddm_login | FR-057 | dark | SDDM theme QML | brand/sddm |
| forjaos_desktop_principal_dock | FR-050, FR-052 | dark | Plasma 6: look-and-feel, painel, dock (layout.js), wallpaper | brand/plasma + image/system_files |
| forjaos_desktop_principal_modo_claro_alabaster_forge | FR-050, FR-052 | light | idem, variante clara | brand/plasma |
| forjaos_central_de_comando_hero_overlay | FR-121, FR-103 | dark | Overlay QML (versão anterior; usar só como referência de animação/waveform) | hero/overlay |
| forjaos_central_de_comando_hero_corrigida | FR-121, FR-103, FR-093 | dark | Overlay QML 520 px — **versão canônica** | hero/overlay |
| forjaos_plasmoid_do_guar_kde_plasma_6 | FR-120, FR-123, FR-054 | dark | Plasmoid QML + popup | hero/plasmoid |
| forjaos_terminal_konsole_dev_forja_doctor | FR-035, FR-036, FR-061 | dark | Konsole colorscheme + profile; saída do `forja doctor`/`forja ai` | brand/konsole + cli |
| forjaos_file_explorer_especializado_dev_edition | **sem FR** — abrir issue/ADR antes de implementar | dark | Dolphin (service menus, places, cor) | — |
| forjaos_wizard_de_primeiro_boot | FR-020, FR-021, FR-022, FR-023 | dark | Wizard QML tela cheia | image/firstboot |
| forjaos_wizard_de_primeiro_boot_passo_6_resumo_conclus_o | FR-020, FR-024 | dark | Wizard QML passo 6 | image/firstboot |
| forjaos_visualizador_de_mem_ria_linha_do_tempo_di_ria | FR-135, FR-131 | dark | App QML (linha do tempo) | hero-memory/viewer |
| forjaos_visualizador_do_grafo_da_mem_ria_fr_135 | FR-135, FR-134 | dark | App QML (grafo força-dirigida) | hero-memory/viewer |
| forjaos_docs_documenta_o_t_cnica_oficial | NFR-043 | light | Site de docs (Astro) + layout do roadmap.html | site/docs |
| forjaos_o_sistema_operacional_para_quem_desenvolve_e_joga | G1, NFR-043 | light | Landing page (Astro) | site/landing |

- [ ] **Step 3: Para cada tela, ler `code.html` (regiões, medidas, classes Tailwind → tokens) e `screen.png`, preencher a spec.** Substituições mínimas a procurar em todas: `Jarvis`, `devos`, `nftables`, `24.04`, `arm64`, `6.12`, `RTX 4070` (máquina de referência é RTX 5060 — §10.2), `rodrigo@devos` → `usuario@forjaos`, `GameMode on` → `hero-game.target`, `Escudo ativo` (só com Escudo instalado). Registrar cada ocorrência achada com `grep -o`.

- [ ] **Step 4: Verificar**

Run: `ls docs/design-system/telas/*.md | wc -l; grep -L "sha256" docs/design-system/telas/forjaos_*.md`
Expected: `17` (16 + template) e lista vazia.

- [ ] **Step 5: Commit**

```bash
git add docs/design-system/telas && git commit -m "docs(design): per-screen fidelity specs for the 16 prototypes"
```

---

### Task 6: `scripts/roadmap.py` + `roadmap.json` + template HTML + gerados

**Files:**
- Create: `scripts/tests/test_roadmap.py`, `scripts/roadmap.py`, `scripts/roadmap_template.html`, `docs/roadmap/roadmap.json`
- Generate: `docs/STATUS.md`, `docs/roadmap/index.html`

- [ ] **Step 1: Teste**

`scripts/tests/test_roadmap.py`:
```python
import json, subprocess, sys, tempfile, unittest, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import roadmap  # noqa: E402

SAMPLE = {
  "project": "ForjaOS", "updated_at": "2026-11-08",
  "phases": [{"id": "0", "name": "Fundação", "weeks": "1–2", "dod": "Imagem builda", "status": "doing"},
             {"id": "1", "name": "Imagem instalável", "weeks": "3–8", "dod": "Pendrive → dual boot", "status": "todo"}],
  "items": [{"id": "GOV-001", "fr": ["ADR-026"], "phase": "0", "title": "Metodologia", "status": "done", "pr": None, "merged_at": "2026-11-08"},
            {"id": "F0-001", "fr": ["FR-001"], "phase": "0", "title": "Containerfile mínimo", "status": "todo"}],
  "deliveries": [{"date": "2026-11-08", "pr": None, "items": ["GOV-001"], "summary": "Governança"}]
}

class RoadmapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()); (self.tmp/"docs"/"roadmap").mkdir(parents=True)
        self.json = self.tmp/"docs"/"roadmap"/"roadmap.json"; self.json.write_text(json.dumps(SAMPLE), encoding="utf-8")
    def tearDown(self): shutil.rmtree(self.tmp)
    def test_validate_ok(self): self.assertEqual(roadmap.validate(SAMPLE), [])
    def test_validate_bad_status(self):
        bad = json.loads(json.dumps(SAMPLE)); bad["items"][0]["status"] = "maybe"
        self.assertTrue(any("status" in e for e in roadmap.validate(bad)))
    def test_validate_unknown_phase(self):
        bad = json.loads(json.dumps(SAMPLE)); bad["items"][0]["phase"] = "9"
        self.assertTrue(any("phase" in e for e in roadmap.validate(bad)))
    def test_next_task_is_first_todo_of_current_phase(self):
        self.assertEqual(roadmap.next_task(SAMPLE)["id"], "F0-001")
    def test_status_md_contains_sections(self):
        md = roadmap.render_status(SAMPLE)
        for s in ("GERADO", "Fase atual", "Feito", "Em andamento", "Próxima tarefa", "F0-001"): self.assertIn(s, md)
    def test_html_is_self_contained_and_has_data(self):
        html = roadmap.render_html(SAMPLE, (ROOT/"scripts"/"roadmap_template.html").read_text(encoding="utf-8"))
        self.assertNotIn("cdn.tailwindcss.com", html)
        self.assertIn('type="application/json"', html); self.assertIn("F0-001", html); self.assertNotIn("{{", html)
    def test_build_writes_and_check_detects_drift(self):
        roadmap.build(self.tmp); status = self.tmp/"docs"/"STATUS.md"; self.assertTrue(status.exists())
        self.assertEqual(roadmap.check(self.tmp), 0)
        status.write_text(status.read_text(encoding="utf-8") + "\nedit manual\n", encoding="utf-8")
        self.assertEqual(roadmap.check(self.tmp), 1)
    def test_add_delivery_marks_items_done(self):
        roadmap.add_delivery(self.tmp, pr=7, items=["F0-001"], summary="Containerfile", date="2026-11-09")
        d = json.loads(self.json.read_text(encoding="utf-8"))
        self.assertEqual(d["items"][1]["status"], "done"); self.assertEqual(d["items"][1]["pr"], 7)
        self.assertEqual(d["deliveries"][-1]["pr"], 7); self.assertEqual(d["updated_at"], "2026-11-09")

if __name__ == "__main__": unittest.main()
```

- [ ] **Step 2: Rodar — deve falhar** (`import roadmap` falha)

Run: `python3 -m unittest discover -s scripts/tests -p 'test_*.py' -v`
Expected: `ModuleNotFoundError: roadmap`.

- [ ] **Step 3: Escrever `scripts/roadmap.py`** com a API usada no teste:

```python
#!/usr/bin/env python3
"""roadmap.py — fonte única: docs/roadmap/roadmap.json → docs/STATUS.md + docs/roadmap/index.html
Uso: roadmap.py validate | build [--check] | add-delivery --pr N --items A,B --summary "..." [--date AAAA-MM-DD]
Só stdlib. Nunca edite os arquivos gerados à mão."""
import argparse, json, sys, datetime, html
from pathlib import Path
STATUSES = ("todo", "doing", "done", "blocked")
GEN = "<!-- GERADO por scripts/roadmap.py a partir de docs/roadmap/roadmap.json — NÃO EDITAR À MÃO -->"

def load(root: Path) -> dict: ...
def save(root: Path, data: dict) -> None: ...        # json.dumps(indent=2, ensure_ascii=False) + "\n"
def validate(data: dict) -> list[str]: ...           # campos obrigatórios, status ∈ STATUSES, phase existe, ids únicos, items das deliveries existem
def current_phase(data) -> dict: ...                 # primeira fase com status "doing", senão primeira "todo"
def next_task(data) -> dict | None: ...              # primeiro item todo|blocked da fase atual (todo antes de blocked)
def render_status(data) -> str: ...                  # GEN + título + Fase atual + Feito + Em andamento + Próxima tarefa + Bloqueios + Entregas (últimas 10)
def render_html(data, template: str) -> str: ...     # substitui {{DATA_JSON}}, {{UPDATED}}, {{PHASE_NAME}}, {{DONE_ROWS}}, {{DOING_ROWS}}, {{TODO_ROWS}}, {{DELIVERIES}}, {{PHASES_NAV}}, {{FR_TABLE}}, {{COUNTS_*}}
def build(root: Path) -> None: ...                   # valida (erro → exit 2), escreve os dois arquivos
def check(root: Path) -> int: ...                    # 0 se gerados == commitados, 1 se diferem (imprime quais)
def add_delivery(root, pr, items, summary, date=None) -> None: ...  # marca items done/pr/merged_at, anexa delivery, updated_at
def main(argv=None) -> int: ...                      # argparse; root = Path(__file__).resolve().parents[1]
if __name__ == "__main__": sys.exit(main())
```
Regras: `html.escape` em todo texto; ordem dos itens = ordem do JSON; `{{...}}` não sobrevive no HTML final (teste cobre).

- [ ] **Step 4: Escrever `scripts/roadmap_template.html`** — tradução para CSS estático do protótipo `forjaos_docs_documenta_o_t_cnica_oficial` (Alabaster Forge): `header` fixo 64 px com logo-texto "ForjaOS" + badge de fase; `aside` 288 px (w-72) com grupos por fase; `main` com `padding-left: 288px; padding-top: 64px`, container `max-width: 1520px`; breadcrumb; banner (`border-radius: 12px`, fundo `surface-container-lowest`, blobs `primary/5`); grid 12 colunas (9 conteúdo + 3 TOC sticky); cards de fase (3 colunas); tabela por FR com pills de status (`todo` = surface-container-high, `doing` = primary-fixed, `done` = emerald tint, `blocked` = tertiary-fixed); linha do tempo de entregas; rodapé com data. Tipografia: Plus Jakarta Sans via Google Fonts `<link>` com fallback `system-ui`; nenhuma dependência JS externa; dados em `<script id="roadmap-data" type="application/json">{{DATA_JSON}}</script>` e um JS inline de ~30 linhas que só liga filtro por fase (sem build de DOM a partir dos dados — o servidor já renderiza as tabelas; o JSON fica para consumo externo). Todas as cores via `:root{--fj-...}` com os valores do tema light do palette.

- [ ] **Step 5: Escrever `docs/roadmap/roadmap.json`** com as 6 fases do PRD §12 (fase 0 `doing`, demais `todo`), itens: `GOV-001…GOV-008` (esta entrega: ADRs, palette, metodologia, design rules, specs de tela, roadmap, agentes, PR template — todos `done`), `F0-001…F0-007` (org GitHub + GHCR, Containerfile mínimo `FROM bazzite-dx-nvidia-open`, workflow build+cosign, `check-branding.sh` real, `THIRD_PARTY_LICENSES` no CI, logo v1 SVG, mascote estático v1 — `todo`, primeiro = `F0-002 Containerfile mínimo`), `F1-001…` (um item por FR-001…016 e FR-050…058 agregado por grupo), F2–F5 agregados por bloco de FR conforme §12. Uma delivery: `2026-11-08`, `pr: null`, itens GOV-*, summary "Metodologia executável e governança".

- [ ] **Step 6: Rodar os testes**

Run: `python3 -m unittest discover -s scripts/tests -p 'test_*.py' -v`
Expected: todos `ok`.

- [ ] **Step 7: Gerar e conferir**

Run: `python3 scripts/roadmap.py validate && python3 scripts/roadmap.py build && python3 scripts/roadmap.py build --check && head -5 docs/STATUS.md`
Expected: `OK`, arquivos escritos, `--check` retorna 0, cabeçalho GERADO.

- [ ] **Step 8: Verificar HTML offline** — abrir `docs/roadmap/index.html` via `device_stage_files` + screenshot não é possível sem browser; alternativa: `python3 -c "import html.parser"` parse + `grep -c '<table' docs/roadmap/index.html` ≥ 2 e `grep -c 'cdn.tailwindcss' = 0`.

- [ ] **Step 9: Commit**

```bash
git add scripts/roadmap.py scripts/roadmap_template.html scripts/tests/test_roadmap.py docs/roadmap docs/STATUS.md
git commit -m "feat(docs): roadmap.json as single source; generated STATUS.md and roadmap HTML"
```

---

### Task 7: `AGENTS.md`, `CLAUDE.md`, comandos, AGENTS.md por pasta, PR template, `check-agents-sync.sh`, `check-branding.sh` stub

**Files:**
- Create: `AGENTS.md`, `CLAUDE.md`, `.claude/commands/{plan,code,test,review,ship}.md`, `{image,cli,hero,hero-mcp,hero-memory,brand,site}/AGENTS.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `scripts/check-agents-sync.sh`, `scripts/tests/test_check_agents_sync.sh`, `scripts/check-branding.sh`
- Delete: os `.gitkeep` das 7 pastas (substituídos pelo AGENTS.md)

- [ ] **Step 1: Teste do sync**

`scripts/tests/test_check_agents_sync.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/.claude/commands"
printf '# plan\nA\n' > "$TMP/.claude/commands/plan.md"
printf '# code\nB\n' > "$TMP/.claude/commands/code.md"
for c in test review ship; do printf '# %s\nX\n' "$c" > "$TMP/.claude/commands/$c.md"; done
{ echo "# AGENTS"; echo "<!-- flow:start -->"; for c in plan code test review ship; do cat "$TMP/.claude/commands/$c.md"; done; echo "<!-- flow:end -->"; } > "$TMP/AGENTS.md"
"$ROOT/scripts/check-agents-sync.sh" "$TMP" || { echo "FAIL: sincronizado reprovado"; exit 1; }
printf '# plan\nMUDOU\n' > "$TMP/.claude/commands/plan.md"
if "$ROOT/scripts/check-agents-sync.sh" "$TMP"; then echo "FAIL: divergência aprovada"; exit 1; fi
echo "PASS test_check_agents_sync"
```

- [ ] **Step 2: Rodar — falha** (script inexistente).

- [ ] **Step 3: `scripts/check-agents-sync.sh`**

```bash
#!/usr/bin/env bash
# O bloco <!-- flow:start --> … <!-- flow:end --> de AGENTS.md deve ser idêntico à concatenação
# de .claude/commands/{plan,code,test,review,ship}.md nessa ordem.
set -euo pipefail
ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
expected="$(for c in plan code test review ship; do cat "$ROOT/.claude/commands/$c.md"; done)"
actual="$(awk '/<!-- flow:start -->/{f=1;next} /<!-- flow:end -->/{f=0} f' "$ROOT/AGENTS.md")"
if [[ "$expected" == "$actual" ]]; then echo "check-agents-sync: OK"; exit 0; fi
echo "check-agents-sync: AGENTS.md (bloco flow) difere de .claude/commands/*.md"
diff <(printf '%s\n' "$expected") <(printf '%s\n' "$actual") || true
exit 1
```

- [ ] **Step 4: Comandos** — cada `.claude/commands/<gate>.md` começa com `# /<gate> — <nome do gate>` e tem: *Quando usar*, *Pré-condições*, *Passos* (numerados, referenciando `docs/dev/METHODOLOGY.md §N`), *Verificação* (comandos exatos), *Saída esperada*. `review.md` inclui a frase: "Você está revisando código que **outra** ferramenta escreveu. Se você escreveu, pare e peça a outra." `ship.md` inclui os comandos `roadmap.py add-delivery` e `build`.

- [ ] **Step 5: `AGENTS.md`** com seções: `## Projeto` (3 linhas + links PRD/METHODOLOGY/DESIGN-RULES/STATUS/roadmap); `## Regras invioláveis` (lista da METHODOLOGY §0 + "leia `docs/STATUS.md` antes de começar; a próxima tarefa está lá"); `## Fluxo` contendo o bloco `<!-- flow:start -->` … `<!-- flow:end -->` = concatenação dos 5 comandos; `## Convenções` (branch, commit, escopos, idioma: regras pt-BR, código/commits en); `## Estrutura do repositório` (tabela das 7 pastas + docs + scripts); `## Design` (resumo ADR-027/028 + link DESIGN-RULES + "nunca abra `code.html` antes da spec da tela"); `## Roadmap` ("toda entrega termina com `roadmap.py add-delivery` + `build`; `STATUS.md`/`index.html` nunca à mão"); `## Verificações` (tabela script → quando roda). Gerar o bloco flow por `for c in plan code test review ship; do cat .claude/commands/$c.md; done`.

- [ ] **Step 6: `CLAUDE.md`**

```markdown
@AGENTS.md

# Claude Code — notas específicas
- Os gates do fluxo estão disponíveis como comandos: `/plan`, `/code`, `/test`, `/review`, `/ship` (`.claude/commands/`).
- Antes de qualquer tarefa: leia `docs/STATUS.md` (próxima tarefa) e a spec/plano referenciados.
- Revisão cruzada: se você implementou a branch, não execute `/review` nela — peça ao Codex (`AGENTS.md §Fluxo › review`).
```

- [ ] **Step 7: `AGENTS.md` por pasta** (≤ 25 linhas cada): escopo (quais FR), linguagem e toolchain, como testar, DoD local, specs de tela que pertencem à pasta (da tabela-mestra da Task 5), o que **não** fazer (ex.: `image/`: nunca desligar SELinux, nunca adicionar repo de terceiros sem ADR; `hero/`: toda tool declara tier; `brand/`: toda cor vem do palette). Remover `.gitkeep`.

- [ ] **Step 8: `.github/PULL_REQUEST_TEMPLATE.md`** — campos: Requisitos (`FR-`/`NFR-`/`ADR-`), Plano (`docs/superpowers/plans/...`), Spec de tela (se houver) + captura lado a lado, checklist dos 5 gates, "Implementado por: Claude Code | Codex", "Revisado por: (a outra)", "Roadmap: `add-delivery` executado ☐".

- [ ] **Step 9: `scripts/check-branding.sh`** stub: cabeçalho explicando FR-002, lista das strings que irá procurar na imagem (`Fedora`, `Bazzite`, `Bluefin`, `fedora-logos`, wallpapers Fedora, `os-release` ≠ ForjaOS), `echo "check-branding: STUB — implementação real é a tarefa F0-004 (ver docs/STATUS.md)"; exit 0`.

- [ ] **Step 10: Rodar tudo**

Run: `chmod +x scripts/*.sh scripts/tests/*.sh; bash scripts/tests/test_check_agents_sync.sh && scripts/check-agents-sync.sh && scripts/check-tokens.sh && scripts/check-branding.sh && grep -q '^@AGENTS.md' CLAUDE.md && echo ALL-OK`
Expected: `PASS…`, `check-agents-sync: OK`, `check-tokens: OK`, stub, `ALL-OK`.

- [ ] **Step 11: Commit**

```bash
git add -A && git commit -m "feat(agents): AGENTS.md single source, CLAUDE.md import, gate commands, per-folder rules, PR template"
```

---

### Task 8: Fechamento — README, verificação final, entrega no roadmap, push

**Files:**
- Modify: `README.md`, `docs/roadmap/roadmap.json` (via `add-delivery` já feito na Task 6 — conferir), gerados

- [ ] **Step 1: README** — título, uma frase do PRD §1, tabela "Comece por aqui": `docs/PRD.md`, `docs/STATUS.md`, `docs/roadmap/index.html`, `docs/dev/METHODOLOGY.md`, `docs/design-system/DESIGN-RULES.md`, `AGENTS.md`; seção "Para agentes (Claude Code / Codex)": leia `AGENTS.md`, comece por `STATUS.md`.

- [ ] **Step 2: Verificação final (DoD da spec §6)**

Run:
```bash
python3 -m unittest discover -s scripts/tests -p 'test_*.py' && bash scripts/tests/test_check_tokens.sh && bash scripts/tests/test_check_agents_sync.sh \
&& scripts/check-tokens.sh && scripts/check-agents-sync.sh && python3 scripts/roadmap.py build --check \
&& [ "$(ls docs/design-system/telas/forjaos_*.md | wc -l)" = 16 ] && grep -q '^@AGENTS.md' CLAUDE.md \
&& ! grep -c 'cdn.tailwindcss' docs/roadmap/index.html && echo DOD-OK
```
Expected: `DOD-OK`.

- [ ] **Step 3: Checar links do AGENTS.md** — todo caminho citado existe:

Run: `grep -oE '(docs|scripts|brand|\.claude|\.github)/[A-Za-z0-9_./-]+' AGENTS.md | sort -u | while read p; do [ -e "$p" ] || echo "MISSING $p"; done`
Expected: vazio.

- [ ] **Step 4: Commit e push**

```bash
git add -A && git commit -m "docs: README entry points for humans and agents" && git push origin main
```
