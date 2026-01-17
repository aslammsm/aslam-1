import time
import numpy as np
import pickle
from queue import Queue, Empty
import grpc
from typing import List

from flwr.client import NumPyClient
from flwr.common import ndarrays_to_parameters, parameters_to_ndarrays

import peer_pb2
import peer_pb2_grpc


class PeerClient(NumPyClient):
    """
    P2P Flower Client using pure NumPy/Pickle for gossip serialization.
    This avoids all protobuf/Flower serialization issues.
    """

    def __init__(self, cid: str, peer_addresses: List[str], incoming_queue: Queue):
        self.cid = cid
        self.peer_addresses = peer_addresses
        self.incoming_queue = incoming_queue
        self.model_weights = [np.zeros(3)]
        self.current_round = 0

    # ------- Flower API --------

    def get_parameters(self, config):
        return self.model_weights

    def fit(self, parameters, config):
        self.current_round = int(config.get("round", 1))

        print(f"[{self.cid}] Training round {self.current_round}")

        # Dummy training — replace with your own
        self.model_weights = [p + 1 for p in parameters]

        # --------------------------
        # Serialize model weights
        # --------------------------
        params_bytes = pickle.dumps(self.model_weights)

        # --------------------------
        # Send update to peers
        # --------------------------
        for peer_addr in self.peer_addresses:
            try:
                with grpc.insecure_channel(peer_addr) as channel:
                    stub = peer_pb2_grpc.PeerServiceStub(channel)
                    msg = peer_pb2.ModelUpdate(
                        sender_id=self.cid,
                        parameters=params_bytes,
                        round=self.current_round,
                    )
                    stub.SendUpdate(msg, timeout=2.0)
                    print(f"[{self.cid}] → Sent update to {peer_addr}")
            except Exception as e:
                print(f"[{self.cid}] ERROR sending to {peer_addr}: {e}")

        # --------------------------
        # Collect updates
        # --------------------------
        collected = []
        deadline = time.time() + 1.0

        while time.time() < deadline:
            try:
                sender, raw, r = self.incoming_queue.get(timeout=0.1)

                if r != self.current_round:
                    self.incoming_queue.put((sender, raw, r))
                    continue

                nds = pickle.loads(raw)
                collected.append(nds)
                print(f"[{self.cid}] ← Received update from {sender}")

            except Empty:
                pass

        # --------------------------
        # Aggregate updates
        # --------------------------
        if collected:
            new_weights = []
            for i, own in enumerate(self.model_weights):
                stack = [own] + [c[i] for c in collected]
                new_weights.append(np.mean(stack, axis=0))
            self.model_weights = new_weights

            print(f"[{self.cid}] Aggregated {len(collected)} peer updates")

        num_examples = sum(w.size for w in self.model_weights)
        return self.model_weights, num_examples, {}

    def evaluate(self, parameters, config):
        loss = float(np.sum(parameters[0]))
        return loss, len(parameters[0]), {"loss": loss}
