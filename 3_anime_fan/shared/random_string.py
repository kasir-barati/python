import random
import string


def random_string(length: int) -> str:
    result = ''.join(random.choice(string.ascii_letters) for _ in range(length))

    return result


# previous_random: list[str] = []
# while True:
#     generated_random = random_string(20)
#     if any(generated_random in x for x in previous_random):
#         print(len(previous_random))
#         raise Exception("Duplicate")
#     previous_random.append(generated_random)