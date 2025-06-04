import pytest
import numpy as np

from agent.memory_reader import (
    PokemonRedReader,
    StatusCondition,
    PokemonData,
    Badge,
)


def make_reader():
    mem = bytearray(0x10000)
    return PokemonRedReader(mem), mem


def test_read_money():
    reader, mem = make_reader()
    mem[0xD349] = 0x45
    mem[0xD348] = 0x23
    mem[0xD347] = 0x01
    assert reader.read_money() == 12345


def test_convert_text_and_names():
    reader, mem = make_reader()
    # Set player and rival names to "AB"
    mem[0xD158:0xD163] = bytes([0x80, 0x81, 0x50, 0x50, 0x50])
    mem[0xD34A:0xD351] = bytes([0x80, 0x81, 0x50, 0x50, 0x50, 0x50, 0x50])
    assert reader.read_player_name() == "AB"
    assert reader.read_rival_name() == "AB"


def test_read_badges():
    reader, mem = make_reader()
    mem[0xD356] = 0xFF
    assert reader.read_badges() == [
        "BOULDER",
        "CASCADE",
        "THUNDER",
        "RAINBOW",
        "SOUL",
        "MARSH",
        "VOLCANO",
        "EARTH",
    ]


def test_item_reading():
    reader, mem = make_reader()
    mem[0xD31D] = 2
    mem[0xD31E] = 0x04
    mem[0xD31F] = 3
    mem[0xD320] = 0x0B
    mem[0xD321] = 1
    assert reader.read_items() == [("POKé BALL", 3), ("ANTIDOTE", 1)]


def test_pokedex_caught_count():
    reader, mem = make_reader()
    mem[0xD2F7] = 0b10101010
    mem[0xD2F8] = 0b11110000
    assert reader.read_pokedex_caught_count() == 8


def test_pokemondata_status_properties():
    pd = PokemonData(
        species_id=1,
        species_name="RHIDON",
        current_hp=10,
        max_hp=20,
        level=5,
        status=StatusCondition.SLEEP | StatusCondition.POISON,
        type1=0,
        type2=None,
        moves=[],
        move_pp=[],
        trainer_id=0,
        nickname="TEST",
        experience=0,
    )
    assert pd.is_asleep
    assert pd.status_name == "SLEEP"

