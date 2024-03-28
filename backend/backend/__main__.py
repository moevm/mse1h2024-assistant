import argparse
import uvicorn
from backend.settings import config


def main():
    uvicorn.run(
        app='backend.main:app',
        host=config.host,
        port=config.port,
        workers=1,
    )


if __name__ == '__main__':
    main()
