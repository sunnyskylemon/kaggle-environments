from kaggle_environments import make
from .agents import random_agent, rock, paper, agents

def negative_move_agent(observation, configuration):
    return -1


def too_big_weapon_agent(observation, configuration):
    return 1000000


def non_integer_agent(observation, configuration):
    return 0.3


def none_agent(observation, configuration):
    return None


def test_rps_completes():
    env = make("rps", configuration={"episodeSteps": 10})
    env.run([random_agent, random_agent])
    json = env.toJSON()
    assert json["name"] == "rps"
    assert json["statuses"] == ["DONE", "DONE"]


def test_all_agents():
    env = make("rps", configuration={"episodeSteps": 3})
    for agent in agents:
        env.run([agent, agent])
        json = env.toJSON()
        assert json["statuses"] == ["DONE", "DONE"]


def test_tie():
    env = make("rps", configuration={"episodeSteps": 3})
    env.run([rock, rock])
    assert env.render(mode='ansi') == "Round 1: Rock vs Rock, Score: 0.5 to 0.5\nRound 2: Rock vs Rock, Score: 0.5 to 0.5\nGame ended on round 2, final score: 1.0 to 1.0\n"
    json = env.toJSON()
    assert json["rewards"] == [0.5, 0.5]
    assert json["statuses"] == ["DONE", "DONE"]


def test_win():
    env = make("rps", configuration={"episodeSteps": 10})
    env.run([paper, rock])
    json = env.toJSON()
    print(json)
    assert json["rewards"] == [1, 0]
    assert json["statuses"] == ["DONE", "DONE"]


def test_loss():
    env = make("rps", configuration={"episodeSteps": 10})
    env.run([rock, paper])
    json = env.toJSON()
    assert json["rewards"] == [0, 1]
    assert json["statuses"] == ["DONE", "DONE"]


def test_negative_move():
    env = make("rps", configuration={"episodeSteps": 10})
    env.run([negative_move_agent, rock])
    json = env.toJSON()
    assert json["rewards"] == [None, 1]
    assert json["statuses"] == ['INVALID', 'DONE']


def test_non_integer_move():
    env = make("rps", configuration={"episodeSteps": 10})
    env.run([non_integer_agent, rock])
    json = env.toJSON()
    assert json["rewards"] == [None, 1]
    assert json["statuses"] == ['INVALID', 'DONE']


def test_too_big_move():
    env = make("rps", configuration={"episodeSteps": 10})
    env.run([paper, too_big_weapon_agent])
    json = env.toJSON()
    assert json["rewards"] == [1, None]
    assert json["statuses"] == ['DONE', 'INVALID']