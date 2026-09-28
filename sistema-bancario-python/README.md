# 🏦 Sistema Bancário em Python

![CI](https://github.com/SEU_USUARIO/sistema-bancario-python/actions/workflows/ci.yml/badge.svg)

Desafio DIO: otimizar o sistema bancário refatorando **depósito, saque e extrato em funções**.
Esta versão vai além do pedido: adiciona usuários, contas, validação de CPF, tratamento de erros próprio e testes automatizados.

## Funcionalidades
- Depositar, sacar e emitir extrato (com data/hora e filtro por tipo)
- Cadastro de usuários (CPF validado e único) e criação de contas
- Limite de R$ 500 por saque e 3 saques **por dia** (reinicia no dia seguinte)
- Valores monetários com `Decimal` (sem erros de ponto flutuante)

## Decisões de projeto
| Tema | Decisão |
|---|---|
| Assinaturas | `depositar(conta, valor, /)` só posicional · `sacar(conta, *, valor)` só nomeado · `gerar_extrato(conta, /, *, tipo)` misto |
| Regras x interface | `operacoes.py` não usa `print`/`input`; a `cli.py` cuida da interação |
| Erros | Exceções específicas herdando de `BancoError`, em vez de `if/else` com prints |
| Testabilidade | `agora` pode ser injetado para testar o limite diário |

## Estrutura
```
src/banco/
  erros.py       exceções de negócio
  modelos.py     dataclasses: Usuario, Conta, Transacao
  operacoes.py   funções: depositar, sacar, gerar_extrato, criar_usuario, criar_conta...
  cli.py         menu interativo
tests/           testes com pytest
```

## Como executar
```bash
git clone https://github.com/SEU_USUARIO/sistema-bancario-python.git
cd sistema-bancario-python
pip install -e ".[dev]"
python -m banco      # ou: banco
pytest -v            # testes
```
Requer Python 3.10+.

## Próximos passos
Persistência em arquivo/SQLite, POO (`Conta`, `Cliente`) e API com FastAPI.

## Licença
MIT
