import random
import pickle

"""
Configure Random Numbers
"""
if __name__ == "__main__":
    seed = "s33d"
    LENGTH = 5000000

    random.seed(seed)
    with open("random_numbers", "wb") as f:
        numbers = [random.random() for n in range(LENGTH)]
        pickle.dump(numbers, f, protocol=pickle.HIGHEST_PROTOCOL)

"""
Access Random Numbers
"""
numbers = []
def setup_generator():
    global numbers
    with open("./random_seed/random_numbers", "rb") as f:
        numbers = pickle.load(f)

def next_number():
    try:
        return numbers.pop()
    except:
        return random.random()
