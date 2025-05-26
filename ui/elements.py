from typing import Callable

def title(text: str):
    print(f"\n=== {text} ===")

def input_field(prompt: str = "") -> str:
    print()
    if prompt:
        print(prompt)
    return input("> ")

def divider():
    print("-" * 40)

def menu_option(key: str, label: str):
    print(f"{key}. {label}")

def render_menu(menu_data: list[tuple[str, str | None, Callable]], left_padding="  ") -> dict[str, Callable]:
    actions = {}
    auto_index = 1

    for label, key, action in menu_data:
        if key is None:
            key = str(auto_index)
            auto_index += 1
        actions[key] = action
        print(f"{left_padding}{key}. {label}")

    return actions