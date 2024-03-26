import argparse
import uvicorn
from backend.settings import config_func, Config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config')
    args = parser.parse_args()
    config: Config = config_func(args.config)
    uvicorn.run(
        app='backend.main:app',
        host=config.host,
        port=config.port,
        workers=1,
    )


if __name__ == '__main__':
    main()
