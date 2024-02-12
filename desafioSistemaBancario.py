import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

#Desafio 3
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
    

class Conta:
    def __init__(self, numero_conta, cliente):
        self._saldo = 0
        self._numero_conta = numero_conta
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero_conta):
        return cls(numero_conta, cliente)
   
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero_conta(self):
        return self._numero_conta
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("!!! Você não possui saldo suficiente!")            
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso! Retire o dinheiro.")
            return True
        else:
            print("!!! Informe um valor válido")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor            
            print("Depósito realizado com sucesso!")
        else:
            print("!!! Informe um valor válido")
            return False

        return True

    def transferir(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("!!! Você não possui saldo suficiente!")            
        elif valor > 0:
            self._saldo -= valor
            print("Transferência realizada com sucesso!")
            return True
        else:
            print("!!! Informe um valor válido")

        return False
    
class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, limite = 500, LIMITE_SAQUES = 3, limite_diario_transferencia = 300, LIMITE_TRANSFERENCIA = 2):
        super().__init__(numero_conta, cliente)
        self._limite = limite
        self._LIMITE_SAQUES = LIMITE_SAQUES
        self._limite_diario_transferencia = limite_diario_transferencia
        self._LIMITE_TRANSFERENCIA = LIMITE_TRANSFERENCIA
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_limite_saques = numero_saques >= self._LIMITE_SAQUES

        if excedeu_limite:
            print(f'!!! Você ultrapassou o limite máximo de R${self.limite},00 por saque')
        elif excedeu_limite_saques:
            print(f'!!! Você ultrapassou o limite diário de {self.LIMITE_SAQUES} saques')
        else:
            return super().sacar(valor)
        
        return False
    
    def transferir(self, valor):
        numero_transferencias = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Transferencia.__name__]
        )

        excedeu_limite = valor > self._limite_diario_transferencia
        excedeu_limite_transferencias = numero_transferencias >= self._LIMITE_TRANSFERENCIA

        if excedeu_limite:
            print(f'!!! Você ultrapassou o limite máximo de R${self.limite},00 por transferência')
        elif excedeu_limite_transferencias:
            print(f'!!! Você ultrapassou o limite diário de {self.LIMITE_TRANSFERENCIA} transferência')
        else:
            return super().transferir(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero_conta}
            Titular:\t{self.cliente.nome}
        """

    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):        
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):        
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Transferencia(Transacao):
    def __init__(self, valor):        
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.transferir(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Desafio Extra
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def recuperar_conta_cliente(usuario):
    if not usuario.contas:        
        print('!!Cliente não possui conta!')
        return
    return usuario.contas[0]

def depositar(usuarios):
    cpf = input('Informe o CPF do cliente => ')
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print('!!! Cliente não encontrado!')
        return
    
    valor_deposito = float(input("Informe o valor do depósito => "))
    transacao = Deposito(valor_deposito)

    conta = recuperar_conta_cliente(usuario)
    if not conta:
        return

    usuario.realizar_transacao(conta,transacao)    

def sacar(usuarios):
    cpf = input('Informe o CPF do cliente => ')
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print('!!! Cliente não encontrado!')
        return
    
    valor_deposito = float(input("Informe o valor do saque => "))
    transacao = Saque(valor_deposito)

    conta = recuperar_conta_cliente(usuario)
    if not conta:
        return

    usuario.realizar_transacao(conta,transacao)

def transferir(usuarios):
    cpf = input('Informe o CPF do cliente => ')
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print('!!! Cliente não encontrado!')
        return
    
    valor_deposito = float(input("Informe o valor da transferência => "))
    transacao = Transferencia(valor_deposito)

    conta = recuperar_conta_cliente(usuario)
    if not conta:
        return

    usuario.realizar_transacao(conta,transacao) 

def consultar_extrato(usuarios):
    cpf = input('Informe o CPF do cliente => ')
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print('!!! Cliente não encontrado!')
        return

    conta = recuperar_conta_cliente(usuario)
    if not conta:
        return
    
    print("\n=============== Extrato ===============\n")
    transacoes = conta.historico.transacoes
    extrato = ''

    if not transacoes:
        extrato = "Nenhuma transação foi realizada"
    else:
        for transacao in transacoes:
            extrato += f'\n{transacao["tipo"]}:\n\tR${transacao["valor"]:.2f}'

    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}\n")
    print("================= Fim =================")  

def cadastrar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)    
    
    if usuario:
        print('!!! Já existe usuário cadastrado com este CPF')
        return
    
    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereço (logradouro, número - bairro - cidade/sigla do estado): ')

    usuario = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    usuarios.append(usuario)
    
    
    print("\n=== Cliente criado com sucesso! ===")
   

def cadastrar_conta_corrente(numero_conta, usuarios, contas):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)    
    
    if not usuario:
        print("\n!!! Usuário não encontrado, fluxo de criação de conta encerrado")
        return
    
    
    conta = ContaCorrente.nova_conta(cliente=usuario,numero_conta=numero_conta)
    contas.append(conta)
    usuario.contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")
    

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def menu():
    menu = """\n
    ================= MENU =================
    [1]\tDepositar
    [2]\tSacar
    [3]\tTransferir
    [4]\tConsultar Extrato
    [5]\tNovo usuário
    [6]\tNova Conta
    [7]\tListar contas
    [0]\tSair
    => """
    return int(input(textwrap.dedent(menu)))
    #return int(input(menu))

def main():
    usuarios = []
    contas = []
   
    while True:
        opcao = menu()
        if opcao == 1:
            depositar(usuarios)
        elif opcao == 2:
            sacar(usuarios)
        elif opcao == 3:
            transferir(usuarios)
        elif opcao == 4:
            consultar_extrato(usuarios)
        elif opcao == 5:
            cadastrar_usuario(usuarios)
        elif opcao == 6:
            numero_conta = len(contas)+1
            cadastrar_conta_corrente(numero_conta, usuarios, contas)
        elif opcao == 7:
            listar_contas(contas)
        elif opcao == 0:
            break
        else:
            print("Operação inválida, por favor, selecione novamente a operação desejada")

main()
   