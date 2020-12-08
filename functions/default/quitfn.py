from interfaces.function import IFunction


class QuitFn(IFunction):

    def __init__(self):
        super().__init__("Quit")

        self.arguments = {
        }

        self.menu_options = {
            "quit": self.quit
        }

    def quit(self, *args):
        quit()
