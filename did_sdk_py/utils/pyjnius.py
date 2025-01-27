from collections.abc import Callable
from typing import ClassVar

from jnius.jnius import PythonJavaClass, java_method


class Runnable(PythonJavaClass):
    __javainterfaces__: ClassVar = ["java/lang/Runnable"]

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    @java_method("()V")
    def run(self):
        self.callback()


class ErrorHandlerBiConsumer(PythonJavaClass):
    __javainterfaces__: ClassVar = ["java/util/function/BiConsumer"]

    def __init__(self, error_handler: Callable[[Exception], None]):
        super().__init__()
        self.error_handler = error_handler

    @java_method("(Ljava/lang/Object;Ljava/lang/Object;)V")
    def accept(self, error, _):
        self.error_handler(Exception(error.toString()))
