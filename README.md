# Papurika

[![Build Status](https://travis-ci.com/Hanaasagi/papurika.svg?token=wFiDySkCsstZBhsxAoPK&branch=master)](https://travis-ci.com/Hanaasagi/papurika)
[![black](https://img.shields.io/badge/code_style-black-000000.svg)](https://github.com/ambv/black)
[![License](https://img.shields.io/github/license/Hanaasagi/papurika.svg)](https://github.com/Hanaasagi/papurika/blob/master/LICENSE)
![](https://img.shields.io/github/languages/code-size/Hanaasagi/papurika.svg)

### Installing

```Bash
# Require pip>=19.0
pip install git+https://github.com:Hanaasagi/papurika.git
```

### Basics

```Python
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

```
