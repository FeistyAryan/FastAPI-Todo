# in app/core/logging_config.py
import sys
import logging
import structlog

def setup_logging():
    shared_processors = [
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(),
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Get the root logger
    root_logger = logging.getLogger()
    # Wipe out any existing handlers
    root_logger.handlers = []
    # Add our own handler
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    # --- THIS IS THE CLEANUP ---
    # Silence Gunicorn's default loggers
    for name in ["gunicorn.error", "gunicorn.access"]:
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Silence Uvicorn's default loggers
    for name in ["uvicorn.error", "uvicorn.access"]:
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = False # Do not let them bubble up to root

    # Set SQLAlchemy's logger to WARNING to hide INFO-level queries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)