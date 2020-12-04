import random

import adventurelib

from cronenbroguelike import commands
from cronenbroguelike import rooms
from engine import actor
from engine import ai
from engine import directions
from engine.globals import G
from engine import say


def _create_rooms(number_of_rooms):
    return random.sample(rooms.all_rooms(), number_of_rooms)


def _get_random_start():
    # TODO: Condition this on how the last death actually occurred.
    cause_of_death = random.choice(
        [
            "being impaled",
            "slowly suffocating as a glabrous tentacle horror looks on",
        ]
    )
    for text in [
        f"The memory of {cause_of_death} fades away.",
        "You know only that you have been here for interminable years, "
        "that you have died innumerable times, and that someone once told "
        "you there was a way out. You were told this an eon ago, or maybe "
        "a day, but the stubborn hope of escape glisters in your mind.",
    ]:
        say.insayne(text)


def _start_game(_):

    # Creates the player character and ensures game will restart upon death.
    G.player = actor.create_actor(
        health=10,
        psyche=10,
        strength=10,
        stamina=10,
        will=10,
        wisdom=10,
        insanity=0,
        name="player",
    )
    G.player.log_stats = True
    G.player.upon_death(_start_game)

    # Creates a small dungeon.
    G.current_room, room_2, room_3 = _create_rooms(3)
    possible_exits = [
        directions.north,
        directions.south,
        directions.east,
        directions.west,
    ]
    exit_1 = random.choice(possible_exits)
    room_2.add_exit(exit_1, G.current_room)
    room_2.add_exit(random.choice(list(set(possible_exits) - set([exit_1]))), room_3)

    # Places a monster in a random room.
    fish_man = monsters.fish_man()
    random.choice([G.current_room, room_2, room_3]).add_character(fish_man)

    # Starts it up.
    _get_random_start()
    commands.enter_room(G.current_room)


_start_game(None)
G.player.upon_death(_start_game)
adventurelib.say("")  # Necessary for space before first prompt.
adventurelib.start()
