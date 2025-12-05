import random

nouns = ["cat", "dog", "robot", "teacher", "car"]
verbs = ["jumps", "runs", "flies", "talks", "sings"]
adjectives = ["happy", "lazy", "funny", "smart", "loud"]
adverbs = ["quickly", "slowly", "silently", "happily", "sadly"]


def random_sentences(count: int = 1) -> str:
    sentences = []

    for _ in range(count):
        sentences.append(
            f"The {random.choice(adjectives)} {random.choice(nouns)} {random.choice(verbs)} {random.choice(adverbs)}."
        )

    return " ".join(sentences)
