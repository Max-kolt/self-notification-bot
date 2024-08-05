from loguru import logger


class Unregistered(Exception):
    """
    Raised when user not registered
    """

    def __init__(self, telegram_id: int, message=lambda t_id: f"User {t_id} not registered"):
        super().__init__(message(telegram_id))
        logger.info(f"User with ID {telegram_id} not authorized")

