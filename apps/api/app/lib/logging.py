import sys
from datetime import UTC, datetime
from functools import partial
from logging import StreamHandler

import structlog
from granian.log import DEFAULT_ACCESSLOG_FMT
from litestar.logging import LoggingConfig, StructLoggingConfig
from rich.console import Console
from rich.default_styles import DEFAULT_STYLES
from structlog.dev import (
    Column,
    ConsoleRenderer,
    KeyValueColumnFormatter,
    RichTracebackFormatter,
)
from structlog.stdlib import ProcessorFormatter
from structlog.typing import EventDict, Processor, WrappedLogger

from app.settings.logging import LoggingSettings

SHARED_PROCESSORS: tuple[Processor, ...] = (
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
)


def _format_console_event(
    _: WrappedLogger, __: str, event: EventDict, *, colors: bool
) -> EventDict:
    timestamp = datetime.now(UTC).time().isoformat(timespec="milliseconds")
    event["timestamp"] = f"{timestamp} UTC"

    level = event["level"]
    label = level.upper()
    style = DEFAULT_STYLES.get(f"logging.level.{level}") if colors else None
    event["level"] = (style.render(label) if style else label) + " " * (8 - len(label))

    if not event["_from_structlog"]:
        record = event["_record"]
        arguments = event.pop("positional_args")

        if record.name == "granian.access" and record.msg == DEFAULT_ACCESSLOG_FMT:
            event["event"] = "{method} {path}  {status}  {dt_ms:.1f}ms".format_map(arguments)

    return event


def _create_console_renderer() -> ConsoleRenderer:
    renderer = ConsoleRenderer(
        colors=False,
        pad_event_to=0,
        sort_keys=False,
        exception_formatter=RichTracebackFormatter(
            show_locals=False,
            color_system=None,
        ),
    )
    columns = {column.key: column for column in renderer.columns}
    text_column = partial(
        KeyValueColumnFormatter,
        key_style=None,
        value_style="",
        reset_style="",
        value_repr=str,
    )
    renderer.columns = [
        columns["timestamp"],
        Column("level", text_column()),
        Column("logger", text_column(width=24)),
        columns["event"],
        columns[""],
    ]

    return renderer


def create_log_handler(settings: LoggingSettings) -> StreamHandler:
    """Build the stream handler used by the application and server processes."""
    render_processors: list[Processor]

    if settings.format == "json":
        render_processors = [
            ProcessorFormatter.remove_processors_meta,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    else:
        terminal = Console(file=sys.stderr)
        colors = (
            sys.stdout.isatty()
            and sys.stderr.isatty()
            and terminal.color_system not in {None, "windows"}
            and not terminal.no_color
        )
        render_processors = [
            partial(_format_console_event, colors=colors),
            ProcessorFormatter.remove_processors_meta,
            _create_console_renderer(),
        ]

    handler = StreamHandler()
    handler.setLevel(settings.level)
    handler.setFormatter(
        ProcessorFormatter(
            foreign_pre_chain=SHARED_PROCESSORS,
            processors=render_processors,
            pass_foreign_args=settings.format == "console",
        ),
    )

    return handler


def create_logging_config(
    settings: LoggingSettings,
    *,
    logger_names: tuple[str, ...] = (),
) -> StructLoggingConfig:
    """Build the logging configuration for an API or worker process."""
    standard_logging = LoggingConfig(
        logging_module="logging",
        root={"level": settings.level, "handlers": ["console"]},
        handlers={"console": {"()": create_log_handler, "settings": settings}},
        loggers={
            name: {
                "level": "NOTSET",
                "handlers": [],
                "propagate": True,
            }
            for name in logger_names
        },
    )

    return StructLoggingConfig(
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        processors=[
            structlog.stdlib.filter_by_level,
            *SHARED_PROCESSORS,
            ProcessorFormatter.wrap_for_formatter,
        ],
        standard_lib_logging_config=standard_logging,
        log_exceptions="always",
    )
