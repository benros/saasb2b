import logging
from logging.handlers import TimedRotatingFileHandler
from niyud.utils.db_log_handler import SQLAlchemyHandler
from pathlib import Path


DEFAULT_LOGGER_NAME = "niyud"
DEFAULT_LOG_LEVEL = logging.DEBUG
DEFAULT_HUMAN_LOG_FORMAT = ("%(process)d - %(asctime)s - %(levelname)s - "
                            "%(name)s - {module_name} - %(funcName)s - "
                            "line %(lineno)d - %(message)s")


def get_logger(logger_name=DEFAULT_LOGGER_NAME, log_level=DEFAULT_LOG_LEVEL,
               enable_machine_log=False, enable_human_log=True,
               enable_stream_log=True, ignore_log_failures=False,
               machine_log_file_path=None, human_log_file_path=None,
               enable_rotation=False, enable_db_log=True,
               human_log_format=DEFAULT_HUMAN_LOG_FORMAT, db_conn=None,
               db_log_schema_name=None, module_name=None):

    # IMPORTANT NOTE:
    # depending on environment settings, log failure may be silently ignored.
    # typically, this is done when log failure should not fail the
    # parent process
    try:

        lgr = logging.getLogger(logger_name)
        # adding logger handlers only if no handlers exist.
        # the logger object acts as a singleton by nature,
        # but handlers may be unintentionally duplicated
        if not len(lgr.handlers):
            lgr.setLevel(int(log_level))

            # add stream handler if enabled
            if str(enable_stream_log).lower() == "true":
                stream_handler = logging.StreamHandler()
                format_ = human_log_format.format(module_name=module_name)
                stream_handler.setFormatter(
                    logging.Formatter(format_))
                lgr.addHandler(stream_handler)

            # add human readable log file handler
            if str(enable_human_log).lower() == "true":
                # Creating the logs folder, if not already exists
                files_folder = Path(human_log_file_path).parent
                if not Path.exists(files_folder):
                    Path.mkdir(files_folder)

                if str(enable_rotation).lower() == "true":
                    # D - for days, 7- after 7 files will delete the oldest one
                    file_handler = \
                        TimedRotatingFileHandler(human_log_file_path,
                                                 when="MIDNIGHT",
                                                 backupCount=7,
                                                 encoding="iso-8859-8")
                    format_ = human_log_format.format(module_name=module_name)
                    file_handler.setFormatter(logging.Formatter(format_))
                    lgr.addHandler(file_handler)
                else:
                    file_handler = \
                        logging.FileHandler(human_log_file_path,
                                            encoding="iso-8859-8")
                    format_ = human_log_format.format(module_name=module_name)
                    file_handler.setFormatter(
                        logging.Formatter(format_))
                    lgr.addHandler(file_handler)

            # add LogStash handler
            if str(enable_machine_log).lower() == "true":
                from logstash_formatter import LogstashFormatter
                file_handler = logging.FileHandler(machine_log_file_path)
                file_handler.setFormatter(LogstashFormatter())
                lgr.addHandler(file_handler)

            # add DB handler
            if str(enable_db_log).lower() == "true":
                db_handler = SQLAlchemyHandler(
                    module_name=module_name,
                    db_conn=db_conn,
                    schema_name=db_log_schema_name,
                    ignore_log_failures=ignore_log_failures)
                format_ = human_log_format.format(module_name=module_name)
                db_handler.setFormatter(logging.Formatter(format_))
                lgr.addHandler(db_handler)

        return lgr

    except Exception:
        if str(ignore_log_failures).lower() == "true":
            pass
        else:
            raise
