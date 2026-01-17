import grpc
from concurrent import futures
from queue import Queue
import peer_pb2
import peer_pb2_grpc

class PeerServer(peer_pb2_grpc.PeerServiceServicer):
    def __init__(self, cid, incoming_queue: Queue):
        self.cid = cid
        self.incoming_queue = incoming_queue

    def SendUpdate(self, request, context):
        print(f"[{self.cid}] Got update from {request.sender_id}")
        self.incoming_queue.put((request.sender_id, request.parameters, request.round))
        return peer_pb2.Ack(success=True)


def start_peer_server(cid: str, port: int, incoming_queue: Queue):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    peer_pb2_grpc.add_PeerServiceServicer_to_server(PeerServer(cid, incoming_queue), server)

    addr = f"[::]:{port}"
    server.add_insecure_port(addr)
    server.start()

    print(f"[{cid}] Peer gRPC server running on {addr}")
    return server
