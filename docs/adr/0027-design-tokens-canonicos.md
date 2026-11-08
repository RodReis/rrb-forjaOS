# ADR-027 — Design tokens canônicos: Cybernetic Forge (escuro) + Alabaster Forge (claro)

**Status:** aceito · **Data:** 2026-11-08 · **Implementa:** FR-050, FR-051 · **Relacionados:** ADR-028

## Contexto

`docs/telas/design/` contém três design systems gerados em momentos diferentes: *Cybernetic Forge*, *Cybernetic Obsidian* (ambos escuros, com superfícies e escalas tipográficas distintas) e *Alabaster Forge* (claro). As 16 telas em `docs/telas/` são inconsistentes entre si: o terminal, o wizard, o explorer e os visualizadores de memória usam a configuração Tailwind do Forge (`surface #0f131d`, `primary #c3f5ff`); GRUB, SDDM, Plymouth e plasmoid usam Fira Code; o overlay antigo usa Inter como fonte de UI. FR-051 exige **um** arquivo fonte (`palette.json`) que gera Plasma, SDDM, Plymouth, Konsole, VS Code, GTK e Firefox. Com três fontes e três conjuntos de fontes tipográficas, "nada de tela genérica" é inatingível: cada agente escolhe a sua.

## Decisão

1. **Tema escuro canônico:** *Cybernetic Forge* (`docs/telas/design/cybernetic_forge/DESIGN.md`). É o que a maioria das telas tokenizadas já usa.
2. **Tema claro canônico:** *Alabaster Forge* (`docs/telas/design/alabaster_forge/DESIGN.md`).
3. ***Cybernetic Obsidian* é aposentado.** Permanece em `docs/telas/design/` apenas como histórico; nenhum valor novo é retirado dele. Onde Obsidian trazia medidas úteis já adotadas nas telas (overlay 520 px, dock 64 px a 12 px da borda), esses valores foram absorvidos no `palette.json` como dimensões, não como tema.
4. **Fonte única de tokens:** `brand/palette.json`. Cores (dark/light), tipografia, raio, espaçamento, elevação, dimensões fixas, semântica de estado e acento do mascote. Qualquer cor em QML, CSS, SVG, KColorScheme, Plymouth, GRUB ou Konsole do projeto tem de existir no `palette.json`; `scripts/check-tokens.sh` falha caso contrário.
5. **Tipografia:** UI = **Plus Jakarta Sans**; monoespaçada (código, telemetria, status, atalhos) = **JetBrains Mono**; **Inter** permitida só em corpo de texto denso (tabelas, inspetores). **Fira Code é proibida** e será removida dos protótipos quando regenerados. Todas as três são OFL — podem ser embarcadas na imagem.
6. **Alterar um token é uma decisão:** exige novo ADR que cite este. Adicionar token novo (sem alterar os existentes) exige apenas PR com justificativa e atualização do `DESIGN-RULES.md`.

## Alternativas descartadas

- **Obsidian como escuro canônico:** spec mais detalhada de overlay e dock, mas exigiria retokenizar cinco telas que já seguem Forge.
- **Manter os três como variantes:** fere FR-051 e torna o `check-tokens.sh` inútil (tudo passa).

## Consequências

- `brand/palette.json` nasce nesta entrega; os temas Plasma/SDDM/Plymouth/Konsole derivam dele por script (FR-051), a construir na Fase 1.
- `docs/design-system/DESIGN-RULES.md` traz a tabela de tradução token → cada tecnologia.
- Telas que hoje usam Fira Code ou cores fora do Forge são implementadas com os tokens canônicos; a divergência fica registrada na spec da tela (`docs/design-system/telas/<slug>.md`).
