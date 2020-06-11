import random
import string
import grpc

from papurika import ServiceMock


def test_mock_unary_stream_call(import_path):
    """Test Server Streaming gRpc Call"""
    from .pb import test_pb2
    from .pb import test_pb2_grpc

    class TestServicer(test_pb2_grpc.GRPCTestServicer):

        _server_id = random.randint(2, 2 ** 10)

        def ServerStreamingMethod(self, request, context):
            def response_stream():
                for data in request.request_data:
                    response = test_pb2.Response(
                        server_id=self._server_id, response_data=data,
                    )
                    yield response

            return response_stream()

    with ServiceMock(
        "localhost:50051", TestServicer, assert_all_method_fired=False
    ):
        with grpc.insecure_channel("localhost:50051") as channel:
            request_data = "".join(
                [random.choice(string.ascii_letters) for _ in range(10)]
            )
            stub = test_pb2_grpc.GRPCTestStub(channel)
            response_stream = stub.ServerStreamingMethod(
                test_pb2.Request(client_id=1, request_data=request_data)
            )

            data = []
            for response in response_stream:
                assert response.server_id == TestServicer._server_id
                data.append(response.response_data)

            assert "".join(data) == request_data
