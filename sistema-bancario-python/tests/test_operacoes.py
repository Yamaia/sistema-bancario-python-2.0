from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from banco import Conta, criar_conta, criar_usuario, depositar, gerar_extrato, sacar
from banco.erros import (
    CpfInvalidoError, LimiteSaqueExcedidoError, LimiteSaquesDiariosError,
    SaldoInsuficienteError, UsuarioJaExisteError, UsuarioNaoEncontradoError,
    ValorInvalidoError,
)

CPF_VALIDO = "529.982.247-25"


@pytest.fixture
def conta():
    return Conta(numero=1, cpf_titular="52998224725")


def test_deposito_atualiza_saldo(conta):
    depositar(conta, "100,50")
    assert conta.saldo == Decimal("100.50")


@pytest.mark.parametrize("valor", [0, -5, "abc", "nan"])
def test_valores_invalidos(conta, valor):
    with pytest.raises(ValorInvalidoError):
        depositar(conta, valor)


def test_saque_ok(conta):
    depositar(conta, 200)
    sacar(conta, valor=50)
    assert conta.saldo == Decimal("150.00")


def test_saque_saldo_insuficiente(conta):
    with pytest.raises(SaldoInsuficienteError):
        sacar(conta, valor=10)


def test_saque_acima_do_limite(conta):
    depositar(conta, 1000)
    with pytest.raises(LimiteSaqueExcedidoError):
        sacar(conta, valor=501)


def test_limite_de_saques_diarios_e_reinicia_no_dia_seguinte(conta):
    depositar(conta, 1000)
    hoje = datetime(2026, 1, 10, 10)
    for _ in range(3):
        sacar(conta, valor=10, agora=hoje)
    with pytest.raises(LimiteSaquesDiariosError):
        sacar(conta, valor=10, agora=hoje)
    sacar(conta, valor=10, agora=hoje + timedelta(days=1))


def test_extrato_lista_movimentacoes(conta):
    assert "Não foram realizadas movimentações." in gerar_extrato(conta)
    depositar(conta, 100)
    sacar(conta, valor=30)
    extrato = gerar_extrato(conta)
    assert "Depósito" in extrato and "Saque" in extrato
    assert "Saldo: R$ 70.00" in extrato
    assert "Saque" not in gerar_extrato(conta, tipo="Depósito")


def test_usuarios_e_contas():
    usuarios, contas = {}, []
    criar_usuario(usuarios, nome="Ana", data_nascimento="01-01-2000",
                  cpf=CPF_VALIDO, endereco="Rua A, 1")
    with pytest.raises(UsuarioJaExisteError):
        criar_usuario(usuarios, nome="Ana", data_nascimento="01-01-2000",
                      cpf="52998224725", endereco="Rua A, 1")
    assert criar_conta(contas, usuarios, CPF_VALIDO).numero == 1
    with pytest.raises(UsuarioNaoEncontradoError):
        criar_conta(contas, usuarios, "111.444.777-35")


def test_cpf_invalido():
    with pytest.raises(CpfInvalidoError):
        criar_usuario({}, nome="X", data_nascimento="", cpf="123.456.789-00", endereco="")
