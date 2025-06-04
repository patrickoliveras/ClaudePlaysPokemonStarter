from agent.emulator import Emulator


def test_can_move_between_tiles_blocked_and_allowed():
    e = Emulator.__new__(Emulator)
    # blocked pair from table
    assert not e._can_move_between_tiles(288, 261, "CAVERN")
    assert not e._can_move_between_tiles(261, 288, "CAVERN")
    # allowed pair not in table
    assert e._can_move_between_tiles(123, 456, "OVERWORLD")
