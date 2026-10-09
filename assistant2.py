import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def ask_ollama(question):
    url = "http://localhost:11434/api/chat"

    data = {
        "model": "llama3.2:latest",
        "messages": [{"role": "user", "content": question}],
        "stream": False,
    }

    request = Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        return result["message"]["content"]

    except HTTPError as error:
        return f"Ollama HTTP error: {error.code}"

    except URLError as error:
        return f"Could not connect to Ollama: {error.reason}"

    except (KeyError, json.JSONDecodeError):
        return "Could not understand Ollama's response."


def main():
    counter = 0

    print("================================")
    print("      DPB&A CLI Assistant")
    print("================================")
    print("Powered by Ollama and Llama 3.2")
    print("Type 'help' for commands or 'exit' to quit.\n")

    while True:
        user_input = input(f"You [{counter + 1}] : ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        elif user_input.lower() == "help":
            print("\nAvailable commands:")
            print("\thelp - Show this message")
            print("\texit - Exit the assistant\n")
            continue

        elif not user_input:
            continue

        counter += 1

        print("\nAI: ", end="", flush=True)
        answer = ask_ollama(user_input)
        print(answer, "\n")


if __name__ == "__main__":
    main()
