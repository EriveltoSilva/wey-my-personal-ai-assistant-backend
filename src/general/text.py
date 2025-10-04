import re
import unicodedata


def slugify(value:str, allow_unicode:bool=False)->str:
    """
    Converte para letras minúsculas, remove caracteres não-alfanuméricos,
    e converte espaços em hifens. Remove acentuação por padrão.

    Parâmetros:
        value (str): A string a ser convertida em slug.
        allow_unicode (bool): Se True, permite caracteres Unicode no slug.
                              Se False, converte para ASCII puro.

    Retorna:
        str: O slug formatado.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        # Remove acentos convertendo para ASCII
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')

    # Remove tudo que não for letra, número, hífen ou espaço
    value = re.sub(r'[^\w\s-]', '', value.lower())
    # Substitui espaços e múltiplos hifens por um único hífen
    value = re.sub(r'[-\s]+', '-', value).strip('-')
    return value
