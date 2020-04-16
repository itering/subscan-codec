from websocket import create_connection
import ssl
import json


def get_current_metadata(endpoint, block_hash):
    ws = create_connection(endpoint, sslopt={"cert_reqs": ssl.CERT_NONE,
                                             "check_hostname": False,
                                             "ssl_version": ssl.PROTOCOL_TLSv1})
    q = {"id": 1, "jsonrpc": "2.0", "method": "state_getMetadata", "params": [block_hash]}
    ws.send(payload=json.dumps(q))
    j = json.loads(ws.recv())
    ws.close()
    return j["result"]
