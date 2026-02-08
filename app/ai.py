from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

CATEGORIES = {
    "Database Error": "database connection failed timeout sql",
    "Authentication Error": "authentication token invalid unauthorized",
    "Network Issue": "network timeout connection refused unreachable",
    "Payment Failure": "payment failed transaction declined",
    "Unknown": "unexpected error unknown issue"
}


def analyze_log(message: str) -> tuple[str, int]:
    texts = list(CATEGORIES.values())
    embeddings = model.encode(texts, convert_to_tensor=True)
    log_embedding = model.encode(message, convert_to_tensor=True)

    scores = util.cos_sim(log_embedding, embeddings)[0]
    best_index = int(scores.argmax())

    category = list(CATEGORIES.keys())[best_index]
    confidence = int(scores[best_index].item() * 100)

    return category, confidence
