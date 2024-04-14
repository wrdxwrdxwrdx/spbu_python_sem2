from inspect import getfullargspec

from src.homeworks.homework_1.homework_1_task_1 import Registry
from src.homeworks.homework_2.storage import *

COMMAND_EXPLANATION = (
    "\nEnter command (AddToStart, AddToEnd, ChangeIndex, AddValue, ...) and args with space.\n"
    "Enter 'Undo' to cancel action.\n"
    "To exit enter 'q'.\n"
    "To see Object Collection enter 'Collection'.\n"
    "To see Full Command List enter 'AllCommands'.\n"
    "To see Available Command List enter 'Commands'.\n"
    "for example: 'ChangeIndex 2 3': \n"
)


def create_action_registry() -> Registry[Action]:
    registry = Registry[Action]()

    for sub_cls in Action.__subclasses__():
        registry.register(sub_cls.__name__)(sub_cls)

    return registry


def create_storage() -> PerformedCommandStorage[Action]:
    collection_type = input("type: ")

    try:
        object_list = input("Enter storage of int`s (for example: 1 2 3): ")
        collection = eval(f"{collection_type}(map(int, object_list.split()))")
    except NameError:
        raise IncorrectCollectionError(collection_type)
    except ValueError:
        raise ValueError("Expected int, got str")
    return PerformedCommandStorage[Action](collection)


def get_command_args(command_line: str) -> tuple[str, list[int]]:
    try:
        command, args = command_line.split()[0], list(
            map(int, command_line.split()[1:] if len(command_line) > 0 else [])
        )
        return command, args
    except ValueError:
        raise ValueError("Expected int argument, got str")


def main() -> None:
    action_registry = create_action_registry()
    all_commands = list(action_registry.classes.keys())
    storage = create_storage()

    all_commands_annotation = []
    available_commands_annotation = []
    for command in all_commands:
        action = action_registry.dispatch(command)
        if isinstance(storage.collection, action.object_collection_type):
            available_commands_annotation.append(command + " " + "  ".join(getfullargspec(action.__init__).args[1:]))
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
            elif command_line == "AllCommands":
                print("\n".join(all_commands_annotation))
            elif command_line == "Commands":
                print(
                    "\n".join(available_commands_annotation)
                    if available_commands_annotation
                    else "No available commands"
                )
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
