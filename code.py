from tinydb import TinyDB, Query
from tabulate import tabulate

db = TinyDB('colaboracoes_db.json')

def exibir_ranking():
    try:
        colaboracoes = db.all()
        if not colaboracoes:
            print("Nenhuma colaboração registrada.")
            return

        ranking = [(item['empresa'], len(item['colaboracoes'].split('; ')), item['colaboracoes']) for item in colaboracoes]
        ranking_sorted = sorted(ranking, key=lambda x: x[1], reverse=True)

        table = [["Posição", "Empresa", "Número de Colaborações", "Colaborações"]]
        for idx, (empresa, num_colabs, colaboracao) in enumerate(ranking_sorted, start=1):
            table.append([idx, empresa, num_colabs, colaboracao])
        print(tabulate(table, headers="firstrow", tablefmt="grid"))
    #aqui
    except Exception as e:
        print(f"Ocorreu um erro ao exibir o ranking: {e}")
        #aqui

def adicionar_colaboracao():
    try:
        empresa = input("Digite o nome da empresa: ")
        while True:
            colaboracao = input("Digite como a empresa ajudou: ")
            Empresa = Query()
            resultado = db.search(Empresa.empresa == empresa)
            if resultado:
                novas_colaboracoes = resultado[0]['colaboracoes'] + f"; {colaboracao}"
                db.update({'colaboracoes': novas_colaboracoes}, Empresa.empresa == empresa)
            else:
                db.insert({'empresa': empresa, 'colaboracoes': colaboracao})
            print("Colaboração adicionada com sucesso.")

            while True:
                outra = input("Deseja adicionar outra colaboração para a mesma empresa? (s/n): ").strip().lower()
                if outra in ('s', 'n'):
                    break
                print("Opção inválida. Por favor, digite 's' para sim ou 'n' para não.")

            if outra != 's':
                break

        # Retorna as colaborações atualizadas após adição
        return db.search(Empresa.empresa == empresa)[0]['colaboracoes']
    #aqui
    except Exception as e:
        print(f"Ocorreu um erro ao adicionar colaboração: {e}")
    #quui
def remover_colaboracao():
    try:
        empresa = input("Digite o nome da empresa: ")
        Empresa = Query()
        resultado = db.search(Empresa.empresa == empresa)
        if resultado:
            contribuicoes = resultado[0]['colaboracoes'].split('; ')
            print("Contribuições da empresa:")
            for idx, contrib in enumerate(contribuicoes, start=1):
                print(f"{idx}. {contrib}")

            while True:
                idx_remover = input("Digite o número da contribuição que deseja remover (ou '0' para cancelar): ").strip()
                if idx_remover.isdigit():
                    idx_remover = int(idx_remover)
                    if 0 < idx_remover <= len(contribuicoes):
                        idx_remover -= 1
                        break
                    else:
                        print("Número inválido. Por favor, escolha um número dentro do intervalo.")
                elif idx_remover == '0':
                    print("Operação cancelada.")
                    return None
                else:
                    print("Entrada inválida. Por favor, insira um número.")

            del contribuicoes[idx_remover]
            novas_colaboracoes = '; '.join(contribuicoes)
            if novas_colaboracoes:
                db.update({'colaboracoes': novas_colaboracoes}, Empresa.empresa == empresa)
            else:
                db.remove(Empresa.empresa == empresa)
            print("Contribuição removida com sucesso.")

            # Verifica se ainda há colaborações após a remoção
            if not db.search(Empresa.empresa == empresa):
                print("Não há mais colaborações para esta empresa. Removendo a entrada.")
                db.remove(Empresa.empresa == empresa)

            # Retorna as colaborações atualizadas após remoção
            return novas_colaboracoes

        else:
            print("Empresa não encontrada no registro de colaborações.")
            return None
        #aqui
    except Exception as e:
        print(f"Ocorreu um erro ao remover colaboração: {e}")

def menu():
    while True:
        print("\nMenu de Ranking de Empresas:")
        print("1. Exibir o ranking de empresas que mais colaboraram")
        print("2. Adicionar uma colaboração que sua empresa fez")
        print("3. Remover uma colaboração que sua empresa fez")
        print("4. Encerrar programa")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            exibir_ranking()
        elif opcao == '2':
            # Atualiza o banco de dados com as colaborações após adição
            colaboracoes_atualizadas = adicionar_colaboracao()
            if colaboracoes_atualizadas is not None:
                print("Colaborações atualizadas:", colaboracoes_atualizadas)
        elif opcao == '3':
            # Atualiza o banco de dados com as colaborações após remoção
            colaboracoes_atualizadas = remover_colaboracao()
            if colaboracoes_atualizadas is not None:
                print("Colaborações atualizadas:", colaboracoes_atualizadas)
        elif opcao == '4':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida, por favor tente novamente.")

if __name__ == "__main__":
    menu()
