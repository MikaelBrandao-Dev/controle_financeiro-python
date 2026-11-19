import json
import os

ARQUIVO = "lancamentos.json"


def carregar_dados():
    # Se ainda nao existir arquivo salvo, comeca com a lista vazia
    if not os.path.exists(ARQUIVO):
        return []

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            # Garante que o arquivo tem uma lista no formato esperado
            if isinstance(dados, list):
                return dados
            print("Formato inesperado no arquivo anterior. Comecando uma lista nova.")
            return []
    except Exception:
        print("Nao deu pra ler o arquivo anterior. Comecando uma lista nova.")
        return []


def salvar_dados(lista):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)


def novo_lancamento(lista):
    desc = input("Descricao do lancamento: ").strip()
    if desc == "":
        print("Voce precisa informar uma descricao.")
        return

    while True:
        tipo = input("E entrada ou saida? (E/S): ").strip().lower()
        if tipo in ("e", "entrada"):
            tipo = "entrada"
            break
        elif tipo in ("s", "saida", "saída"):
            tipo = "saida"
            break
        else:
            print("Digite apenas E para entrada ou S para saida.")

    while True:
        # Troca virgula por ponto caso o usuario digite no padrao brasileiro
        valor_texto = input("Valor R$: ").strip().replace(",", ".")
        try:
            valor = float(valor_texto)
            if valor <= 0:
                print("O valor precisa ser maior que zero.")
                continue
            valor = round(valor, 2)
            break
        except ValueError:
            print("Valor invalido, tente novamente (ex: 35.90).")

    lista.append({
        "descricao": desc,
        "tipo": tipo,
        "valor": valor
    })
    salvar_dados(lista)
    print("Salvo!")


def listar(lista):
    if len(lista) == 0:
        print("\nNenhum registro encontrado.")
        return

    print("\n--- Seus Lancamentos ---")
    for idx, item in enumerate(lista, start=1):
        sinal = "+" if item["tipo"] == "entrada" else "-"
        print(f"{idx}. {item['descricao']} ({item['tipo']}) -> {sinal} R$ {item['valor']:.2f}")


def resumo(lista):
    entradas = 0.0
    saidas = 0.0

    for item in lista:
        if item["tipo"] == "entrada":
            entradas += item["valor"]
        elif item["tipo"] == "saida":
            saidas += item["valor"]

    saldo = entradas - saidas

    print("\n--- Resumo Geral ---")
    print(f"Entradas: R$ {entradas:.2f}")
    print(f"Saidas:   R$ {saidas:.2f}")
    print(f"Saldo:    R$ {saldo:.2f}")


def excluir(lista):
    if len(lista) == 0:
        print("\nLista vazia, nada para excluir.")
        return

    listar(lista)
    opcao = input("Numero do item para apagar (Enter para voltar): ").strip()
    if opcao == "":
        return

    if not opcao.isdigit():
        print("Informe apenas o numero do item.")
        return

    pos = int(opcao) - 1
    if pos < 0 or pos >= len(lista):
        print("Esse numero nao existe na lista.")
        return

    apagado = lista.pop(pos)
    salvar_dados(lista)
    print(f"Item '{apagado['descricao']}' removido.")


def main():
    lancamentos = carregar_dados()

    while True:
        print("\n===============================")
        print("  CONTROLE DE GASTOS - TERMINAL")
        print("===============================")
        print("1 - Novo lancamento")
        print("2 - Listar tudo")
        print("3 - Ver saldo e totais")
        print("4 - Excluir lancamento")
        print("0 - Sair")
        print("-------------------------------")
        print("Dev: MikaelBrandao-Dev")

        escolha = input("\nOpcao: ").strip()

        if escolha == "1":
            novo_lancamento(lancamentos)
        elif escolha == "2":
            listar(lancamentos)
        elif escolha == "3":
            resumo(lancamentos)
        elif escolha == "4":
            excluir(lancamentos)
        elif escolha == "0":
            print("\nEncerrando... | MikaelBrandao-Dev")
            break
        else:
            print("Opcao invalida.")


if _name_ == "_main_":
    main()
