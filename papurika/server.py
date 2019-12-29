from grpc._server import _validate_generic_rpc_handlers


class ServerMock:
    def __init__(self):
        self.handlers = {}

    def add_generic_rpc_handlers(self, generic_rpc_handlers):
        _validate_generic_rpc_handlers(generic_rpc_handlers)

        self.handlers.update(generic_rpc_handlers[0]._method_handlers)


__all__ = [
    "ServerMock",
]
