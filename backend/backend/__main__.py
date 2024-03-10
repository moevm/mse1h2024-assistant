import uvicorn
from backend.settings import config


def _run_uvicorn():
    uvicorn.run(
        app='backend.main:app',
        host=config.host,
        port=config.port,
        workers=1,
    )


def main():
    _run_uvicorn()


if __name__ == '__main__':
    main()
