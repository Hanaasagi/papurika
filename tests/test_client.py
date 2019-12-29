import grpc

from papurika import ServiceMock


def test_run(import_path):
    from .wd import helloworld_pb2
    from .wd import helloworld_pb2_grpc

    class Greeter(helloworld_pb2_grpc.GreeterServicer):
        def SayHello(self, request, context):
            return helloworld_pb2.HelloReply(
                message="Hello, %s!" % request.name
            )

    with ServiceMock("localhost:50051", Greeter):
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = helloworld_pb2_grpc.GreeterStub(channel)
            response = stub.SayHello(helloworld_pb2.HelloRequest(name="you"))
            assert response.message == "Hello, you!"
