import pybase62
import hashlib

def generate_hash_short_code(url: str, length=6):
    """
    Gera um short_code baseado no hash MD5 da URL original,
    convertendo o resultado para Base62.
    """
    # Cria um hash MD5 da URL
    hash_object = hashlib.md5(url.encode())
    # Converte o hash hexadecimal para um número inteiro
    hash_int = int(hash_object.hexdigest(), 16)
    # Codifica o número inteiro em Base62
    short_code = pybase62.encode(hash_int)
    # Retorna os primeiros caracteres conforme o tamanho desejado
    return short_code[:length]
