import random
import string
import grpc

from papurika import ServiceMock


def test_mock_stream_stream_call(import_path):
    """Test Bidirectional Streaming gRpc Call"""
    from .pb import test_pb2
    from .pb import test_pb2_grpc

    class TestServicer(test_pb2_grpc.GRPCTestServicer):

        _server_id = random.randint(2, 2 ** 10)

        def BidirectionalStreamingMethod(self, request_stream, context):
            def response_stream():
                for request in request_stream:
                    response = test_pb2.Response(
                        server_id=self._server_id,
                        response_data=request.request_data,
                    )
                    yield response

            return response_stream()

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
            response_stream = stub.BidirectionalStreamingMethod(
                request_stream()
            )

            for idx, response in enumerate(response_stream):
                assert response.response_data == request_data[idx]
