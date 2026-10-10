import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def ask_ollama(messages):
    url = "http://localhost:11434/api/chat"

    data = {
        "model": "llama3.2:latest",
        "messages": messages,
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

        answer = result["message"]["content"]
        return answer, None

    except HTTPError as error:
        return None, f"Ollama HTTP error: {error.code}"

    except URLError as error:
        return None, f"Could not connect to Ollama: {error.reason}"

    except TimeoutError:
        return None, "Ollama timed out. Please try again."

    except (KeyError, TypeError, json.JSONDecodeError):
        return None, "Could not understand Ollama's response."


def main():
    counter = 0

    messages = [
        {
            "role": "system",
            "content": (
                "You are the DPB&A AI Assistant, a helpful technical "
                "assistant specializing in Python, Java enterprise "
                "software, and AI development. Explain concepts clearly "
                "and tailor explanations to the user's apparent skill "
                "level. Prioritize technical accuracy over sounding "
                "confident. Do not invent facts. When a claim depends "
                "on context, explain the relevant conditions. If you "
                "are uncertain, say so. When comparing technologies, "
                "avoid sweeping claims and distinguish general tendencies "
                "from workload-dependent results. Provide runnable code "
                "examples when useful."
            ),
        }
    ]

    print("================================")
    print("      DPB&A CLI Assistant")
    print("================================")
    print("Powered by Ollama and Llama 3.2")
    print("Type 'help' for commands or 'exit' to quit.\n")

    while True:
        try:
            user_input = input(f"You [{counter + 1}] : ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

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

        messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        print("\nAI: ", end="", flush=True)

        answer, error = ask_ollama(messages)

        if error:
            print(f"\nError: {error}\n")
            messages.pop()
            continue

        print(answer, "\n")

        messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )


if __name__ == "__main__":
    main()
