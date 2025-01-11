from transformers import AutoTokenizer, AutoModel


def load_model(model_name: str):
    model = AutoModel.from_pretrained(model_name)
    return model


def load_tokenizer(model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return tokenizer
