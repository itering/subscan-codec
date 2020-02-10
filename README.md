## SubScan codec gRpc tool

> reference from https://github.com/polkascan/py-scale-codec

## install

    virtualenv -p python3.6 env
    . env/bin/activate
    pip install -r requirements.txt
    
## install proto compile

    python -m pip install grpcio-tools

## server run
    
    python server.py
    
## proto compile

    python -m grpc_tools.protoc -I . --python_out=pb --grpc_python_out=pb rpc.proto
