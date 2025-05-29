from ui.sprites.screamers import BONNIE_SCREAMER_DARK, CHICA_SCREAMER_DARK, FREADDY_SCREAMER_DARK, FOXY_SCREAMER_DARK

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
        "screamer_sprite": BONNIE_SCREAMER_DARK
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
        "screamer_sprite": CHICA_SCREAMER_DARK
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
        "screamer_sprite": FREADDY_SCREAMER_DARK
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
        "screamer_sprite": FOXY_SCREAMER_DARK
    }
}