from logutils.logger import Logger
from datetime import datetime


class LogDecorator:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        # Funciton return value
        return_value = None

        # Start time
        function_start = datetime.now()

        # Base message
        spacer = '\t' * 8
        out_message_base = "Module: {} - Function: {} ".format(
            self.function.__module__,
            self.function.__name__)

        out_message_base += "\n{}ARGUMENTS: {}".format(spacer, args)
        for cont in self._breakdown("\t", 9, "*args", args):
            out_message_base += "\n{}".format(cont)
        for cont in self._breakdown("\t", 9, "**kwargs", kwargs):
            out_message_base += "\n{}".format(cont)

        caught_exception = None
        try:
            # Execute funciton, if exception log it
            return_value = self.function(*args, **kwargs)
        except Exception as ex:
            caught_exception = ex
            out_message_base += "\n{}EXCEPTION: {}".format(spacer, str(ex))

        # Add function return
        if return_value:
            out_message_base += "\n{}RETURNS: {}".format(spacer, return_value)
            for cont in self._breakdown("\t", 9, "return_value", return_value):
                out_message_base += "\n{}".format(cont)


        # Add clock to function
        span = datetime.now() - function_start
        out_message_base += "\n{}EXECUTION: {}".format(spacer, str(span))

        # Finally log it and return the function return value
        Logger.add_log(out_message_base)

        if caught_exception:
            raise caught_exception

        return return_value

    def _breakdown(self, spacer_char, depth, name, obj):
        return_data = []
        if name:
            return_data.append("{}{}".format((spacer_char*depth), name))

        if isinstance(obj, list):
            for item in obj:
                res = self._breakdown(spacer_char, depth+1, None, item)
                return_data.extend(res)
        elif isinstance(obj, dict):
            for item in obj.keys():
                res = self._breakdown(spacer_char, depth+1, item, obj[item])
                return_data.extend(res)
        elif isinstance(obj, tuple):
            for idx in range(len(obj)):
                res = self._breakdown(spacer_char, depth+1, None, obj[idx])
                return_data.extend(res)
        else:
            if not hasattr(obj, "__dict__"):
                return_data.append("{}{} - {}".format((spacer_char * depth),type(obj), str(obj)))
            else:
                obj_vars = vars(obj)
                for v in obj_vars:
                    return_data.append("{}{} - {} - {}".format((spacer_char * depth),v, type(obj_vars[v]), str(obj_vars[v])))

                    if isinstance(obj_vars[v], list) or isinstance(obj_vars[v],dict) or hasattr(obj_vars[v], "__dict__"):
                        res = self._breakdown(spacer_char, depth+1, v, obj_vars[v])
                        return_data.extend(res)

        return return_data