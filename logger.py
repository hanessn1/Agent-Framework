import logging
from config import LOG_LEVEL

TRACE_LEVEL_NUM = 5
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")


def trace(self, message, *args, **kws):
	if self.isEnabledFor(TRACE_LEVEL_NUM):
		self._log(TRACE_LEVEL_NUM, message, args, **kws)


logging.Logger.trace = trace


def setup_logging(level=LOG_LEVEL, log_filename="agent.log"):
	"""Sets up logging to write ONLY to agent.log."""
	fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
	date_fmt = "%Y-%m-%d %H:%M:%S"

	# writes directly to agent.log without printing to console
	file_handler = logging.FileHandler(log_filename, mode="w", encoding="utf-8")
	file_handler.setFormatter(logging.Formatter(fmt, datefmt=date_fmt))

	# pre-existing default handlers are overwritten
	logging.basicConfig(level=level, handlers=[file_handler], force=True)

	# Mute 3rd-party library loggers
	third_party_loggers = [
		"httpx",
		"httpcore",
		"openai",
		"urllib3",
		"fastapi",
		"uvicorn",
		"asyncio",
	]
	for logger_name in third_party_loggers:
		logging.getLogger(logger_name).setLevel(logging.WARNING)
