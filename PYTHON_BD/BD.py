import json
import os

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_BD = os.path.join(PASTA_ATUAL, "ocorrencias.json")

def carregar_ocorrencias():
    """Carrega o banco de dados de ocorrências do arquivo JSON."""
    if os.path.exists(ARQUIVO_BD):
        with open(ARQUIVO_BD, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_ocorrencias(lista_ocorrencias):
    """Salva o banco de dados de ocorrências no arquivo JSON."""
    with open(ARQUIVO_BD, "w", encoding="utf-8") as f:
        json.dump(lista_ocorrencias, f, indent=2, ensure_ascii=False)

# Função pra permitir que o nivel da agua receba valores decimais
def decimal_agua(valor):
    partes = valor.split(".")
    return len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit()

# Função para o menu
def menu():
    print("\n--- Sistema de Monitoramento de Enchentes ---")
    print("1. Cadastrar ocorrência de enchente")
    print("2. Visualizar estatísticas")
    print("3. Orientações em caso de enchente")
    print("4. Deletar ocorrência")
    print("5. Sair")
    while True:
        opcao = input("Escolha uma opção: ")
        if opcao.isdigit():
            opcao = int(opcao)
            if opcao in [1,2,3,4,5]:
                return opcao
            else:
                print("Opção inválida. Tente novamente.")
        else:
            print("Tipo de valor na opção invalido!")

# Ativa quando a opção 1 é selecionada, para cadastrar ocorrencias de enchente
def cadastrar_ocorrencia(lista_ocorrencias):
    print("\nCadastro de Ocorrência")
    cidade = input("Informe a cidade (Nome inteiro sem abreviações): ").strip()
    if cidade == "":
        print("A cidade deve ser informada!")
        return
    nivel_agua = input("Nível da água em centímetros (se não souber deixe em branco): ")
    if nivel_agua == "":
        nivel_agua = "desconhecido"
        print("Nível de água foi colocado como 'Desconhecido'")
    elif (nivel_agua.isdigit() or decimal_agua(nivel_agua)):
        nivel_agua = float(nivel_agua)
        if nivel_agua < 0:
            print("Nível de água não pode ser negativo.")
            return
    else:
        print("Formato de valor inválido!")
        return
    pessoas_afetadas = input("Número de pessoas afetadas (se não souber deixe em branco): ")
    if pessoas_afetadas == "":
        pessoas_afetadas = "desconhecido"
        print("Numero de pessoas afetadas foi colocado como 'Desconhecido'")
    elif pessoas_afetadas.isdigit():
        pessoas_afetadas = int(pessoas_afetadas)
        if pessoas_afetadas < 0:
            print("Numero de pessoas afetadas não pode ser negativo.")
            return
    else:
        print("Formato de valor inválido!")
        return
    ano = 2025
    mes = input("Qual o mês da ocorrencia (use o número, ex: 1 para Janeiro): ").strip()
    if mes.isdigit():
        mes = int(mes)
        if mes > 12 or mes < 1:
            print("Valor absurdo, logo não será aceito")
            return
    else:
        print("Formato de valor inválido!")
        return
    dia = input("Qual o dia da ocorrencia: ").strip()
    if dia.isdigit():
        dia = int(dia)
        if dia > 31 or dia < 1:
            print("Valor absurdo, logo não será aceito")
            return
    else:
        print("Formato de valor inválido!")
        return
    data = f"{dia:02d}/{mes:02d}/{ano}"
    ocorrencia = {
        'cidade': cidade,
        'nivel_agua': nivel_agua,
        'pessoas_afetadas': pessoas_afetadas,
        'data': data
    }
    lista_ocorrencias.append(ocorrencia)
    salvar_ocorrencias(lista_ocorrencias)
    print("Ocorrência cadastrada com sucesso!")

# Ativa quando a opção 2 é selecionada, mostra as enchentes registradas
def visualizar_estatisticas(lista_ocorrencias):
    print("\n--- Estatísticas de Ocorrências ---")
    if not lista_ocorrencias:
        print("Nenhuma ocorrência cadastrada.")
        return
    for i, ocorrencia in enumerate(lista_ocorrencias):
        print(f"\nOcorrência {i+1}:")
        print(f" Cidade: {ocorrencia['cidade']}")
        print(f" Nível da água: {ocorrencia['nivel_agua']}")
        print(f" Pessoas afetadas: {ocorrencia['pessoas_afetadas']}")
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
    if not lista_ocorrencias:
        print("Nenhuma ocorrência cadastrada.")
        return
    visualizar_estatisticas(lista_ocorrencias)
    numero = input("Informe o número da ocorrência que deseja deletar: ")
    if numero.isdigit():
        numero = int(numero)
        if 1 <= numero <= len(lista_ocorrencias):
            removida = lista_ocorrencias.pop(numero - 1)
            salvar_ocorrencias(lista_ocorrencias)
            print(f"Ocorrência de {removida['cidade']} removida com sucesso.")
        else:
            print("Número inválido de ocorrência.")
    else:
        print("Formato inválido.")

# Main que tem todas as funções
def main():
    lista_ocorrencias = carregar_ocorrencias()
    while True:
        opcao = menu()
        if opcao == 1:
            cadastrar_ocorrencia(lista_ocorrencias)
        elif opcao == 2:
            visualizar_estatisticas(lista_ocorrencias)
        elif opcao == 3:
            orientacoes()
        elif opcao == 4:
            deletar_ocorrencia(lista_ocorrencias)
        elif opcao == 5:
            print("Saindo do sistema. Até logo!")
            break

main()