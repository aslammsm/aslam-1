# P2P Federated Learning System 🤖

This project is a decentralized Peer-to-Peer (P2P) Federated Learning implementation. It allows multiple nodes to train a machine learning model collaboratively without sharing their private data with a central server.

## 🚀 Key Features
* **Decentralized Training:** Nodes communicate directly to aggregate model updates.
* **Privacy-Preserving:** Raw data never leaves the local client.
* **Custom Communication Protocol:** Built using **gRPC** and **Protocol Buffers** (`peer.proto`) for efficient data exchange.

## 🛠️ Tech Stack
* **Language:** Python 3.10
* **Framework:** Flower (Flwr)
* **Communication:** gRPC
* **Scripting:** Bash (`setup.sh`)

## 📂 Project Structure
* `run_peer_fl.py`: The main entry point to start the federated learning cycle.
* `peer_client.py` & `peer_server.py`: Handles the P2P logic for sending/receiving weights.
* `peer.proto`: Defines the message structure for the gRPC service.
