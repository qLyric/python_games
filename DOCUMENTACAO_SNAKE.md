# Documentação da refatoração — snake.py

**Responsável:** Stephanie Vieira  
**Arquivo:** `src/games/snake.py` · **Testes:** `tests/test_snake.py`  
**Ambiente de verificação:** Python 3.12 e pygame 2.6

---

## 1. Erros encontrados e seus tipos

| # | Erro | Local | Tipo | Causa |
|---|---|---|---|---|
| 1 | `AttributeError: 'dict' object has no attribute 'iteritems'` | `setup()` | Erro de execução — incompatibilidade de versão (Python 2 → 3) | `iteritems()` foi removido no Python 3 |
| 2 | `AttributeError: 'dict' object has no attribute 'has_key'` | `Snake.control()` | Erro de execução — incompatibilidade de versão | `has_key()` foi removido no Python 3; falha na primeira tecla pressionada |
| 3 | `TypeError` em `random.randrange(WIDTH/UNIT)` | `rand_pos()` | Erro de tipo — incompatibilidade de versão | `/` passou a retornar float no Python 3, e `randrange` exige inteiro (a partir do Python 3.12 o float gera erro) |
| 4 | ENTER não reiniciava o jogo após o “GAME OVER” | `key_up()` / `new_game()` | Erro de lógica | `new_game()` não zerava a variável `game_over`, então a tela de fim de jogo continuava ativa |
| 5 | `ModuleNotFoundError: No module named 'game_tools'` | importações | Erro de importação | Caminho relativo incorreto; **já corrigido pela equipe** nos commits anteriores (`src.game_tools`) |

## 2. Correções realizadas

| # | Correção |
|---|---|
| 1 | `image_infos.iteritems()` → `image_infos.items()` |
| 2 | `self.controls.has_key(key)` → `key in self.controls` |
| 3 | `random.randrange(WIDTH/UNIT)` → `random.randrange(WIDTH // UNIT)` (idem para `HEIGHT`); `WIDTH/2` → `WIDTH // 2` no texto de fim de jogo |
| 4 | `new_game()` passou a reiniciar `score`, `game_over` e `move_count`; `key_up('return')` também zera `game_over` |

## 3. Melhorias de eficiência, desempenho e legibilidade

Os ganhos de desempenho são pequenos: o jogo é leve (grade de 15×10 células) e nunca teve problema de velocidade. As melhorias foram principalmente de simplicidade do código:

- **`check_collision()`:** usa expressão geradora (`any(... for ...)`) em vez de montar uma lista a cada quadro. A consulta `self.head.pos` é feita uma única vez, e a verificação termina assim que encontra a colisão.
- **`Snake.update()`:** removeu a duplicação de `self.body.append(new_seg)` (existia nos dois ramos do `if/else`), deixando a lógica de crescimento mais direta (`ate_food`).
- **Código morto removido:** blocos comentados em `is_on()`, `draw_tail()` e `update()`.
- **Estrutura de controles:** `controls` agora é um dicionário literal, e a consulta é feita com `in`.
- **Complexidade ciclomática média (radon):** 3,32 → 3,26 (grau A nos dois casos); o módulo já tinha baixa complexidade, e a ferramenta confirmou que a refatoração não a aumentou.

## 4. Melhorias de interface

- **Placar e recorde** exibidos no canto da tela (`Score` e `Best`), com 10 pontos por comida (`POINTS_PER_FOOD`).
- **Mensagem de reinício** na tela de fim de jogo (“Clique ou pressione ENTER para reiniciar”).
- **Novas teclas de controle:** `A` e `D` funcionam como `←` e `→` (giro à esquerda/direita da cobra).

**Controles:** `←`/`A` gira à esquerda · `→`/`D` gira à direita · `ESPAÇO` pausa · `ENTER` ou clique reinicia.

## 5. Testes automatizados

Arquivo `tests/test_snake.py` (`unittest`, 8 casos): carregamento das imagens, posição aleatória dentro da grade, teclas válidas e inválidas, pontuação ao comer, reinício do estado, colisão com o corpo, comida fora da cobra e travessia da borda.

Como executar (na raiz do repositório):

```
python -m unittest discover -s tests -t . -v
```

Resultado: **8 aprovados** no código refatorado; **8 com erro** no código original (evidência dos defeitos corrigidos).

## 6. Commit e push

Mensagem de commit utilizada:

```
fix(snake): compatibilidade com Python 3 (iteritems, has_key, randrange), placar, reinício corrigido e testes automatizados
```
