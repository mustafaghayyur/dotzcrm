from django.conf import settings as ds  # stands for django-settings
from core.helpers import misc

class Logger:
    def settings(self, app, file):
        self.app = app
        self.loggerFile = file
        
    def record(self, subject, log_message, level = 1):
        """
            Logs all C.U.D. operations in designated log-keeping-file
            
            :param subject: [*] any variable to inspect in logs
            :param log_message: string message for log
            :param level: 1 = minimal details | 2 = deep dive into 'subject'
        """
        if ds.DEBUG:
            misc.log(subject, {'space': self.app, 'msg': log_message}, level, self.loggerFile, crud=True)

