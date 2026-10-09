def main():
    counter = 0
    print("================================")
    print("      DPB&A CLI Assistant")
    print("================================")
    print("Type 'exit' to quit.\n")

    while True:
        counter += 1

        user_input = input(f"You [{counter}] : ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        elif user_input.lower() == "help":
            print("Available commands:\n")
            print("\thelp - Show this message")
            print("\texit - Exit the assistant")
            counter -= 1
            continue
        else:
            print(f"You said: {user_input}")


if __name__ == "__main__":
    main()
