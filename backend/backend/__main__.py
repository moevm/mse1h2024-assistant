import uvicorn

HOST = '0.0.0.0'
PORT = 5000


def _run_uvicorn():
    uvicorn.run(
        app='backend.main:app',
        host=HOST,
        port=PORT,
        workers=1,
    )


def main():
    _run_uvicorn()


if __name__ == '__main__':
    main()
