import os

# --- Configurações (Ajuste a Linha 11) ---

# 1. Este é o caminho QUE ESTÁ NO SEU BANCO. Está perfeito.
#    (É o caminho que o servidor usará para encontrar a imagem)
URL_BASE_NO_SERVIDOR = "/imagens/avatars/"

# 2. Nome da sua tabela (conforme seu script SQL)
NOME_DA_TABELA = "Avatar"

# 3. Colunas da sua tabela (conforme seu script SQL)
COLUNA_NOME = "nome"
COLUNA_CAMINHO = "caminho_foto"

# 4. !!! IMPORTANTE !!!
#    Coloque aqui o caminho ABSOLUTO (completo) no SEU COMPUTADOR
#    para a pasta onde estão as 115 imagens.
#    (Ex: "C:\Users\SeuNome\Documentos\projetos\xplearn-backend\app\static\imagens\avatares")
CAMINHO_DA_PASTA_LOCAL = r"/home/iasmin/Documentos/Estudos/xpLearn/xplearn-backend/xplearn-backend/app/static/imagens/avatares"
# -----------------------------------------------------------------

def gerar_sql_inserts():
    comandos_sql = []
    
    try:
        nomes_dos_arquivos = os.listdir(CAMINHO_DA_PASTA_LOCAL)
    except FileNotFoundError:
        print(f"Erro: Pasta não encontrada em:")
        print(f"{CAMINHO_DA_PASTA_LOCAL}")
        print("---")
        print("Por favor, ajuste a variável 'CAMINHO_DA_PASTA_LOCAL' no script.")
        print("O caminho precisa ser o caminho *completo* no seu computador.")
        return

    # Filtra para incluir apenas imagens
    arquivos_de_imagem = [f for f in nomes_dos_arquivos if f.endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg'))]
    
    if not arquivos_de_imagem:
        print(f"Nenhum arquivo de imagem encontrado em {CAMINHO_DA_PASTA_LOCAL}")
        return

    # Gera o início do comando INSERT
    comandos_sql.append(f"INSERT INTO {NOME_DA_TABELA} ({COLUNA_NOME}, {COLUNA_CAMINHO}) VALUES")

    valores = []
    for nome_arquivo in arquivos_de_imagem:
        
        # --- Lógica para criar um nome amigável ---
        # Pega o nome do arquivo sem a extensão (ex: 'ninja.png' -> 'ninja')
        nome_base = os.path.splitext(nome_arquivo)[0]
        # Transforma o nome (ex: 'ninja' -> 'Ninja', 'avatar_samurai' -> 'Avatar Samurai')
        nome_amigavel = nome_base.replace('_', ' ').replace('-', ' ').title()
        
        # Monta a URL final que será salva no banco
        url_final_no_banco = f"{URL_BASE_NO_SERVIDOR}{nome_arquivo}"
        
        # Adiciona o valor formatado para SQL
        valores.append(f"('{nome_amigavel}', '{url_final_no_banco}')")

    # Junta todos os valores com vírgulas e finaliza com ponto e vírgula
    comandos_sql.append(",\n".join(valores) + ";")
    
    # Salva tudo em um arquivo .sql
    nome_arquivo_saida = "inserts_de_avatares_gerados.sql"
    with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
        f.write("\n".join(comandos_sql))
        
    print(f"Sucesso! Os {len(arquivos_de_imagem)} comandos de INSERT foram salvos no arquivo:")
    print(f"{os.path.abspath(nome_arquivo_saida)}")
    print("\nAbra esse arquivo, copie o conteúdo e cole no seu script SQL principal.")

# Roda a função
gerar_sql_inserts()