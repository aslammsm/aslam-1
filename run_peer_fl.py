#!/usr/bin/env python3
import argparse
from queue import Queue
from peer_server import start_peer_server
from peer_client import PeerClient
from flwr.client import start_client

def parse_args():
    parser = argparse.ArgumentParser(description="Run a Flower client with P2P gossip.")
    parser.add_argument("--cid", required=True, help="Client id (client1, client2, ...)")
    parser.add_argument("--port", type=int, required=True, help="gRPC port to listen on (e.g. 5051)")
    parser.add_argument("--peers", default="", help="Comma-separated peer addresses like localhost:5052,localhost:5053")
    parser.add_argument("--server", default="localhost:8080", help="Flower server address (host:port)")
    return parser.parse_args()

def main():
    args = parse_args()
    cid = args.cid
    port = args.port
    peer_addresses = [p.strip() for p in args.peers.split(",") if p.strip()]

    incoming_q = Queue()
    server = start_peer_server(cid, port, incoming_q)

    client = PeerClient(cid=cid, peer_addresses=peer_addresses, incoming_queue=incoming_q)

    # start_client will connect to the Flower server and run until server ends
    start_client(server_address=args.server, client=client)

if __name__ == "__main__":
    main()
