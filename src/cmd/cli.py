from src.config.settings import Settings
from src.entrypoints.cli.commands import cli
from src.shared.logging.logger import setup_logger

if __name__ == "__main__":
    settings = Settings()
    setup_logger(settings.log)

    cli(obj={"settings": settings})
