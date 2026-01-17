#!/usr/bin/env bash
set -e
echo "=== Setup script for flwr_p2p (Ubuntu, Python 3.10) ==="

# 1) create venv if missing
if [ ! -d "venv" ]; then
  python3.10 -m venv venv
fi

# 2) activate
source venv/bin/activate

# 3) upgrade pip
pip install --upgrade pip setuptools wheel

# 4) install working versions
pip install numpy==1.26.4
pip install protobuf==6.31.1
pip install grpcio==1.76.0 grpcio-tools==1.76.0
pip install flwr==1.9.0

echo
echo "=== DONE: dependencies installed into venv ==="
echo "Now generate gRPC code:"
echo "python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. peer.proto"
echo
echo "Then run server.py and run_peer_fl.py (see README for examples)."
