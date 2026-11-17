if __name__ == "__main__":
    import sys
    from pathlib import Path

    from dotenv import load_dotenv
    import uvicorn

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    load_dotenv(Path(__file__).resolve().parent / ".env")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)
