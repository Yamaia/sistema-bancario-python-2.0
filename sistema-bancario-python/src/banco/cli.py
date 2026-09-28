from .erros import BancoError
from .modelos import Conta, Usuario
from . import operacoes as op

MENU = """
================ MENU ================
[d]  Depositar
[s]  Sacar
[e]  Extrato
[nu] Novo usuário
[nc] Nova conta
[lc] Listar contas
[q]  Sair
=> """


def selecionar_conta(contas: list[Conta]) -> Conta:
    if not contas:
        raise BancoError("Nenhuma conta cadastrada.")
    numero = input("Número da conta: ").strip()
    for conta in contas:
        if str(conta.numero) == numero:
            return conta
    raise BancoError("Conta não encontrada.")


def main() -> None:
    usuarios: dict[str, Usuario] = {}
    contas: list[Conta] = []

    while True:
        opcao = input(MENU).strip().lower()
        if opcao == "q":
            print("Até logo!")
            break
        try:
            if opcao == "d":
                conta = selecionar_conta(contas)
                op.depositar(conta, input("Valor do depósito: "))
                print("\n=== Depósito realizado com sucesso! ===")
            elif opcao == "s":
                conta = selecionar_conta(contas)
                op.sacar(conta, valor=input("Valor do saque: "))
                print("\n=== Saque realizado com sucesso! ===")
            elif opcao == "e":
                print(op.gerar_extrato(selecionar_conta(contas)))
            elif opcao == "nu":
                op.criar_usuario(
                    usuarios,
                    cpf=input("CPF: "),
                    nome=input("Nome completo: "),
                    data_nascimento=input("Data de nascimento (dd-mm-aaaa): "),
                    endereco=input("Endereço (logradouro, nro - bairro - cidade/UF): "),
                )
                print("\n=== Usuário criado com sucesso! ===")
            elif opcao == "nc":
                conta = op.criar_conta(contas, usuarios, input("CPF do titular: "))
                print(f"\n=== Conta {conta.numero} criada com sucesso! ===")
            elif opcao == "lc":
                print(op.listar_contas(contas, usuarios))
            else:
                print("Operação inválida, selecione novamente.")
        except BancoError as erro:
            print(f"\n@@@ Operação falhou! {erro} @@@")
