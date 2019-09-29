## install

    virtualenv -p python3.6 env
    . env/bin/activate
    pip install -r requirements.txt
    
    
## install proto compile
    python -m pip install grpcio-tools

## proto compile

    python -m grpc_tools.protoc -I . --python_out=libs --grpc_python_out=libs rpc.proto
    
## server run
    
    python rpc_server.py
    
## client run
    
    python rpc_client.py
    
    
## update scalecodec
    pip uninstall -y scalecodec && pip install -r requirements.txt