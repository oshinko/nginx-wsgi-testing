import logging
import logging.handlers
import os
import pathlib
import sys
import wsgiref.simple_server

FULL_LOG_FORMAT = ('%(asctime)s %(levelname)s %(filename)s %(name)s '
                   '%(funcName)s %(message)s')

SIMPLE_LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s %(message)s'

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(SIMPLE_LOG_FORMAT)

default = logging.StreamHandler(sys.stdout)
default.setFormatter(formatter)
default.setLevel(logging.DEBUG)
logger.addHandler(default)

log_file = os.environ.get('APP_LOG_FILE')

if log_file:
    log_file = pathlib.Path(log_file)
    log_file.parent.mkdir(exist_ok=True)
    info = logging.handlers.RotatingFileHandler(
        log_file,
        backupCount=int(os.environ.get('APP_LOG_FILE_BACKUP_COUNT', 4)),
        encoding=os.environ.get('APP_LOG_FILE_ENCODING', 'utf8'),
        maxBytes=int(os.environ.get('APP_LOG_FILE_MAX_BYTES', 1024 * 1024))
    )
    info.setFormatter(formatter)
    info.setLevel(logging.INFO)
    logger.addHandler(info)


def app(environ, start_response):
    logger.warning('Warning message')
    logger.info('Info message')
    logger.debug('Debug message')
    path = environ['PATH_INFO']
    if path == '/404':
        logger.error('The resource was not found.')
        status = '404 Not Found'
    elif path == '/500':
        raise Exception(path)
    else:
        status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    yield b'Hello!'


if __name__ == '__main__':
    class Handler(wsgiref.simple_server.WSGIRequestHandler):
        def log_message(self, format, *args):
            logger.info(f'{self.client_address[0]} {format % args}')

    server = wsgiref.simple_server.make_server('', 8000, app,
                                               handler_class=Handler)

    with server as httpd:
        logger.info('Serving on port 8000...')
        httpd.serve_forever()
