import random
import string
import grpc

from papurika import ServiceMock


def test_mock_unary_stream_call(import_path):
    """Test Single gRpc Call"""
    from .pb import test_pb2
    from .pb import test_pb2_grpc

    class TestServicer(test_pb2_grpc.GRPCTestServicer):

        _server_id = random.randint(2, 2 ** 10)

        def SingleMethod(self, request, context):

            return test_pb2.Response(
                server_id=self._server_id, response_data=request.request_data
            )

    with ServiceMock(
        "localhost:50051", TestServicer, assert_all_method_fired=False
    ):
        with grpc.insecure_channel("localhost:50051") as channel:
            request_data = random.choice(string.ascii_letters)

            stub = test_pb2_grpc.GRPCTestStub(channel)
            response = stub.SingleMethod(
                test_pb2.Request(client_id=1, request_data=request_data)
            )
            assert response.server_id == TestServicer._server_id
            assert response.response_data == request_data
