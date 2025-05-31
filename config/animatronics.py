from ui.sprites.screamers.bonnie import BONNIE_SCREAMER_FRAMES
from ui.sprites.screamers.foxy import FOXY_SCREAMER_FRAMES
from ui.sprites.screamers.chica import CHICA_SCREAMER_FRAMES
from ui.sprites.screamers.freddy import FREDDY_SCREAMER_FRAMES

ANIMATRONICS = {
    "Bonnie": {
        "default_position_index": 1,
        "path_graph": {
            1: [2],
            2: [3, 6],
            3: [2, 6],
            6: [7, 8, 13],
            7: [8, 13],
            13: [8],
            8: [11]
        },
        "attack_trigger": {
            "type": "position",
            "position": 8
        },
        "screamer_sprites": BONNIE_SCREAMER_FRAMES
    },
    "Chica": {
        "default_position_index": 1,
        "path_graph": {
            1: [2],
            2: [4, 9, 5],
            4: [2, 9],
            5: [2, 9],
            9: [10, 14],
            14: [10],
            10: [11]
        },
        "attack_trigger": {
            "type": "position",
            "position": 10
        },
        "screamer_sprites": CHICA_SCREAMER_FRAMES
    },
    "Freddy": {
        "default_position_index": 1,
        "path_graph": {
            1: [2],
            2: [4],
            4: [9],
            9: [14],
            14: [11]
        },
        "attack_trigger": {
            "type": "laugh",
            "number": 3,
            "position": 10
        },
        "screamer_sprites": FREDDY_SCREAMER_FRAMES
    },
    "Foxy": {
        "default_position_index": 12,
        "path_graph": {
            12: [11],
        },
        "attack_trigger": {
            "type": "run",
            "attack_pose": 4,
            "position": 8,
            "power_cost": 5,
        },
        "screamer_sprites": FOXY_SCREAMER_FRAMES
    }
}