import os
import psycopg2
import psycopg2.extras # Essencial para retornar dicionários
from dotenv import load_dotenv
from typing import Dict, Any, Optional, List
from datetime import datetime
from src.shared.parsing import achatar_analise_cpted
from src.info_extraction.schemas import AnaliseCptedDoLocal
from werkzeug.security import check_password_hash

# Carrega as variáveis de ambiente do arquivo .env do repositório da API
load_dotenv()

def get_db_connection():
    """
    Cria e retorna uma nova conexão com o banco de dados.
    Lança uma exceção se a conexão falhar.
    Nota: Para aplicações de alta performance, considere usar um "connection pool".
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"ERRO CRÍTICO: Não foi possível conectar ao banco de dados. {e}")
        raise

def add_user_app(name: str, email: str, cpf: str, hashed_password: str) -> Optional[int]:
    """
    Adiciona um novo usuário do aplicativo (quem tira a foto) ao banco de dados.

    Args:
        name: Nome do usuário.
        email: Email do usuário (deve ser único).
        cpf: CPF do usuário (deve ser único).
        hashed_password: Senha do usuário já criptografada.

    Retorna:
        O ID do novo usuário ou None em caso de erro.
    """
    sql = "INSERT INTO user_app (name, email, cpf, password) VALUES (%s, %s, %s, %s) RETURNING id;"
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(sql, (name, email, cpf, hashed_password))
            user_id = cur.fetchone()[0]
            conn.commit()
            return user_id
    except psycopg2.errors.UniqueViolation:
        print(f"Erro: O email '{email}' ou CPF '{cpf}' já está cadastrado.")
        return None
    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao adicionar usuário: {error}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            conn.close()

def add_user_platform(name: str, email: str, cpf: str, hashed_password: str) -> Optional[int]:
    """
    Adiciona um novo usuário da plataforma (dashboard, admin) ao banco de dados.

    ATENÇÃO DE SEGURANÇA:
    A senha fornecida a esta função DEVE ser previamente tratada com um
    algoritmo de hash forte, como o bcrypt. NUNCA passe senhas em texto puro.

    Args:
        name (str): O nome completo do usuário.
        email (str): O email do usuário, que deve ser único.
        cpf (str): O CPF do usuário, que deve ser único.
        hashed_password (str): A senha já processada por um hash.

    Returns:
        Optional[int]: O ID do novo usuário criado, ou None em caso de erro
                         (por exemplo, se o email já existir).
    """
    # O SQL para inserir um novo usuário na tabela user_platform e retornar seu id.
    sql = "INSERT INTO user_platform (name, email, cpf, password) VALUES (%s, %s, %s, %s) RETURNING id;"

    conn = None
    try:
        # Pega uma nova conexão com o banco
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Executa o comando SQL, passando os dados de forma segura
            cur.execute(sql, (name, email, cpf, hashed_password))

            # Pega o ID retornado pelo comando 'RETURNING id'
            user_id = cur.fetchone()[0]
            
            # Se a execução foi bem-sucedida, salva a transação
            conn.commit()
            
            print(f"Usuário da plataforma '{name}' inserido com sucesso. ID: {user_id}")
            return user_id
            
    except psycopg2.errors.UniqueViolation:
        # Erro específico para quando o email (que é UNIQUE) já existe
        print(f"Erro: O email '{email}' ou CPF '{cpf}' já está cadastrado para um usuário da plataforma.")
        if conn:
            conn.rollback() # Reverte a transação
        return None
        
    except (Exception, psycopg2.Error) as error:
        # Captura outros possíveis erros de banco de dados
        print(f"Erro ao adicionar usuário da plataforma: {error}")
        if conn:
            conn.rollback() # Reverte a transação
        return None
        
    finally:
        # Garante que a conexão seja sempre fechada
        if conn:
            conn.close()


def find_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Busca um usuário do aplicativo pelo seu email.

    Retorna:
        Um dicionário com os dados do usuário ou None se não for encontrado.
    """
    sql = "SELECT * FROM user_app WHERE email = %s;"
    conn = None
    try:
        conn = get_db_connection()
        # DictCursor faz com que o resultado seja um dicionário (chave: valor)
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql, (email,))
            user = cur.fetchone()
            return dict(user) if user else None
    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao buscar usuário: {error}")
        return None
    finally:
        if conn:
            conn.close()


# ==============================================================================
# FUNÇÕES DO PIPELINE (CAPTURA E RESULTADO)
# ==============================================================================

def add_capture(user_app_id: int, url: str, date: datetime, lat: float, long: float) -> Optional[int]:
    """
    Adiciona uma nova captura (imagem de entrada do pipeline) ao banco de dados.

    Retorna:
        O ID da nova captura ou None em caso de erro.
    """
    sql = "INSERT INTO capture (user_app_id, url, date, lat, long) VALUES (%s, %s, %s, %s, %s) RETURNING id;"
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(sql, (user_app_id, url, date, lat, long))
            capture_id = cur.fetchone()[0]
            conn.commit()
            print(f"capture id:{capture_id}")
            return capture_id
    except psycopg2.errors.UniqueViolation:
        print(f"Erro: A URL '{url}' já foi capturada anteriormente.")
        return None
    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao inserir captura: {error}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            conn.close()


def add_pipeline_output(capture_id: int, dados: Dict) -> Optional[int]:
    """
    Adiciona o resultado processado pelo pipeline para uma captura existente.

    Args:
        capture_id: O ID da captura a que este resultado pertence.
        dados: O objeto AnaliseCptedDoLocal contendo os dados da análise.

    Retorna:
        O ID da nova linha em pipeline_output ou None em caso de erro.
    """
    # Achata o dicionário para que os valores sejam passados na ordem correta
    dados = AnaliseCptedDoLocal(**dados)
    dados_achatados = achatar_analise_cpted(dados)

    # Constrói a query dinamicamente para evitar SQL Injection e facilitar a manutenção
    colunas = ", ".join(dados_achatados.keys())
    placeholders = ", ".join(["%s"] * len(dados_achatados))

    sql = f"INSERT INTO pipeline_output (capture_id, {colunas}) VALUES (%s, {placeholders}) RETURNING id;"
    
    # Prepara a lista de valores na ordem correta
    valores = [int(capture_id)] + list(dados_achatados.values())

    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(sql, valores)
            output_id = cur.fetchone()[0]
            conn.commit()
            return output_id
    except psycopg2.errors.UniqueViolation:
        print(f"Erro: Já existe um resultado de pipeline para a captura ID {capture_id}.")
        return None
    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao inserir resultado do pipeline: {error}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            conn.close()


def get_all_analyses_for_map() -> List[Dict[str, Any]]:
    """
    Busca no banco de dados todas as análises que possuem coordenadas geográficas
    para a geração do mapa, incluindo a URL da imagem de captura.
    """

    sql = """
        SELECT
            c.lat,
            c.long AS lon,
            c.url AS capture_url,
            po.titulo_analise,
            po.indice_cpted_geral,
            po.resumo_executivo,
            po.recomendacoes,
            po.data_processamento
        FROM
            capture c
        JOIN
            pipeline_output po ON c.id = po.capture_id
        WHERE
            c.lat IS NOT NULL AND c.long IS NOT NULL;
    """
    conn = None
    results = []
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql)
            results = [dict(row) for row in cur.fetchall()]
    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao buscar dados para o mapa: {error}")
    finally:
        if conn:
            conn.close()
    return results

def get_full_analysis_by_url(url: str) -> Optional[Dict[str, Any]]:
    """
    Busca todos os dados relacionados a uma captura (usuário, captura e resultado)
    usando a URL da imagem como chave de busca. Esta é a principal função de "leitura".

    Retorna:
        Um dicionário com todos os dados combinados ou None se a URL não for encontrada.
    """
    sql = """
        SELECT
            ua.id AS user_id,
            ua.name AS user_name,
            ua.email AS user_email,
            c.id AS capture_id,
            c.url AS capture_url,
            c.date AS capture_date,
            c.lat,
            c.long,
            -- Usar um sub-SELECT com row_to_json é uma forma elegante
            -- de agrupar os resultados do pipeline em um objeto aninhado.
            (SELECT row_to_json(po) FROM pipeline_output po WHERE po.capture_id = c.id) AS pipeline_results
        FROM
            capture c
        JOIN
            user_app ua ON c.user_app_id = ua.id
        WHERE
            c.url = %s;
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql, (url,))
            resultado = cur.fetchone()
            return dict(resultado) if resultado else None
    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao buscar análise completa: {error}")
        return None
    finally:
        if conn:
            conn.close()

def get_all_captures_by_user(user_id: int) -> List[Dict[str, Any]]:
    """
    Busca todas as capturas feitas por um usuário específico.

    Args:
        user_id: O ID do usuário cujas capturas queremos buscar.

    Retorna:
        Uma lista de dicionários com os dados das capturas ou uma lista vazia se não houver capturas.
    """
    sql = """
        SELECT
            c.id AS capture_id,
            c.url AS capture_url,
            c.date AS capture_date,
            c.lat,
            c."long",
            (
                SELECT COALESCE(json_agg(row_to_json(po)), '[]'::json)
                FROM pipeline_output po
                WHERE po.capture_id = c.id
            ) AS pipeline_results
        FROM
            capture c
        WHERE
            c.user_app_id = %s;
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql, (user_id,))
            resultados = cur.fetchall()
            return [dict(r) for r in resultados] if resultados else []
    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao buscar capturas do usuário {user_id}: {error}")
        return []
    finally:
        if conn:
            conn.close()

def get_all_users() -> List[Dict[str, Any]]:
    """
    Busca todos os usuários do aplicativo.

    Retorna:
        Uma lista de dicionários com os dados de cada usuário.
    """
    sql = "SELECT * FROM user_app;"
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql)
            resultados = cur.fetchall()
            return [dict(r) for r in resultados] if resultados else []
    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao buscar usuários: {error}")
        return []
    finally:
        if conn:
            conn.close()

def get_all_platform_users() -> List[Dict[str, Any]]:
    """
    Busca todos os usuários da plataforma (dashboard, admin).

    Retorna:
        Uma lista de dicionários com os dados de cada usuário da plataforma.
    """
    sql = "SELECT * FROM user_platform;"
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql)
            resultados = cur.fetchall()
            return [dict(r) for r in resultados] if resultados else []
    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao buscar usuários da plataforma: {error}")
        return []
    finally:
        if conn:
            conn.close()

def get_capture_by_id(capture_id: int) -> Optional[Dict[str, Any]]:
    """
    Busca uma captura específica pelo seu ID.

    Args:
        capture_id: O ID da captura a ser buscada.

    Retorna:
        Um dicionário com os dados da captura ou None se não for encontrada.
    """
    sql = "SELECT * FROM capture WHERE id = %s;"
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql, (capture_id,))
            resultado = cur.fetchone()
            return dict(resultado) if resultado else None
    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao buscar captura ID {capture_id}: {error}")
        return None
    finally:
        if conn:
            conn.close()

def get_pipeline_output_by_capture_id(capture_id: int) -> Optional[Dict[str, Any]]:
    """
    Busca o resultado do pipeline para uma captura específica pelo seu ID.

    Args:
        capture_id: O ID da captura cujo resultado do pipeline queremos buscar.

    Retorna:
        Um dicionário com os dados do resultado do pipeline ou None se não for encontrado.
    """
    sql = "SELECT * FROM pipeline_output WHERE capture_id = %s;"
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql, (capture_id,))
            resultado = cur.fetchone()
            return dict(resultado) if resultado else None
    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao buscar resultado do pipeline para captura ID {capture_id}: {error}")
        return None
    finally:
        if conn:
            conn.close()    

def login_user_app(email: str, senha_digitada: str) -> bool:
    """
    Faz o login de um usuário do aplicativo.

    Verifica se o email existe e se a senha corresponde ao hash armazenado.

    Args:
        email (str): Email do usuário.
        senha_digitada (str): Senha que o usuário digitou.

    Returns:
        bool: True se o login for bem-sucedido, False caso contrário.
    """
    sql = "SELECT password FROM user_app WHERE email = %s;"
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(sql, (email,))
            resultado = cur.fetchone()

            if resultado is None:
                print("Usuário não encontrado.")
                return False

            senha_hash = resultado[0]

            # Faz a verificação usando Werkzeug
            if check_password_hash(senha_hash, senha_digitada):
                print("Login bem-sucedido!")
                return True
            else:
                print("Senha incorreta.")
                return False

    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao tentar fazer login: {error}")
        return False
    finally:
        if conn:
            conn.close()