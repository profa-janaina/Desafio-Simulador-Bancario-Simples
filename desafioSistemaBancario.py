login = """
Escolha uma opção:

[1] Cadastrar usuário
[2] Cadastrar conta-corrente
[3] Listar contas
[4] Acessar operações
[0] Sair

=> """

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

usuarios = []
contas = []
AGENCIA = '0001'


# #Cadastrar conta corrente (vincular pelo cpf)
# agencia = "0001"
# numero_conta = 1
# usuario = user[nome]

def depositar(saldo,extrato,/):
    deposito = int(input("Informe o valor do depósito => "))
    if deposito > 0:
        saldo = saldo + deposito
        extrato += f"Depósito: R$ {deposito:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("!!! Informe um valor válido")

    return saldo, extrato    


def sacar(*,numero_saques,saldo,limite,extrato,limite_saque_max):
    if numero_saques < limite_saque_max:
            saque = int(input("Informe o valor do saque => "))
            if saque > 0:
                if saque < saldo:
                    if saque <= limite:
                        saldo = saldo - saque
                        numero_saques = numero_saques + 1
                        extrato += f"Saque: R$ {saque:.2f}\n"
                        print("Saque realizado com sucesso! Retire o dinheiro.")
                    else:
                        print("!!! Você ultrapassou o limite máximo de R$500,00 por saque")
                else:
                    print("!!! Você não possui saldo suficiente!")
            else:
                print("!!! Informe um valor válido")
    else:
        print("!!! Você ultrapassou o limite diário de 3 saques")
    
    return saldo, extrato, numero_saques

def transferir(numero_transferencias,/,*,saldo,limite_diario,extrato,limite_transferencia_max):
    if numero_transferencias < limite_transferencia_max:
        transferencia = int(input("Informe o valor a ser transferido => "))
        if transferencia > 0:
            if transferencia < saldo:
                if transferencia <= limite_diario:
                    saldo -= transferencia
                    numero_transferencias += 1
                    extrato += f"Transferência: R$ {transferencia:.2f}\n"
                    print("Transferência realizada com sucesso!")
                else:
                    print("!!! Você ultrapassou o limite máximo de R$300,00 por transferência")
            else:
                print("!!! Você não possui saldo suficiente!")
        else:
            print("!!! Informe um valor válido")
    else:
        print("!!! Você ultrapassou o limite diário de 2 transferências")  

    return saldo, extrato, numero_transferencias 

def consultar(saldo,/,*,extrato):
    print("\n=============== Extrato ===============\n")
    if not extrato:
        print("Nenhuma transação realizada\n")
    else:
        print(extrato)
    print(f"\nSaldo: R$ {saldo:.2f}\n")
    print("================= Fim =================")   
    return saldo, extrato

def cadastrar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)    
    
    if usuario:
        print('!!! Já existe usuário cadastrado com este CPF')
        return
    
    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereço (logradouro, número - bairro - cidade/sigla do estado): ')

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento,  "cpf" : cpf, "endereco":endereco})
    print('Usuário cadastrado com sucesso!')

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def cadastrar_conta_corrente(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)    
    
    if usuario:
        print('Conta criada com sucesso!')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario }
    
    print("!!! Usuário não encontrado")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência: {conta['agencia']}
            C/C:     {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        """
        print("-"*100)
        print(linha)

while True:
    opcao_login = int(input(login))

    if opcao_login == 1:
        cadastrar_usuario(usuarios)

    elif opcao_login == 2:
        numero_conta = len(contas) + 1
        conta = cadastrar_conta_corrente(AGENCIA, numero_conta, usuarios)

        if conta:
            contas.append(conta)

    elif opcao_login == 3:
        listar_contas(contas)

    elif opcao_login == 4:
        while True:
            opcao = int(input(menu))

            if opcao == 1:
                saldo, extrato = depositar(saldo,extrato)

            elif opcao == 2:
                saldo, extrato, numero_saques = sacar(numero_saques = numero_saques,saldo = saldo,limite = limite,extrato = extrato,limite_saque_max=LIMITE_SAQUES)

            elif opcao == 3:
                saldo, extrato, numero_transferencias = transferir(numero_transferencias,saldo=saldo,limite_diario=limite_diario_transferencia,extrato=extrato, limite_transferencia_max = LIMITE_TRANSFERENCIA)

            elif opcao == 4:
                saldo, extrato = consultar(saldo,extrato=extrato)

            elif opcao == 0:
                break

            else:
                print("Operação inválida, por favor, selecione novamente a operação desejada")

    elif opcao_login == 0:
            break

    else:
        print("Operação inválida, por favor, selecione novamente a operação desejada")