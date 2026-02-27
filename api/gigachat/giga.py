from gigachat import GigaChat
from config import load_config

Authorization_key = load_config().auth_key
giga = GigaChat(
    credentials=Authorization_key,
    verify_ssl_certs=False,
)

def chat(message: str):
    return giga.chat(message)

