import os

URL_BASE_NO_SERVIDOR = "/imagens/avatars/"
NOME_DA_TABELA = "Avatar"
COLUNA_NOME = "nome"
COLUNA_CAMINHO = "caminho_foto"
CAMINHO_DA_PASTA_LOCAL = r"/home/iasmin/Documentos/Estudos/xpLearn/xplearn-backend/xplearn-backend/app/static/imagens/avatares"

def gerar_sql_inserts():
    comandos_sql = []

    try:
        nomes_dos_arquivos = os.listdir(CAMINHO_DA_PASTA_LOCAL)
    except FileNotFoundError:
        print(f"Erro: Pasta não encontrada em:")
        print(f"{CAMINHO_DA_PASTA_LOCAL}")
        return

    arquivos_de_imagem = [f for f in nomes_dos_arquivos if f.endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg'))]

    if not arquivos_de_imagem:
        print(f"Nenhum arquivo de imagem encontrado em {CAMINHO_DA_PASTA_LOCAL}")
        return

    # ✅ Ordena os arquivos numericamente (Avatar1, Avatar2, Avatar10, ...)
    arquivos_de_imagem.sort(key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))

    comandos_sql.append(f"INSERT INTO {NOME_DA_TABELA} ({COLUNA_NOME}, {COLUNA_CAMINHO}) VALUES")

    valores = []
    for nome_arquivo in arquivos_de_imagem:
        nome_base = os.path.splitext(nome_arquivo)[0]
        nome_amigavel = nome_base.replace('_', ' ').replace('-', ' ').title()
        url_final_no_banco = f"{URL_BASE_NO_SERVIDOR}{nome_arquivo}"
        valores.append(f"('{nome_amigavel}', '{url_final_no_banco}')")

    comandos_sql.append(",\n".join(valores) + ";")

    nome_arquivo_saida = "inserts_de_avatares_gerados.sql"
    with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
        f.write("\n".join(comandos_sql))

    print(f"✅ Sucesso! {len(arquivos_de_imagem)} registros foram gerados em ordem e salvos em:")
    print(f"{os.path.abspath(nome_arquivo_saida)}")

gerar_sql_inserts()
