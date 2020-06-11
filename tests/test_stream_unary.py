import random
import string
import grpc

from papurika import ServiceMock


def test_mock_stream_unary_call(import_path):
    """Test Client Streaming gRpc Call"""
    from .pb import test_pb2
    from .pb import test_pb2_grpc

    class TestServicer(test_pb2_grpc.GRPCTestServicer):

        _server_id = random.randint(2, 2 ** 10)

        def ClientStreamingMethod(self, request_stresam, context):
            client_data = []

            for request in request_stresam:
                client_data.append(request.request_data)

            response = test_pb2.Response(
                server_id=self._server_id, response_data="".join(client_data)
            )
            return response

    with ServiceMock(
        "localhost:50051", TestServicer, assert_all_method_fired=False
    ):
        request_data = []

        def request_stream():
            for i in range(10):
                data = random.choice(string.ascii_letters)
                request_data.append(data)

                request = test_pb2.Request(client_id=1, request_data=data,)
                yield request

        with grpc.insecure_channel("localhost:50051") as channel:
            stub = test_pb2_grpc.GRPCTestStub(channel)
            response = stub.ClientStreamingMethod(request_stream())

            assert response.server_id == TestServicer._server_id
            assert request_data != []
            assert response.response_data == "".join(request_data)
