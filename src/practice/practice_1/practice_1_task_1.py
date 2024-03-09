from class_module import *

COMMAND_EXPLANATION = ("\nEnter command (AddToStart, AddToEnd, ChangeIndex, AddValue) and args with space.\n"
                       "Enter 'Undo' to cancel action.\n"
                       "To exit enter 'q'.\n"
                       "To see Object List enter 'List'.\n"
                       "for example: 'ChangeIndex 2 3': "
                       )


def parse_command(storage: PerformedCommandStorage, command: str) -> PerformedCommandStorage:
    split_command = command.split()

    command_name, arguments = split_command.pop(0), split_command[0:]
    arguments = list(map(int, arguments))
    if command_name == "Undo":
        storage.undo()
    elif command_name == "List":
        print(storage.get_storage())
    elif command_name == "AddToStart":
        storage.apply(AddToStart(*arguments))
    elif command_name == "AddToEnd":
        storage.apply(AddToEnd(*arguments))
    elif command_name == "ChangeIndex":
        storage.apply(ChangeIndex(*arguments))
    elif command_name == "AddValue":
        storage.apply(AddValue(*arguments))
    else:
        print("Incorrect command")

    return storage


def main():
    object_list_str = input("Enter list (for example: 1 2 3): ")
    try:
        object_list = list(map(int, object_list_str.split()))
    except Exception:
        raise ValueError("Incorrect list input")

    storage = PerformedCommandStorage(object_list)
    print(COMMAND_EXPLANATION)

    while True:
        command = input()

        if command == "q":
            break

        storage = parse_command(storage, command)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)
