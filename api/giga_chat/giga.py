from gigachat import GigaChat

from .promt import promt
from config import load_config

Authorization_key = load_config().auth_key
giga = GigaChat(
    credentials=Authorization_key,
    verify_ssl_certs=False,
)

def chat(nlp_metrics_json, physiological_metrics_json, cardio_metrics_json, productivity_metrics_json):
    return giga.chat(promt(nlp_metrics_json,
                           physiological_metrics_json,
                           cardio_metrics_json,
                           productivity_metrics_json))

