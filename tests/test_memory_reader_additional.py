import numpy as np
from agent.memory_reader import PokemonRedReader, PokemonType, Pokemon, Move
from agent.memory_reader import StatusCondition


def make_reader():
    mem = bytearray(0x10000)
    return PokemonRedReader(mem), mem


def test_convert_text_numbers_and_punctuation():
    reader, mem = make_reader()
    data = [0xF6, 0xF7, 0x9A, 0x9B, 0x4E, 0x50]
    assert reader._convert_text(data) == "01()"


def test_read_coordinates_and_location_tileset():
    reader, mem = make_reader()
    mem[0xD362] = 5
    mem[0xD361] = 7
    mem[0xD35E] = 0x00  # PALLET_TOWN
    mem[0xD367] = 0x00  # OVERWORLD
    assert reader.read_coordinates() == (5, 7)
    assert reader.read_location() == "PALLET TOWN"
    assert reader.read_tileset() == "OVERWORLD"


def test_read_game_time_and_coins():
    reader, mem = make_reader()
    mem[0xDA40] = 0
    mem[0xDA41] = 2
    mem[0xDA42] = 30
    mem[0xDA44] = 15
    mem[0xD5A4] = 0x01
    mem[0xD5A5] = 0x02
    assert reader.read_game_time() == (2, 30, 15)
    assert reader.read_coins() == 258


def test_read_party_pokemon_single():
    reader, mem = make_reader()
    mem[0xD163] = 1  # party size
    base = 0xD16B
    mem[base] = Pokemon.RHYDON
    mem[base + 1] = 0
    mem[base + 2] = 50
    mem[base + 0x22] = 0
    mem[base + 0x23] = 60
    mem[base + 0x21] = 5
    mem[base + 4] = int(StatusCondition.NONE)
    mem[base + 5] = PokemonType.ROCK
    mem[base + 6] = PokemonType.GROUND
    mem[base + 8] = Move.TACKLE
    mem[base + 0x1D] = 35
    mem[base + 12] = 0x12
    mem[base + 13] = 0x34
    mem[base + 0x1A] = 0
    mem[base + 0x1B] = 0
    mem[base + 0x1C] = 10
    mem[0xD2B5:0xD2B5+11] = bytes([0x80, 0x81, 0x50] + [0x50]*8)

    party = reader.read_party_pokemon()
    assert len(party) == 1
    p = party[0]
    assert p.species_name == "RHYDON"
    assert p.current_hp == 50
    assert p.max_hp == 60
    assert p.level == 5
    assert p.type1.name == "ROCK"
    assert p.type2.name == "GROUND"
    assert p.moves == ["TACKLE"]
    assert p.move_pp == [35]
    assert p.nickname == "AB"
    assert p.experience == 10
