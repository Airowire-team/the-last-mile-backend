if __name__ == "__main__":
    import sys
    from pathlib import Path

    import uvicorn

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)
