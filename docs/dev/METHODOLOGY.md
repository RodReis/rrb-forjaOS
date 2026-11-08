# Metodologia de implementação — ForjaOS

**Versão:** 1.0 · **Data:** 2026-11-08 · **Vale para:** Claude Code, Codex e humanos · **Fonte de regras do agente:** `AGENTS.md` (raiz)

## 0. Por que existe e regras invioláveis

O PRD diz *o quê*. Este documento diz *como* uma tarefa entra e sai do repositório. São cinco gates em sequência — **plan → code → test → review → ship** — e nenhum é pulável. Cada gate tem entrada, saída, checklist e um comando que prova que foi cumprido. "Passou no comando" é o critério; opinião não é.

**Regras invioláveis**

1. Nenhum gate é pulado. Hotfix de segurança pode pular *plan* (ver §7), nunca *test* nem *review*.
2. **Quem implementou não revisa.** Claude Code implementa → Codex revisa, ou o inverso. A mesma ferramenta nunca ocupa os dois papéis na mesma branch.
3. **PRD manda no conteúdo; protótipo manda no layout** (ADR-028). Divergência vira issue, não improviso.
4. **Toda cor vem de `brand/palette.json`** (ADR-027). `scripts/check-tokens.sh` é juiz.
5. **Nenhuma ação destrutiva fora de tier** (FR-093, FR-100): `rm -rf`, `dd`, alteração de firewall, de SELinux ou de `/etc` só com confirmação explícita do humano e registro no PR.
6. **Toda unit systemd própria declara consumo** (`MemoryMax`, `CPUQuota`, `Nice`) — princípio 5 do PRD.
7. **Toda entrega atualiza o roadmap no mesmo PR** (`scripts/roadmap.py add-delivery` + `build`). `docs/STATUS.md` e `docs/roadmap/index.html` nunca são editados à mão.
8. **Comece por `docs/STATUS.md`.** A próxima tarefa está lá. Não invente prioridade.
9. Idioma: regras e docs de produto em pt-BR; código, nomes de arquivo, commits e docs técnicas em inglês (PRD regra 4).

---

## 1. Gate *plan*

**Entrada:** uma spec aprovada em `docs/superpowers/specs/AAAA-MM-DD-<slug>-design.md` **ou** uma issue com ID do PRD (`FR-xxx`, `NFR-xxx`, `ADR-xxx`) e DoD objetivo.

**Saída:** `docs/superpowers/plans/AAAA-MM-DD-<slug>.md` com:
- header do `writing-plans` (Goal, Architecture, Tech Stack);
- mapa de arquivos (criar/modificar, responsabilidade de cada um);
- tarefas de **≤ 2 h** cada, numeradas, com: arquivos exatos, o teste que prova a tarefa, o critério de pronto e o commit esperado;
- para tela: referência explícita a `docs/design-system/telas/<slug>.md`.

**Checklist**
- [ ] Toda tarefa cita pelo menos um `FR-`/`NFR-`/`ADR-`.
- [ ] Nenhuma tarefa diz "TBD", "ajustar depois", "tratar erros" sem dizer como.
- [ ] Tarefas de tela citam a spec da tela, não o `code.html`.
- [ ] Nenhuma tarefa depende de decisão não tomada (se depende, a decisão vira ADR **antes**).
- [ ] O plano cabe em uma branch e um PR. Se não cabe, são dois planos.

**Comando de verificação**
```bash
f=docs/superpowers/plans/<arquivo>.md
grep -L 'FR-\|NFR-\|ADR-' "$f"            # deve imprimir nada
grep -niE 'TBD|TODO|depois|a definir' "$f" # deve imprimir nada
```

---

## 2. Gate *code*

**Entrada:** plano aprovado (gate 1). **Nunca** começa em `main`.

**Saída:** branch com um commit por tarefa do plano, todos verdes.

**Convenções**
- Branch: `feat/FR-xxx-slug` · `fix/FR-xxx-slug` · `adr/NNNN-slug` · `docs/slug` · `chore/slug`.
- Commits convencionais: `tipo(escopo): resumo em inglês no imperativo`. Tipos: `feat fix adr docs test chore refactor`. Escopos: `image cli hero hero-mcp hero-memory brand site docs scripts agents`.
- **TDD obrigatório** em Rust, shell e Python: escreva o teste → rode e veja falhar → implemente o mínimo → rode e veja passar → refatore → commit. Um commit sem teste correspondente só é aceito em `docs/` e `brand/` (artes).
- Para tela: (1) abra `docs/design-system/telas/<slug>.md`; (2) aplique a tabela de substituições (ADR-028); (3) copie **medidas** e **tokens**, nunca valores hex soltos; (4) use `screen.png` como referência visual e `code.html` só para conferir classe/medida específica.
- Arquivos pequenos e com uma responsabilidade. Um arquivo QML ou Rust acima de ~400 linhas é sinal de divisão.
- Nada de dependência nova sem justificativa no commit e verificação de licença (G4).

**Checklist**
- [ ] Branch nomeada pela convenção e criada a partir de `main` atualizada.
- [ ] Cada tarefa do plano virou exatamente um commit.
- [ ] Testes escritos antes da implementação (histórico do commit mostra).
- [ ] Nenhum hex fora do palette; nenhuma string da coluna "No protótipo" do ADR-028.
- [ ] Nenhum segredo, chave ou token em arquivo (NFR-024).

**Comando de verificação**
```bash
git log --format=%s origin/main..HEAD | grep -vE '^(feat|fix|adr|docs|test|chore|refactor)\((image|cli|hero|hero-mcp|hero-memory|brand|site|docs|scripts|agents)\): ' # vazio
scripts/check-tokens.sh
git diff origin/main..HEAD | grep -nE 'Jarvis|devos|nftables|24\.04|arm64|RTX 4070' # vazio
```

---

## 3. Gate *test*

**Entrada:** branch do gate 2.

**Saída:** todos os testes da(s) pasta(s) tocada(s) verdes; evidência visual quando há tela.

**Por pasta**

| Pasta | Comando |
| --- | --- |
| `cli/`, `hero/`, `hero-mcp/`, `hero-memory/` (Rust) | `cargo fmt --check && cargo clippy --all-targets -- -D warnings && cargo test && cargo llvm-cov --fail-under-lines 70` (NFR-041) |
| `image/` (shell, Containerfile, recipes) | `bash scripts/tests/*.sh`; `podman build` no CI (Fase 0+); `scripts/check-branding.sh` |
| `brand/` (QML, SVG, temas) | `scripts/check-tokens.sh`; `qmllint` nos `.qml`; captura lado a lado |
| `site/` | build do site sem warnings; `scripts/check-tokens.sh` |
| `scripts/`, `docs/` | `python3 -m unittest discover -s scripts/tests -p 'test_*.py'`; `bash scripts/tests/*.sh`; `python3 scripts/roadmap.py build --check` |

**Evidência visual (toda tarefa de tela)**
- Captura lado a lado em `docs/design-system/telas/<slug>/compare-AAAA-MM-DD.png`: protótipo à esquerda, implementação à direita, **mesma resolução**.
- Medidas-chave da spec conferidas (largura do overlay, altura da barra, raio, espaçamentos) e listadas no PR.

**Checklist**
- [ ] Comando da pasta passou localmente (saída colada no PR).
- [ ] Teste novo falha se a implementação for revertida (prova que testa algo).
- [ ] Tela: captura lado a lado anexada; `check-tokens.sh` OK.
- [ ] Unit systemd nova: `systemd-analyze verify` passou e `MemoryMax`/`CPUQuota`/`Nice` presentes.

**Comando de verificação**
```bash
# raiz do repositório
python3 -m unittest discover -s scripts/tests -p 'test_*.py' && bash scripts/tests/*.sh && scripts/check-tokens.sh && python3 scripts/roadmap.py build --check
# + comando da pasta tocada (tabela acima)
```

---

## 4. Gate *review* (revisão cruzada)

**Entrada:** PR aberto pela ferramenta que implementou. Ela **para** aqui.

**Saída:** comentário `review: 8/8` da **outra** ferramenta e zero achados abertos.

**Protocolo**
1. O revisor confirma que não é o autor da branch (`git log --format=%an`, descrição do PR). Se for, interrompe e devolve.
2. Roda os comandos do gate 3 do zero (não confia na saída colada).
3. Percorre o checklist abaixo. Cada achado vira **commit na branch** com prefixo `fix(review): …`, nunca comentário solto.
4. Fecha com `review: N/8` — só `8/8` libera o gate 5.

**Checklist (8 itens)**
- [ ] (1) O FR/NFR/ADR citado está realmente coberto; DoD do PRD atendido.
- [ ] (2) ADR-028 aplicado: nenhuma string proibida; conteúdo bate com o PRD.
- [ ] (3) ADR-027 aplicado: `check-tokens.sh` OK; fontes só Plus Jakarta Sans / JetBrains Mono / Inter(dense).
- [ ] (4) Testes existem, foram escritos antes e provam o comportamento (não só cobertura).
- [ ] (5) Consumo declarado em toda unit systemd; modelos de IA descarregam quando ociosos (princípio 5).
- [ ] (6) Nenhum segredo em arquivo; chaves só via KWallet/`secret-tool` (NFR-024).
- [ ] (7) SELinux, firewalld, `/etc` e tiers do Policy Engine intocados fora do escopo declarado.
- [ ] (8) Roadmap: `add-delivery` preparado no PR (gate 5) e `STATUS.md`/`index.html` regenerados, não editados.

**Comando de verificação**
```bash
gh pr view <N> --json comments -q '.comments[].body' | grep -E '^review: 8/8$'
```

---

## 5. Gate *ship*

**Entrada:** `review: 8/8`, CI verde (a partir da Fase 0), branch rebased em `main`.

**Saída:** squash merge em `main`; roadmap atualizado no mesmo PR.

**Passos**
1. Na branch, antes do merge:
   ```bash
   python3 scripts/roadmap.py add-delivery --pr <N> --items <ID1>,<ID2> --summary "<uma frase>"
   python3 scripts/roadmap.py build
   git add docs/roadmap/roadmap.json docs/STATUS.md docs/roadmap/index.html
   git commit -m "docs(roadmap): deliver PR #<N>"
   git push
   ```
2. PR template completo (todos os campos, checklist dos 5 gates marcado).
3. **Squash merge** com título = primeiro commit `feat/fix` da branch.
4. Apagar a branch remota.
5. Se a entrega fecha um DoD de fase do PRD §12, atualizar `status` da fase em `roadmap.json` no mesmo commit.

**Checklist**
- [ ] `roadmap.py build --check` passa na branch.
- [ ] PR template sem campo vazio.
- [ ] Squash merge, branch apagada.

**Comando de verificação**
```bash
python3 scripts/roadmap.py build --check && git log -1 --format=%s | grep -q 'docs(roadmap): deliver PR #'
```

---

## 6. Mapa de comandos

| Gate | Claude Code | Codex | Documento |
| --- | --- | --- | --- |
| plan | `/plan` | `AGENTS.md › Fluxo › plan` | este §1 |
| code | `/code` | `AGENTS.md › Fluxo › code` | este §2 |
| test | `/test` | `AGENTS.md › Fluxo › test` | este §3 |
| review | `/review` | `AGENTS.md › Fluxo › review` | este §4 |
| ship | `/ship` | `AGENTS.md › Fluxo › ship` | este §5 |

Os cinco arquivos em `.claude/commands/` e o bloco `<!-- flow:start -->…<!-- flow:end -->` do `AGENTS.md` são o mesmo texto; `scripts/check-agents-sync.sh` falha se divergirem.

---

## 7. Exceções

- **Hotfix de segurança** (CVE crítica em pacote próprio, NFR-026; chave vazada): pode pular o gate *plan*; a descrição do PR começa com `hotfix: <motivo>`; *test* e *review* continuam obrigatórios; o revisor cruzado tem prioridade sobre qualquer outra tarefa.
- **Mudança só em `docs/`** sem impacto em código: *test* reduz-se a `roadmap.py build --check` + links válidos; *review* continua cruzada.
- **Esta entrega inicial (2026-11-08)** foi commitada direto em `main` por não existir CI nem segunda ferramenta configurada ainda; está registrada em `roadmap.json` como `GOV-*`. A partir da primeira tarefa da Fase 0, os cinco gates valem integralmente.
