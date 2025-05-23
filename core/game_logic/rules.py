from core.game_logic.game_state import GameState

def check_game_over(state: GameState) -> bool:
    for name, pos in state.animatronic_positions.items():
        if pos == "door" and not state.doors["left"]:
            state.is_alive = False
            return True
    return False