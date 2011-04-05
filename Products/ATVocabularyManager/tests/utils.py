import sys
import code


def interact(locals=None):
    """Emulate the interactive Python interpreter.

    locals -- passed to InteractiveInterpreter.__init__()

    thanks to Jens Klein aka jenzenz
    """

    savestdout = sys.stdout
    sys.stdout = sys.stderr
    console = code.InteractiveConsole(locals)
    console.interact("exit using Ctrl-D")
    sys.stdout = savestdout
