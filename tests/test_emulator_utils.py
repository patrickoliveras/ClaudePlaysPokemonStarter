import numpy as np
from agent.emulator import Emulator


def test_downsample_array():
    e = Emulator.__new__(Emulator)  # bypass __init__
    arr = np.arange(18*20).reshape(18,20)
    down = e._downsample_array(arr)
    assert down.shape == (9,10)
    # first block average of arr[0:2,0:2]
    assert down[0,0] == np.mean(arr[0:2,0:2])


def test_get_direction_patterns():
    e = Emulator.__new__(Emulator)
    arr = np.zeros((4,4), dtype=int)
    arr[0:2,0:2] = [[0,1],[2,3]]
    assert e._get_direction(arr) == "down"
    arr[0:2,0:2] = [[4,5],[6,7]]
    assert e._get_direction(arr) == "up"
    arr[0:2,0:2] = [[9,8],[11,10]]
    assert e._get_direction(arr) == "right"
    arr[0:2,0:2] = [[8,9],[10,11]]
    assert e._get_direction(arr) == "left"
    arr[0:2,0:2] = [[99,99],[99,99]]
    assert e._get_direction(arr) == "no direction found"
