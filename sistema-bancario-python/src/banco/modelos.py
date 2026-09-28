from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

AGENCIA_PADRAO = "0001"


@dataclass(frozen=True)
class Usuario:
    nome: str
    data_nascimento: str
    cpf: str
    endereco: str


@dataclass(frozen=True)
class Transacao:
    tipo: str  # "Depósito" ou "Saque"
    valor: Decimal
    data: datetime


@dataclass
class Conta:
    numero: int
    cpf_titular: str
    agencia: str = AGENCIA_PADRAO
    saldo: Decimal = Decimal("0")
    limite: Decimal = Decimal("500")
    limite_saques_diarios: int = 3
    transacoes: list[Transacao] = field(default_factory=list)
