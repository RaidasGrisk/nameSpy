import logging
import json


# this is optional: lets add structured message to logging record
# logging.info(StructuredMessage('message 1', foo='bar', bar='baz', num=123, fnum=123.456))
class StructuredMessage(object):
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return '%s >>> %s' % (self.message, self.kwargs)


# Store and access the logging records on a list
# instead of printing in stdout or saving in file.
# Later pipe them as part of the api output.
# To be able to do that, lets subclass logging.Handler
# https://docs.python.org/3/library/logging.handlers.html
class CustomHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.log = []

    def emit(self, record):
        self.log.append(self.string_to_dict(self.format(record)))

    # By default records are expected to be str.
    # I'd like records to be a dict.
    # Cannot simply configure logging.Formatter
    # as by default a record should stay str, otherwise
    # would have to overwrite methods in other classes to.
    # So, lets just convert str to dict on the last step.
    @staticmethod
    def string_to_dict(formatted_record):
        return json.loads(formatted_record)

    def clear_log(self):
        self.log = []


# init and set logger params
logger = logging.getLogger(__name__)  # __name__ is the module file name
handler = CustomHandler()
formatter = logging.Formatter(
    '{"time":"%(asctime)s", '
    # '"level": "%(levelname)s", '
    # '"name": "%(name)s", '
    '"message": "%(message)s"}'
)

logger.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)

# having this setup, log records can be created in any other module by either
# importing logging package or importing logger object defined in this module.
# Both of the following works:
#
# import logging
# logging.info('message')
# /
# from logger_config import logger
# logger.info('message')
# / also possible to do this
# import logging
# logger = logging.getLogger()
# logger.info('message')
# not sure which is the standard way:
# https://www.machinelearningplus.com/python/python-logging-guide/#:~:text=Create%20a%20new%20project%20directory,root%20logger's%20logging%20message!%E2%80%9D.
# https://stackoverflow.com/questions/37958568/how-to-implement-a-global-python-logger