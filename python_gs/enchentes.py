# Aplicação para Monitoramento de Enchentes no Brasil

# Grupo:
# Erick Jooji RM 564482
# Luiz Dalboni RM 564189
# Rafael Lorenzini RM 563643

# Função pra permitir que o nivel da agua receba valores decimais
def decimal_agua(valor):
    partes = valor.split(".")
    return len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit()

# Função para o menu
def menu():
    # Opções do menu 
    print("\n--- Sistema de Monitoramento de Enchentes ---")
    print("1. Cadastrar ocorrência de enchente")
    print("2. Visualizar ocorrências")
    print("3. Orientações em caso de enchente")
    print("4. Deletar ocorrência")
    print("5. Sair")

    while True:

        opcao = input("Escolha uma opção: ") # Pede educadamente para o usuário informar uma opção

        if(opcao.isdigit()): # Se o usuário fizer o certo, e colocar um numero faz o abaixo 

            opcao = int(opcao) # Converte a String em int

            if(opcao in [1, 2, 3, 4, 5]): # Se tiver dentro dos 4 valores da lista faz o abaixo

                return opcao # retorna a opção :O
            
            else: # Se não opção invalida!

                print("Opção inválida. Tente novamente.") # Opção inválida! :D

        else:
            print("Tipo de valor na opção invalido!") # Se o usuário não tiver sido legal, e tiver colocado um valor que não é digito ele informa que o tipo é invalido! 

# Ativa quando a opção 1 é selecionada, para cadastrar ocorrencias de enchente
def cadastrar_ocorrencia(lista_ocorrencias): # Essa função usa também as listas de ocorrencias, que pode estar vazia ou não se alguma ocorrencia tiver side registrada.

    print("\nCadastro de Ocorrência")

    # Usamos o .strip para melhor controle do input do usuário
    local = input("Informe a local (Nome inteiro sem abreviações): ").strip()  # Pede a local que ocorreu a enchente, a local deve ser informada sem abreviação.
    if(local == ""): # A local da ocorrencia deve ser informada, logo não aceita e encerra
        print("A local deve ser informada!")
        return
    
    nivel_agua = input("Nível da água em metros (se não souber deixe em branco): ") # Pede o nível da água da enchente se a pessoa não souber pode deixar em branco.

    if(nivel_agua == ""): # Se o usuário deixar em branco, o valor é colocado como desconhecido
        nivel_agua = "desconhecido" 
        print("Nível de água foi colocado como 'Desconhecido'") # Pra não deixar o úsuario no vácuo a gente fala pra ele que foi informado como desconhecido 

    elif(nivel_agua.isdigit() or decimal_agua(nivel_agua)): # Se for um digito, converte nivel da agua em float, e verifica se o nivel da agua é negativo, se for recusa o valor, se não aceita.
        nivel_agua = float(nivel_agua)
        if nivel_agua < 0:
            print("Nível de água não pode ser negativo.")
            return

    else: # Se colocar um valor invalido, informa que o valor é invalido, e encerra
        print("Formato de valor inválido!") 
        return 
    
    pessoas_afetadas = input("Número de pessoas afetadas (se não souber deixe em branco): ") # Pede a quantidade de pessoas que foram afetadas pela enchente, se não souber deixar em branco novamente.

    if(pessoas_afetadas == ""): # Se o usuário deixar em branco, o valor é colocado como desconhecido
        pessoas_afetadas = "desconhecido" 
        print("Numero de pessoas afetadas foi colocado como 'Desconhecido'") # Pra não deixar o úsuario no vácuo a gente fala pra ele que foi informado como desconhecido 

    elif(pessoas_afetadas.isdigit()): # Se for um digito, converte pessoas afetadas em inteiro, e verifica se a quantidade de pessoas afetadas é negativa, se for recusa o valor, se não aceita
        pessoas_afetadas = int(pessoas_afetadas) 
        if(pessoas_afetadas < 0): 
            print("Numero de pessoas afetadas não pode ser negativo.") 
            return 

    else: # Se colocar um valor invalido, informa que o valor é invalido, e encerra
        print("Formato de valor inválido!") 
        return  
    
    ano = 2025 # Como é uma aplicação pra registrar ocorrencias recentes, ou pelo menos desse ano, não precisa que o usuário informe o ano

    mes = input("Qual o mês da ocorrencia (use o número, ex: 1 para Janeiro): ").strip()  # Valor importante, logo será pedido

    if(mes.isdigit()): # Se for digito, converte o mes em inteiro, verifica se é maior que 12 ou menor que 1, se for recusa o valor, se não aceita
        mes = int(mes) 
        if(mes>12 or mes<1): 
            print("Valor absurdo, logo não será aceito") 
            return 
    
    else: # Se colocar um valor invalido, informa que o valor é invalido, e encerra
        print("Formato de valor inválido!")
        return  

    dia = input("Qual o dia da ocorrencia: ").strip()  # Valor importante, logo será pedido

    if(dia.isdigit()): # Se for digito, converte o dia em inteiro, verifica se é maior que 31 ou menor que 1, se for recusa o valor, se não aceita
        dia = int(dia)  
        if(dia>31 or dia<1):
            print("Valor absurdo, logo não será aceito") 
            return 
    
    else: # Se colocar um valor invalido, informa que o valor é invalido, e encerra
        print("Formato de valor inválido!") 
        return 

    data = f"{dia:02d}/{mes:02d}/{ano}" # Converte em String e ajusta para ficar no formato DD/MM/AAAA

    ocorrencia = { # Sim eu sei, não foi ensinado dicionarios durante as aulas (pelo menos até agora), mas eu fiz um cursinho na alura, e nele eles falam sobre, então sim eu sei como eles funcionam fique tranquilo nenhum chat gpt foi responsável por isso
        'local': local,
        'nivel_agua': nivel_agua,
        'pessoas_afetadas': pessoas_afetadas,
        'data': data
    }

    lista_ocorrencias.append(ocorrencia) # Adiciona o dicionario na lista de ocorrencias

    print("Ocorrência cadastrada com sucesso!") # Retorna ao usuário que a ocorrencia foi registrada com sucesso

# Ativa quando a opção 2 é selecionada, mostra as enchentes registradas
def visualizar_ocorrencias(lista_ocorrencias):
    print("\n--- Estatísticas de Ocorrências ---")

    if(not lista_ocorrencias):
        print("Nenhuma ocorrência cadastrada.")
        return

    for i in range(len(lista_ocorrencias)):
        ocorrencia = lista_ocorrencias[i]
        print(f"\nOcorrência {i + 1}:")
        print(f" local: {ocorrencia['local']}")

        nivel = ocorrencia['nivel_agua']
        if(nivel == "desconhecido" or nivel is None):
            print(" Nível da água: desconhecido")
        else:
            print(f" Nível da água: {nivel} metros")

        pessoas = ocorrencia['pessoas_afetadas']
        if(pessoas == "desconhecido" or pessoas is None):
            print(" Pessoas afetadas: desconhecido")
        else:
            print(f" Pessoas afetadas: {pessoas} pessoas")

        print(f" Data: {ocorrencia['data']}")

# Ativa quando a opção 3 é selecionada, mostra as orientações em caso de enchente
def orientacoes():

    print("\n--- Orientações em Caso de Enchente ---")
    print("- Procure abrigo em locais elevados e seguros.")
    print("- Evite contato com a água da enchente.")
    print("- Desconecte aparelhos elétricos.")
    print("- Siga as recomendações das autoridades locais.")
    print("- Tenha sempre um kit de emergência preparado.")
    print("- Em caso de emergência, ligue para 193 (Bombeiros) ou 199 (Defesa Civil).")

# Ativa quando a opção 4 é selecionada, deleta uma ocorrencia
def deletar_ocorrencia(lista_ocorrencias):
    if(not lista_ocorrencias): # Se não tiver ocorrencia, não tem uso essa função, avisa e encerra
        print("Nenhuma ocorrência cadastrada.")
        return

    visualizar_ocorrencias(lista_ocorrencias) # Mostra as ocorrencias

    numero = input("Informe o número da ocorrência que deseja deletar: ") # Pede qual ocorrencia deve ser deletada

    if(numero.isdigit()):
        numero = int(numero) # Se for um digito, converte o input em inteiro, e deleta ele.
        if(1 <= numero <= len(lista_ocorrencias)):
            removida = lista_ocorrencias.pop(numero - 1)
            print(f"Ocorrência de {removida['local']} removida com sucesso.")
        else:
            print("Número inválido de ocorrência.")
    else:
        print("Formato inválido.") 

# Main que tem todas as funções
def main():
    # Cria a lista_ocorrencia que vai ser de extrema importancia
    lista_ocorrencias = []

    # Fica preso em um loop de menu
    while True:
        opcao = menu()

        if(opcao == 1):
            cadastrar_ocorrencia(lista_ocorrencias)
        elif(opcao == 2):
            visualizar_ocorrencias(lista_ocorrencias)
        elif(opcao == 3):
            orientacoes()
        elif(opcao == 4):
            deletar_ocorrencia(lista_ocorrencias)
        elif(opcao == 5): # Quebra o loop de menus
            print("Saindo do sistema. Até logo!")
            break

main() # Executa a main

