menu = """
Escolha uma opção:

[1] Depositar
[2] Sacar
[3] Transferência
[4] Extrato
[0] Sair

=> """

saldo = 0
limite = 500
limite_diario_transferencia = 300
extrato = ""
numero_saques = 0
numero_transferencias = 0
LIMITE_SAQUES = 3
LIMITE_TRANSFERENCIA = 2

while True:
    opcao = int(input(menu))

    if opcao == 1:
        deposito = int(input("Informe o valor do depósito => "))
        if deposito > 0:
            saldo = saldo + deposito
            extrato += f"Depósito: R$ {deposito:.2f}\n"
            print("Depósito realizado com sucesso!")
        else:
            print("Informe um valor válido")

    elif opcao == 2:
        if numero_saques < LIMITE_SAQUES:
            saque = int(input("Informe o valor do saque => "))
            if saque > 0:
                if saque < saldo:
                    if saque <= limite:
                        saldo = saldo - saque
                        numero_saques = numero_saques + 1
                        extrato += f"Saque: R$ {saque:.2f}\n"
                        print("Saque realizado com sucesso! Retire o dinheiro.")
                    else:
                        print("Você ultrapassou o limite máximo de R$500,00 por saque")
                else:
                    print("Você não possui saldo suficiente!")
            else:
                print("Informe um valor válido")
        else:
            print("Você ultrapassou o limite diário de 3 saques")

    elif opcao == 3:
        if numero_transferencias < LIMITE_TRANSFERENCIA:
            transferencia = int(input("Informe o valor a ser transferido => "))
            if transferencia > 0:
                if transferencia < saldo:
                    if transferencia <= limite_diario_transferencia:
                        saldo -= transferencia
                        numero_transferencias += 1
                        extrato += f"Transferência: R$ {transferencia:.2f}\n"
                        print("Transferência realizada com sucesso!")
                    else:
                        print("Você ultrapassou o limite máximo de R$300,00 por transferência")
                else:
                    print("Você não possui saldo suficiente!")
            else:
                print("Informe um valor válido")
        else:
            print("Você ultrapassou o limite diário de 2 transferências")

    elif opcao == 4:
        print("\n=============== Extrato ===============\n")
        if not extrato:
            print("Nenhuma transação realizada\n")
        else:
            print(extrato)
        print(f"\nSaldo: R$ {saldo:.2f}\n")
        print("================= Fim =================")    

    elif opcao == 0:
        break

    else:
        print("Operação inválida, por favor, selecione novamente a operação desejada")