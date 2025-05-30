import mysql.connector

DB_CONFIG = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "database": "enchentes_BD"
}

def conectar_mysql():
    return mysql.connector.connect(**DB_CONFIG)

def decimal_agua(valor):
    partes = valor.split(".")
    return len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit()

def menu():
    print("\n--- Sistema de Monitoramento de Enchentes ---")
    print("1. Cadastrar ocorrência de enchente")
    print("2. Visualizar ocorrências")
    print("3. Orientações em caso de enchente")
    print("4. Deletar ocorrência")
    print("5. Sair")
    while True:
        opcao = input("Escolha uma opção: ")
        if(opcao.isdigit()):
            opcao = int(opcao)
            if(opcao in [1,2,3,4,5]):
                return opcao
            else:
                print("Opção inválida. Tente novamente.")
        else:
            print("Tipo de valor na opção invalido!")

def carregar_ocorrencias():
    conn = conectar_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT cidade, nivel_agua, pessoas_afetadas, data_enchente FROM registros")
    ocorrencias = cursor.fetchall()
    cursor.close()
    conn.close()
    return ocorrencias

def salvar_ocorrencia(ocorrencia):
    conn = conectar_mysql()
    cursor = conn.cursor()
    query = """
        INSERT INTO registros (cidade, nivel_agua, pessoas_afetadas, data_enchente)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (
        ocorrencia['cidade'],
        None if ocorrencia['nivel_agua'] == "desconhecido" else ocorrencia['nivel_agua'],
        None if ocorrencia['pessoas_afetadas'] == "desconhecido" else ocorrencia['pessoas_afetadas'],
        ocorrencia['data_mysql']
    ))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_ocorrencia_por_indice(indice):
    ocorrencias = carregar_ocorrencias()
    if(0 <= indice < len(ocorrencias)):
        ocorrencia = ocorrencias[indice]
        conn = conectar_mysql()
        cursor = conn.cursor()
        conditions = []
        params = []
        for campo in ['cidade', 'nivel_agua', 'pessoas_afetadas', 'data_enchente']:
            if(ocorrencia[campo] is not None):
                conditions.append(f"{campo} = %s")
                params.append(ocorrencia[campo])
            else:
                conditions.append(f"{campo} IS NULL")
        query = f"""
            DELETE FROM registros
            WHERE {' AND '.join(conditions)}
            LIMIT 1
        """
        cursor.execute(query, tuple(params))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Ocorrência de {ocorrencia['cidade']} removida com sucesso.")
    else:
        print("Número inválido de ocorrência.")

def cadastrar_ocorrencia():
    print("\nCadastro de Ocorrência")
    cidade = input("Informe a cidade (Nome inteiro sem abreviações): ").strip()
    if(cidade == ""):
        print("A cidade deve ser informada!")
        return
    nivel_agua = input("Nível da água em metros (se não souber deixe em branco): ")
    if(nivel_agua == ""):
        nivel_agua = "desconhecido"
        print("Nível de água foi colocado como 'Desconhecido'")
    elif(nivel_agua.isdigit() or decimal_agua(nivel_agua)):
        nivel_agua = float(nivel_agua)
        if(nivel_agua < 0):
            print("Nível de água não pode ser negativo.")
            return
    else:
        print("Formato de valor inválido!")
        return
    pessoas_afetadas = input("Número de pessoas afetadas (se não souber deixe em branco): ")
    if(pessoas_afetadas == ""):
        pessoas_afetadas = "desconhecido"
        print("Numero de pessoas afetadas foi colocado como 'Desconhecido'")
    elif(pessoas_afetadas.isdigit()):
        pessoas_afetadas = int(pessoas_afetadas)
        if(pessoas_afetadas < 0):
            print("Numero de pessoas afetadas não pode ser negativo.")
            return
    else:
        print("Formato de valor inválido!")
        return
    ano = 2025
    mes = input("Qual o mês da ocorrencia (use o número, ex: 1 para Janeiro): ").strip()
    if(mes.isdigit()):
        mes = int(mes)
        if(mes > 12 or mes < 1):
            print("Valor absurdo, logo não será aceito")
            return
    else:
        print("Formato de valor inválido!")
        return
    dia = input("Qual o dia da ocorrencia: ").strip()
    if(dia.isdigit()):
        dia = int(dia)
        if(dia > 31 or dia < 1):
            print("Valor absurdo, logo não será aceito")
            return
    else:
        print("Formato de valor inválido!")
        return
    data = f"{dia:02d}/{mes:02d}/{ano}"

    data_mysql = f"{ano}-{mes:02d}-{dia:02d}"
    ocorrencia = {
        'cidade': cidade,
        'nivel_agua': nivel_agua,
        'pessoas_afetadas': pessoas_afetadas,
        'data': data,
        'data_mysql': data_mysql
    }
    salvar_ocorrencia(ocorrencia)
    print("Ocorrência cadastrada com sucesso!")

def visualizar_ocorrencias():
    print("\n--- Estatísticas de Ocorrências ---")
    lista_ocorrencias = carregar_ocorrencias()
    if(not lista_ocorrencias):
        print("Nenhuma ocorrência cadastrada.")
        return
    for i, ocorrencia in enumerate(lista_ocorrencias):
        print(f"\nOcorrência {i+1}:")
        print(f" Cidade: {ocorrencia['cidade']}")

        nivel = ocorrencia['nivel_agua']
        if(nivel is None):
            print(" Nível da água: Desconhecido")
        else:
            print(f" Nível da água: {nivel} metros")

        pessoas = ocorrencia['pessoas_afetadas']
        if(pessoas is None):
            print(" Pessoas afetadas: Desconhecido")
        else:
            print(f" Pessoas afetadas: {pessoas} pessoas")

        print(f" Data: {ocorrencia['data_enchente']}")

def deletar_ocorrencia():
    lista_ocorrencias = carregar_ocorrencias()
    if(not lista_ocorrencias):
        print("Nenhuma ocorrência cadastrada.")
        return
    visualizar_ocorrencias()
    numero = input("Informe o número da ocorrência que deseja deletar: ")
    if(numero.isdigit()):
        numero = int(numero)
        if(1 <= numero <= len(lista_ocorrencias)):
            deletar_ocorrencia_por_indice(numero - 1)
        else:
            print("Número inválido de ocorrência.")
    else:
        print("Formato inválido.")

def orientacoes():
    print("\n--- Orientações em caso de enchente ---")
    print("- Mantenha a calma e procure abrigo em locais altos.")
    print("- Evite contato com a água da enchente.")
    print("- Desligue os aparelhos elétricos e feche o registro de água e gás.")
    print("- Siga as orientações da Defesa Civil e Corpo de Bombeiros.")
    print("- Se possível, leve documentos, medicamentos e itens essenciais.")

def main():
    while True:
        opcao = menu()
        if(opcao == 1):
            cadastrar_ocorrencia()
        elif(opcao == 2):
            visualizar_ocorrencias()
        elif(opcao == 3):
            orientacoes()
        elif(opcao == 4):
            deletar_ocorrencia()
        elif(opcao == 5):
            print("Saindo do sistema. Até logo!")
            break

if __name__ == "__main__":
    main()
