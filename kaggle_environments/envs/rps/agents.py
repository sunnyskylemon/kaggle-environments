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

def favor_scissors(observation, configuration):
    return 2  # Всегда выбирает ножницы

def favor_paper(observation, configuration):
    return 1  # Всегда выбирает бумагу

def favor_rock(observation, configuration):
    return 0  # Всегда выбирает камень

# Дополнительные агенты
def random_favor_rock(observation, configuration):
    """Случайный агент, чаще выбирающий камень"""
    return random.choices([0, 1, 2], weights=[0.5, 0.25, 0.25])[0]

def random_favor_paper(observation, configuration):
    """Случайный агент, чаще выбирающий бумагу"""
    return random.choices([0, 1, 2], weights=[0.25, 0.5, 0.25])[0]

def random_favor_scissors(observation, configuration):
    """Случайный агент, чаще выбирающий ножницы"""
    return random.choices([0, 1, 2], weights=[0.25, 0.25, 0.5])[0]

def cycle_moves(observation, configuration):
    """Агент, циклически перебирающий все варианты"""
    return observation.step % configuration.signs

def anti_statistical(observation, configuration):
    """Агент, выбирающий ход, который бьет наиболее часто используемый противником ход"""
    if observation.step == 0:
        anti_statistical.action_histogram = {}
    action = observation.lastOpponentAction
    if action not in anti_statistical.action_histogram:
        anti_statistical.action_histogram[action] = 0
    anti_statistical.action_histogram[action] += 1
    mode_action = max(anti_statistical.action_histogram, key=anti_statistical.action_histogram.get)
    return (mode_action + 2) % configuration.signs

def mirror_last_two(observation, configuration):
    """Агент, который повторяет последний ход, если он победил, и меняет ход, если проиграл"""
    if observation.step == 0:
        mirror_last_two.last_action = random.randrange(0, configuration.signs)
        return mirror_last_two.last_action
    if get_score(mirror_last_two.last_action, observation.lastOpponentAction) > 0:
        return mirror_last_two.last_action
    mirror_last_two.last_action = (observation.lastOpponentAction + 1) % configuration.signs
    return mirror_last_two.last_action

def rotating_choice(observation, configuration):
    """Агент, который каждый ход выбирает новое действие циклически"""
    return (observation.step % configuration.signs)

def fixed_pattern(observation, configuration):
    """Агент с фиксированной последовательностью: Камень -> Бумага -> Ножницы"""
    pattern = [0, 1, 2]
    return pattern[observation.step % len(pattern)]

def beat_previous_move(observation, configuration):
    """Агент выбирает ход, который побьет предыдущий ход противника"""
    if observation.step == 0:
        return random.randrange(0, configuration.signs)
    return (observation.lastOpponentAction + 1) % configuration.signs

def lose_to_previous_move(observation, configuration):
    """Агент выбирает ход, который проиграет предыдущему ходу противника"""
    if observation.step == 0:
        return random.randrange(0, configuration.signs)
    return (observation.lastOpponentAction + 2) % configuration.signs

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
agents = {
    "rock": rock,
    "paper": paper,
    "scissors": scissors,
    "copy_opponent": copy_opponent,
    "copy_changing": copy_changing,
    "reactionary": reactionary,
    "counter_reactionary": counter_reactionary,
    "random_choice": random_choice,
    "favor_scissors": favor_scissors,
    "favor_paper": favor_paper,
    "favor_rock": favor_rock,
    "statistical": statistical,
    "random_favor_rock": random_favor_rock,
    "random_favor_paper": random_favor_paper,
    "random_favor_scissors": random_favor_scissors,
    "cycle_moves": cycle_moves,
    "anti_statistical": anti_statistical,
    "mirror_last_two": mirror_last_two,
    "rotating_choice": rotating_choice,
    "fixed_pattern": fixed_pattern,
    "beat_previous_move": beat_previous_move,
    "lose_to_previous_move": lose_to_previous_move
}
