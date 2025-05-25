ANIMATRONICS = {
    "Bonnie": {
        "default_possition_index": 1,
        "path_graph": {
            1: [2],
            2: [3, 6],
            3: [2, 6],
            6: [7, 8],
            7: [8],
            8: []
        },
        "attack_trigger": {
            "type": "position",
            "position": 8
        }
    },
    "Chica": {
        "default_possition_index": 1,
        "path_graph": {
            1: [2],
            2: [9, 5],
            5: [2, 9],
            9: [10],
            10: []
        },
        "attack_trigger": {
            "type": "position",
            "position": 10
        }
    }
}