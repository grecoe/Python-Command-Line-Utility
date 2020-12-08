import os
from datetime import datetime


class Logger:

    @staticmethod
    def add_log(message, log_directory="./logs", log='app.log'):
        """
        Very simple logger that just dumps out the message with a time stamp
        with append only. Careful this could create an enormous log.
        """
        log = Logger._get_log_path(log_directory, log)

        output = "\n{}\t{}".format(str(datetime.now()), message)
        with open(log, 'a') as log_file:
            log_file.writelines(output)

    @staticmethod
    def clear_log(max_size=102400, log_directory="./logs", log='app.log'):
        """
        Checks the size of the log and renames it if it is already
        a certain size.
        """
        log = Logger._get_log_path(log_directory, log)
        if os.path.exists(log):
            size = os.path.getsize(log)
            print("Log is {} bytes".format(size))
            if size >= max_size:
                os.remove(log)
                Logger.add_log("Log file cleared on size...")

    @staticmethod
    def _get_log_path(log_directory, log):
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        return os.path.join(log_directory, log)
