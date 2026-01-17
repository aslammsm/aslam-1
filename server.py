import flwr as fl
from flwr.server.strategy import FedAvg

# -----------------------------
# Custom strategy WITHOUT reconnect
# -----------------------------
class NoReconnectStrategy(FedAvg):
    def __init__(self):
        super().__init__()
    
    # This disables Flower sending reconnect attempts
    def evaluate(self, server_round, parameters):
        return None
    
    def configure_fit(self, server_round, parameters, client_manager):
        # Wait for clients to appear (NO forced reconnect)
        connected_clients = client_manager.num_available()

        print(f"[SERVER] Waiting for clients... currently connected: {connected_clients}")

        # Allow the server to wait until at least 2 clients are up
        while connected_clients < 2:
            import time
            time.sleep(1)
            connected_clients = client_manager.num_available()
            print(f"[SERVER] Still waiting... connected: {connected_clients}")

        return super().configure_fit(server_round, parameters, client_manager)

# -----------------------------
# Start server with modified strategy
# -----------------------------
fl.server.start_server(
    server_address="0.0.0.0:8080",
    config=fl.server.ServerConfig(
        num_rounds=3,
        round_timeout=None,       # no timeout
    ),
    strategy=NoReconnectStrategy(),
)
