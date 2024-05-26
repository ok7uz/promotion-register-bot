from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError, ConfigurationError
from loguru import logger

from config import DB_NAME

TORTOISE_ORM = {
    "connections": {
        "default": f"sqlite://{DB_NAME}"
    },
    "apps": {
        "models": {
            "models": ["bot.models"],
            "default_connection": "default",
        },
    },
}

async def setup() -> None:
    """
    Set up the Tortoise ORM with the defined configuration.
    Initialize the database and generate schemas.

    Raises:
        DBConnectionError: If there is a problem with the database connection.
        ConfigurationError: If there is a problem with the Tortoise configuration.
    """
    try:
        logger.info("Initializing Tortoise ORM ...")
        await Tortoise.init(TORTOISE_ORM)
        logger.info("Generating database schemas ...")
        await Tortoise.generate_schemas()
        logger.info("Database setup completed successfully.")
    except (DBConnectionError, ConfigurationError) as e:
        logger.error(f"Error during database setup: {e}")
        raise

async def close() -> None:
    """
    Close the Tortoise ORM connection.
    """
    logger.info("Closing Tortoise ORM connection ...")
    await Tortoise.close_connections()
    logger.info("Tortoise ORM connection closed.")
