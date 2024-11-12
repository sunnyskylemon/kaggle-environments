import random
from .utils import get_score


def rock(observation, configuration):
    return 0


def paper(observation, configuration):
    return 1


def scissors(observation, configuration):
    return 2


def copy_opponent(observation, configuration):
    if observation.step > 0:
        return observation.lastOpponentAction
    else:
        return random.randrange(0, configuration.signs)
        
#Мой код
# Агент, который всегда выбирает камень, если противник выбирает бумагу
def copy_opponent_rock(observation, configuration):
    return rock(observation, configuration)  # Всегда выбирает "камень"

# Агент, который всегда выбирает бумагу, если противник выбирает камень
def copy_opponent_paper(observation, configuration):
    return paper(observation, configuration)  # Всегда выбирает "бумагу"

# Агент, который всегда выбирает ножницы, если противник выбирает камень
def copy_opponent_scissors(observation, configuration):
    return scissors(observation, configuration)  # Всегда выбирает "ножницы"

# Агент, который выбирает камень, если противник выбрал бумагу
def copy_rock_if_paper(observation, configuration):
    if observation.step > 0 and observation.lastOpponentAction == 1:  # Бумага
        return rock(observation, configuration)  # Камень бьет бумагу
    return random.randrange(0, configuration.signs)

# Агент, который выбирает бумагу, если противник выбрал ножницы
def copy_paper_if_scissors(observation, configuration):
    if observation.step > 0 and observation.lastOpponentAction == 2:  # Ножницы
        return paper(observation, configuration)  # Бумага бьет ножницы
    return random.randrange(0, configuration.signs)

# Агент, который выбирает ножницы, если противник выбрал камень
def copy_scissors_if_rock(observation, configuration):
    if observation.step > 0 and observation.lastOpponentAction == 0:  # Камень
        return scissors(observation, configuration)  # Ножницы бьют камень
    return random.randrange(0, configuration.signs)

# Агент, который меняет свое поведение на то, что побеждает последнее действие противника
def copy_changing(observation, configuration):
    if observation.step > 0:
        return (observation.lastOpponentAction + 1) % configuration.signs  # Меняет действие на то, которое побеждает последнее
    return random.randrange(0, configuration.signs)

# Агент, который выбирает случайный ход
def copy_random(observation, configuration):
    return random.randrange(0, configuration.signs)  # Случайный выбор

# Агент, который реагирует на действия противника
last_react_action = None

def reactionary(observation, configuration):
    global last_react_action
    if observation.step == 0:
        last_react_action = random.randrange(0, configuration.signs)
    elif get_score(last_react_action, observation.lastOpponentAction) <= 1:
        last_react_action = (observation.lastOpponentAction + 1) % configuration.signs

    return last_react_action


last_counter_action = None


def counter_reactionary(observation, configuration):
    global last_counter_action
    if observation.step == 0:
        last_counter_action = random.randrange(0, configuration.signs)
    elif get_score(last_counter_action, observation.lastOpponentAction) == 1:
        last_counter_action = (last_counter_action + 2) % configuration.signs
    else:
        last_counter_action = (observation.lastOpponentAction + 1) % configuration.signs

    return last_counter_action


action_histogram = {}


def statistical(observation, configuration):
    global action_histogram
    if observation.step == 0:
        action_histogram = {}
        return
    action = observation.lastOpponentAction
    if action not in action_histogram:
        action_histogram[action] = 0
    action_histogram[action] += 1
    mode_action = None
    mode_action_count = None
    for k, v in action_histogram.items():
        if mode_action_count is None or v > mode_action_count:
            mode_action = k
            mode_action_count = v
            continue

    return (mode_action + 1) % configuration.signs


agents = {
    "rock": rock,
    "paper": paper,
    "scissors": scissors,
    "copy_opponent": copy_opponent,
    "reactionary": reactionary,
    "counter_reactionary": counter_reactionary,
    "statistical": statistical,
    "copy_opponent_rock": copy_opponent_rock,
    "copy_opponent_paper": copy_opponent_paper,
    "copy_opponent_scissors": copy_opponent_scissors,
    "copy_rock_if_paper": copy_rock_if_paper,
    "copy_paper_if_scissors": copy_paper_if_scissors,
    "copy_scissors_if_rock": copy_scissors_if_rock
}
