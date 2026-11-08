# /plan — Gate 1: planejar antes de tocar em código

**Quando usar:** sempre que uma tarefa nova vai começar. Sem plano aprovado não existe branch.

**Pré-condições**
- Leu `docs/STATUS.md` e a tarefa é a "Próxima tarefa" (ou foi explicitamente pedida pelo humano).
- Existe spec aprovada em `docs/superpowers/specs/` **ou** issue com `FR-`/`NFR-`/`ADR-` e DoD objetivo.
- Se a tarefa envolve tela: a spec `docs/design-system/telas/<slug>.md` existe e o hash bate (`python3 scripts/gen_tela_specs.py --check`).

**Passos** (`docs/dev/METHODOLOGY.md §1`)
1. Leia o PRD nos IDs citados e, se houver tela, a spec da tela **antes** do `code.html`.
2. Escreva `docs/superpowers/plans/AAAA-MM-DD-<slug>.md` com: Goal, Architecture, Tech Stack, mapa de arquivos, tarefas de ≤ 2 h — cada uma com arquivos exatos, o teste que a prova, DoD e mensagem de commit.
3. Toda tarefa cita um ID do PRD. Nenhuma diz "TBD", "depois", "tratar erros" sem dizer como.
4. Se alguma tarefa depende de decisão não tomada, pare: a decisão vira ADR primeiro.
5. Se o plano não cabe em uma branch/PR, divida em dois planos.

**Verificação**
```bash
f=docs/superpowers/plans/<arquivo>.md
grep -L 'FR-\|NFR-\|ADR-' "$f"               # vazio
grep -niE 'TBD|TODO|depois|a definir' "$f"   # vazio
```

**Saída esperada:** plano commitado em `docs/superpowers/plans/` com mensagem `docs(plans): <slug>`; branch ainda **não** criada.
