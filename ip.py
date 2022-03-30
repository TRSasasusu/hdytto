# coding: hdytto

from code import InteractiveConsole

class HdyttoConsole(InteractiveConsole):
    def runsource(self, source, filename="<input>", symbol="single"):
        source = '# coding: hdytto\n' + source
        super().runsource(source, filename, symbol)

#InteractiveConsole().interact()
HdyttoConsole().interact()
