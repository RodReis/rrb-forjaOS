# /ship — Gate 5: registrar a entrega no roadmap e mergear

**Quando usar:** após `review: 8/8` e CI verde.

**Pré-condições**
- `review: 8/8` no PR; CI verde; branch rebased em `main`.
- Você sabe os IDs do `roadmap.json` que este PR entrega (ex.: `F0-002`).

**Passos** (`docs/dev/METHODOLOGY.md §5`)
1. Na branch:
   ```bash
   python3 scripts/roadmap.py add-delivery --pr <N> --items <ID1>,<ID2> --summary "<uma frase do que foi entregue>"
   python3 scripts/roadmap.py build
   git add docs/roadmap/roadmap.json docs/STATUS.md docs/roadmap/index.html
   git commit -m "docs(roadmap): deliver PR #<N>"
   git push
   ```
2. Se a entrega fecha o DoD de uma fase do PRD §12, mude o `status` da fase em `roadmap.json` no mesmo commit (`doing` → `done`, próxima `todo` → `doing`).
3. Confira o template do PR: nenhum campo vazio, checklist dos 5 gates marcado.
4. **Squash merge**; título = primeiro commit `feat/fix` da branch. Apague a branch remota.
5. Se surgiu tarefa nova durante o trabalho, adicione-a em `roadmap.json` (`items[]`) — nunca em TODO solto no código.

**Verificação**
```bash
python3 scripts/roadmap.py build --check && git log -1 --format=%s | grep -q 'docs(roadmap): deliver PR #'
```

**Saída esperada:** `main` com a entrega; `docs/STATUS.md` aponta a próxima tarefa; `docs/roadmap/index.html` atualizado.
