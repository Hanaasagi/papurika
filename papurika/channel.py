from collections import defaultdict

"""
Mock gRPC channels
"""


class ContextMock:
    def __init__(self):
        self._invocation_metadata = []

    def abort(self, code, details):
        raise Exception(code, details)

    def invocation_metadata(self):
        return self._invocation_metadata


class ChannelMock:
    def __init__(self, server_mock):
        """
        :param service:
        :return:
        """
        self._server_mock = server_mock
        self._call_count = defaultdict(lambda: 0)

    @property
    def call_count(self):
        return self._call_count

    def is_called(self, path) -> bool:
        return self._call_count.get(path, 0) != 0

    def _handle(self, method_name, path, *args, **kwargs):
        handler = self._server_mock.handlers[path]
        real_method = getattr(handler, method_name)

        def fake_handler(request):
            context = ContextMock()
            self._call_count[path] += 1
            return real_method(request, context)

        return fake_handler

    def unary_unary(
        self, method, request_serializer=None, response_deserializer=None,
    ):
        return self._handle("unary_unary", method)

    def unary_stream(
        self, method, request_serializer=None, response_deserializer=None,
    ):
        return self._handle("unary_stream", method)

    def stream_unary(
        self, method, request_serializer=None, response_deserializer=None,
    ):
        return self._handle("stream_unary", method)

    def stream_stream(
        self, method, request_serializer=None, response_deserializer=None,
    ):
        return self._handle("stream_stream", method)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        success = exc_type is None
        return success
