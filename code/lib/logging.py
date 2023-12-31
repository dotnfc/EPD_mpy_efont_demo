#
# https://github.com/erikdelange/MicroPython-Logging
#
import sys
import time
import os
try:
    import urequests
except ImportError:
    pass
    
import json

CRITICAL = const(50)
ERROR = const(40)
WARNING = const(30)
INFO = const(20)
DEBUG = const(10)
NOTSET = const(0)

_level_str = {
    CRITICAL: "CRITICAL",
    ERROR: "ERROR",
    WARNING: "WARNING",
    INFO: "INFO",
    DEBUG: "DEBUG"
}

_stream = sys.stderr  # default output
_filename = None # '/log.log'  # overrides stream
_level = INFO  # ignore messages which are less severe
_format = "%(asctime)s:%(levelname)s:%(message)s"  # default message format
_loggers = dict()

_max_size = 15000 # max size of the log file
_prune_size = 10000 # size to prune the log file too when too big


class Logger:

    def __init__(self, name):
        self.name = name
        self.level = _level

    def _get_log_str(self,level,message,*args):
        if args:
            message = message % args

        record = dict()
        record["levelname"] = _level_str.get(level, str(level))
        record["level"] = level
        record["message"] = message
        record["name"] = self.name
        tm = time.localtime()
        record["asctime"] = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}" \
            .format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])

        return _format % record + "\n"
    
        
    def log(self, level, message, *args):
        if level < self.level:
            return

        try:
            error_text = ''
            err = None
            
            log_str = self._get_log_str(level,message,*args)

            if _filename is None:
                _ = _stream.write(log_str)
            else:
                try:
                    from settings.settings import settings
                    from wlan_helper import connection
                    if connection.is_connected():
                        urequests.post(settings.log_export_url,data=json.dumps({'device_id':settings.device_id,'log':log_str}))
                except ImportError:
                    # Settings and wifi_connect may try to log something before they're setup
                    pass
                except Exception as e:
                    if 'EHOSTUNREACH' not in str(e): # most likely don't have a connection
                        # log the error even thou it probably can't be sent to server...
                        err = e
                        error_text = self._get_log_str(level,f"Log post error: {str(e)}")
                
                with open(_filename, "a") as fp:
                    fp.write(log_str)
                    if error_text:
                        fp.write(error_text)
                        sys.print_exception(err, fp)
                        message += '\n' + error_text # this will print out if in debug
                                                
                # Allways print out the log message when in debug
                if self.level == DEBUG:
                    print(message)
                    
                prune(_filename)


        except Exception as e:
            print("--- Logging Error ---")
            print(repr(e))
            print("Message: '" + message + "'")
            print("Arguments:", args)
            print("Format String: '" + _format + "'")
            raise e

    def setLevel(self, level):
        self.level = level

    def debug(self, message, *args):
        self.log(DEBUG, message, *args)

    def info(self, message, *args):
        self.log(INFO, message, *args)

    def warning(self, message, *args):
        self.log(WARNING, message, *args)

    def error(self, message, *args):
        self.log(ERROR, message, *args)

    def critical(self, message, *args):
        self.log(CRITICAL, message, *args)

    def exception(self, exception, message, *args):
        # if seetings is debug and there is a file, print the message
        self.log(ERROR, message, *args)

        if _filename is None or self.level == DEBUG:
            sys.print_exception(exception, _stream)
            
        if not _filename is None:
            with open(_filename, "a") as fp:
                sys.print_exception(exception, fp)
                

def getLogger(name="root"):
    if name not in _loggers:
        _loggers[name] = Logger(name)
    return _loggers[name]


def basicConfig(level=INFO, filename=None, filemode='a', format=None):
    global _filename, _level, _format
    _filename = filename
    _level = level
    if format is not None:
        _format = format

    if filename is not None and filemode != "a":
        with open(filename, "w"):
            pass  # clear log file


def setLevel(level):
    getLogger().setLevel(level)

huh = 'Undefined Message' # just to avoid error if no message provided

def debug(message=huh, *args):
    getLogger().debug(message, *args)


def info(message=huh, *args):
    getLogger().info(message, *args)


def warning(message=huh, *args):
    getLogger().warning(message, *args)


def error(message=huh, *args):
    getLogger().error(message, *args)


def critical(message=huh, *args):
    getLogger().critical(message, *args)


def exception(exception, message=huh, *args):
    getLogger().exception(exception, message, *args)
    
def prune(filename):
    # reduce log file to no more than 
    try:
        s = os.stat(filename)[6] #file size in bytes
        tmp_file = filename + 'tmp'
        
        if s > _max_size:
            with open(filename,'r') as old:
                old.seek(s - _prune_size)
                with open(tmp_file,'w') as new:
                    new.write('------------- pruned ----------------\n')
                    x = True
                    while x:
                        x = old.readline()
                        if x:
                            new.write(x)
                            
            # swap files
            os.remove(filename)
            os.rename(tmp_file,filename)
            
    except Exception as e:
        # logging this may cause an infinate loop
        print(f'Exception pruning log: {str(e)}')
        
        
