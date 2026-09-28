import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

from .erros import (
    CpfInvalidoError, LimiteSaqueExcedidoError, LimiteSaquesDiariosError,
    SaldoInsuficienteError, UsuarioJaExisteError, UsuarioNaoEncontradoError,
    ValorInvalidoError,
)
from .modelos import Conta, Transacao, Usuario


def converter_valor(texto: str | int | float | Decimal) -> Decimal:
    """Converte a entrada em Decimal positivo com 2 casas."""
    try:
        valor = Decimal(str(texto).replace(",", ".").strip())
    except InvalidOperation:
        raise ValorInvalidoError("O valor informado não é um número.") from None
    if not valor.is_finite() or valor <= 0:
        raise ValorInvalidoError("O valor deve ser maior que zero.")
    return valor.quantize(Decimal("0.01"))


def depositar(conta: Conta, valor, /, *, agora: datetime | None = None) -> Conta:
    valor = converter_valor(valor)
    conta.saldo += valor
    conta.transacoes.append(Transacao("Depósito", valor, agora or datetime.now()))
    return conta


def sacar(conta: Conta, *, valor, agora: datetime | None = None) -> Conta:
    agora = agora or datetime.now()
    valor = converter_valor(valor)

    if valor > conta.saldo:
        raise SaldoInsuficienteError("Saldo insuficiente.")
    if valor > conta.limite:
        raise LimiteSaqueExcedidoError(
            f"O valor excede o limite por saque (R$ {conta.limite:.2f})."
        )
    saques_hoje = sum(
        1 for t in conta.transacoes
        if t.tipo == "Saque" and t.data.date() == agora.date()
    )
    if saques_hoje >= conta.limite_saques_diarios:
        raise LimiteSaquesDiariosError("Número máximo de saques diários excedido.")

    conta.saldo -= valor
    conta.transacoes.append(Transacao("Saque", valor, agora))
    return conta


def gerar_extrato(conta: Conta, /, *, tipo: str | None = None) -> str:
    """Extrato formatado; `tipo` filtra por 'Depósito' ou 'Saque'."""
    linhas = [
        f"{t.data:%d/%m/%Y %H:%M:%S}  {t.tipo:<9} R$ {t.valor:>10.2f}"
        for t in conta.transacoes
        if tipo is None or t.tipo == tipo
    ]
    corpo = "\n".join(linhas) or "Não foram realizadas movimentações."
    return (
        "================ EXTRATO ================\n"
        f"{corpo}\n\n"
        f"Saldo: R$ {conta.saldo:.2f}\n"
        "=========================================="
    )


def normalizar_cpf(cpf: str) -> str:
    numeros = re.sub(r"\D", "", cpf)
    if len(numeros) != 11 or numeros == numeros[0] * 11:
        raise CpfInvalidoError("CPF inválido: informe 11 dígitos.")
    for tamanho in (9, 10):
        soma = sum(int(d) * p for d, p in zip(numeros[:tamanho], range(tamanho + 1, 1, -1)))
        digito = (soma * 10 % 11) % 10
        if digito != int(numeros[tamanho]):
            raise CpfInvalidoError("CPF inválido: dígitos verificadores não conferem.")
    return numeros


def buscar_usuario(usuarios: dict[str, Usuario], cpf: str) -> Usuario | None:
    return usuarios.get(re.sub(r"\D", "", cpf))


def criar_usuario(usuarios: dict[str, Usuario], *, nome: str, data_nascimento: str,
                  cpf: str, endereco: str) -> Usuario:
    cpf = normalizar_cpf(cpf)
    if cpf in usuarios:
        raise UsuarioJaExisteError("Já existe usuário com esse CPF.")
    usuario = Usuario(nome.strip(), data_nascimento.strip(), cpf, endereco.strip())
    usuarios[cpf] = usuario
    return usuario


def criar_conta(contas: list[Conta], usuarios: dict[str, Usuario], cpf: str) -> Conta:
    usuario = buscar_usuario(usuarios, cpf)
    if usuario is None:
        raise UsuarioNaoEncontradoError("Usuário não encontrado; cadastre-o primeiro.")
    conta = Conta(numero=len(contas) + 1, cpf_titular=usuario.cpf)
    contas.append(conta)
    return conta


def listar_contas(contas: list[Conta], usuarios: dict[str, Usuario]) -> str:
    if not contas:
        return "Nenhuma conta cadastrada."
    return "\n".join(
        f"Agência: {c.agencia} | C/C: {c.numero} | Titular: {usuarios[c.cpf_titular].nome}"
        for c in contas
    )
