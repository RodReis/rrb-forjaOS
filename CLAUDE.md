@AGENTS.md

# Claude Code — notas específicas

- Os cinco gates do fluxo estão disponíveis como comandos: `/plan`, `/code`, `/test`, `/review`, `/ship` (`.claude/commands/`). O texto deles é o mesmo do bloco **Fluxo** do `AGENTS.md`.
- Antes de qualquer tarefa: leia `docs/STATUS.md` (próxima tarefa) e a spec ou plano que ela referencia. Não escolha outra tarefa sem pedido explícito.
- **Revisão cruzada:** se você implementou a branch, não execute `/review` nela — peça ao Codex (`AGENTS.md › Fluxo › review`). Se o Codex implementou, `/review` é seu.
- Telas: abra `docs/design-system/telas/<slug>.md` antes do `code.html`. Tokens só de `brand/palette.json`.
- Arquivos gerados (`docs/STATUS.md`, `docs/roadmap/index.html`, `docs/design-system/telas/*.md` exceto Status/Pendências) não são editados com Edit/Write — regenere com o script correspondente.
- Superpowers (brainstorming → writing-plans → executing-plans) complementam os gates: *brainstorming* alimenta a spec, *writing-plans* é o gate *plan*, *executing-plans* é o gate *code*. As regras deste repositório prevalecem onde divergirem.
