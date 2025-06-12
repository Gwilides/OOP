from virtual_keyboard import Keyboard
from memento import KeyboardStateSaver
from commands.print import PrintCharCommand
from commands.volume import VolumeUpCommand, VolumeDownCommand
from commands.media import MediaPlayerCommand


def main() -> None:
    keyboard = Keyboard()
    state_saver = KeyboardStateSaver()

    keyboard.key_bind("ctrl++", VolumeUpCommand(keyboard._output_service))
    keyboard.key_bind("ctrl+-", VolumeDownCommand(keyboard._output_service))
    keyboard.key_bind("ctrl+p", MediaPlayerCommand(keyboard._output_service))
    for char in "abcdefghijklmnopqrstuvwxyz ":
        keyboard.key_bind(char, PrintCharCommand(
            char, keyboard._output_service))

    saved_bindings = state_saver.load_state()
    if saved_bindings:
        keyboard.restore_bindings(saved_bindings)

    try:
        while True:
            key = input("Введите команду: ").strip()

            if key == "exit":
                break
            elif key == "undo":
                keyboard.undo()
            elif key == "redo":
                keyboard.redo()
            elif key == "save":
                state_saver.save_state(keyboard)
            elif key == "load":
                saved_bindings = state_saver.load_state()
                if saved_bindings:
                    keyboard.restore_bindings(saved_bindings)
            else:
                keyboard.press_key(key)

    except KeyboardInterrupt:
        print("\nВыход")
    finally:
        state_saver.save_state(keyboard)


if __name__ == "__main__":
    main()
