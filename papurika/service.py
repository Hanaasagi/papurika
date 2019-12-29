import grpc
import inspect

from unittest.mock import patch

from papurika.server import ServerMock
from papurika.channel import ChannelMock


"""
Mock gRPC services
"""


class ServiceMock:
    def __init__(
        self, listen_at: str, service, *, assert_all_method_fired: bool = True,
    ) -> None:
        """
        :param listen_at:
        :return:
        """
        self._listen_at = listen_at
        self._standin = service
        self._assert_all_method_fired = assert_all_method_fired

        self._patcher = None
        self._server = ServerMock()
        self._inject_service()
        self._channel = ChannelMock(self._server)

    def _format_inject_call_name(self, service_name: str) -> str:
        return f"add_{service_name}_to_server"

    def _inject_service(self) -> None:
        """Inject mock service to the server.
        """
        parent_class = inspect.getmro(self._standin)[1]
        parent_class_module = inspect.getmodule(parent_class)

        inject_name = self._format_inject_call_name(parent_class.__name__)

        inject = getattr(parent_class_module, inject_name)
        inject(self._standin(), self._server)

    @property
    def channel(self):
        return self._channel

    def start(self):
        # TODO secure_channel
        def _insecure_channel(target, options=None, compression=None):
            if target == self._listen_at:
                return self._channel
            return grpc.insecure_channel(target, options, compression)

        self._patcher = patch(
            target="grpc.insecure_channel", new=_insecure_channel,
        )
        self._patcher.start()

    def stop(self, allow_assert: bool = True) -> None:
        self._patcher.stop()

        if not allow_assert:
            return

        not_called = []
        for path in self._server.handlers.keys():
            if not self._channel.is_called(path):
                not_called.append(path)

        if self._assert_all_method_fired and not_called:
            raise AssertionError(
                "Not all requests have been executed {0!r}".format(
                    [path for path in not_called]
                )
            )

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        success = exc_type is None
        self.stop(allow_assert=success)
        return success


class ServiceMockGroup:
    def __init__(self):
        self.reset()

    def reset(self):
        self._services = {}
        self._calls = []

    def add(self, listen_at, service, *, assert_all_method_fired: bool = True):
        service_mock = ServiceMock(
            listen_at, service, assert_all_method_fired=assert_all_method_fired
        )
        self._services[listen_at] = service_mock

    def _dispatch(self, target):
        return self._services.get(target, None)

    def start(self):
        def _insecure_channel(target, options=None, compression=None):
            service = self._dispatch(target)
            if service is not None:
                return service.channel
            return grpc.insecure_channel(target, options, compression)

        self._patcher = patch(
            target="grpc.insecure_channel", new=_insecure_channel,
        )
        self._patcher.start()

    def stop(self, allow_assert):
        self._patcher.stop()

        if not allow_assert:
            return

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        success = exc_type is None
        self.stop(allow_assert=success)
        return success


__all__ = [
    "ServerMock",
    "ServiceMockGroup",
]
