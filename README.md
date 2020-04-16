## SubScan Codec GRPC tool

-------

SubScan codec grpc tool is written in Python.It reference from https://github.com/polkascan/py-scale-codec, is lightweight, efficient grpc server.
It is not restricted by any language,you can find grpc example in https://grpc.io/.


### feature

1. Decode substrate metadata,Extrinsic,Event,chain storage
2. Reg custom type


### install

    virtualenv -p python3.6 env
    . env/bin/activate
    pip install -r requirements.txt
    
### install proto compile

    python -m pip install grpcio-tools

### server run
    
    python server.py
    
### proto compile

    python -m grpc_tools.protoc -I . --python_out=pb --grpc_python_out=pb codec.proto


