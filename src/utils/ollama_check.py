import subprocess

def is_ollama_installed() -> bool:
    try:
        subprocess.run(
            ["ollama", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except Exception:
        return False


def is_ollama_running() -> bool:
    try:
        subprocess.run(
            ["ollama", "list"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except Exception:
        return False


def is_model_available(model_name: str) -> bool:
    try:
        out = subprocess.check_output(["ollama", "list"]).decode()
        return model_name in out
    except Exception:
        return False
