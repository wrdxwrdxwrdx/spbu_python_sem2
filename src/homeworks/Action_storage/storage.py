from inspect import getfullargspec

from src.homeworks.Action_storage.storage_class import *

COMMAND_EXPLANATION = (
    "\nEnter command (AddToStart, AddToEnd, ChangeIndex, AddValue, ...) and args with space.\n"
    "Enter 'Undo' to cancel action.\n"
    "To exit enter 'q'.\n"
    "To see Object Collection enter 'Collection'.\n"
    "To see Full Command List enter 'Commands'.\n"
    "for example: 'ChangeIndex 2 3': \n"
)


def create_storage() -> PerformedCommandStorage:
    try:
        object_list = input("Enter storage of int`s (for example: 1 2 3): ")
        collection = list(map(int, object_list.split()))
    except ValueError:
        raise ValueError("Expected int, got str")
    return PerformedCommandStorage(collection)


def get_command_args(command_line: str) -> tuple[str, list[int]]:
    try:
        command, args = command_line.split()[0], list(
            map(int, command_line.split()[1:] if len(command_line) > 0 else [])
        )
        return command, args
    except ValueError:
        raise ValueError("Expected int argument, got str")


def main() -> None:
    action_registry = registry
    all_commands = list(action_registry.classes.keys())
    storage = create_storage()

    all_commands_annotation = []
    for command in all_commands:
        action = action_registry.dispatch(command)
        all_commands_annotation.append(command + " " + "  ".join(getfullargspec(action.__init__).args[1:]))

    print(COMMAND_EXPLANATION)

    while True:
        try:
            command_line = input(">>")
            command, args = get_command_args(command_line)

            if command_line == "q":
                break
            elif command_line == "Undo":
                storage.undo()
            elif command_line == "Collection":
                print(storage.collection)
            elif command_line == "Commands":
                print("\n".join(all_commands_annotation))
            elif command in all_commands:
                action = action_registry.dispatch(command)
                storage.apply(action(*args))
            else:
                raise IncorrectActionError(command)
        except Exception as error:
            print(error)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
