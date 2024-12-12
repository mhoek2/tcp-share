# app core modules
from typing import TYPE_CHECKING, TypedDict

from modules.app.read_write import ReadWrite
from modules.app.settings import Settings
from modules.tcp import TCP

import datetime;

if TYPE_CHECKING:
    from main import Application

class Logging:
    class LogData_t(TypedDict):
        ip: str
        file: str
        comment: str
        datetime: str

    def __init__( self, context ) -> None:
        self.context : "Application" = context
        self.settings : Settings = context.settings

    def log( self, data : LogData_t ):
        """Write to log file"""
        log = self.context.read_write.getLogFile()
        log.append( data )
        self.context.read_write.writeLogFile( log )

    def log_file( self, filename : str, comment : str ):
        data : self.LogData_t = { "ip": self.settings.server_ip, 
                                  "file": filename, 
                                  "comment": comment, 
                                  "datetime": str(datetime.datetime.now())
                                }
        self.log( data )