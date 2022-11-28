### Client-Centric consistency for distributed banking system
This project is about implementing Client-Centric consistency model on a distributed banking system that accepts requests from customers to withdraw or deposit money from multiple branches.

### Getting Started:
Below step by step instructions will enable you to get the application up and running in your local machine for development and testing purposes.

### Prerequisites:
Minimum system requirements for running the program in local machine: Python 3.5 or higher pip version 9.0.1 or higher

If necessary, upgrade your version of pip:

```python -m pip install --upgrade pip```

Step1: Install gRPC : ```python -m pip install grpcio```

Step2: Install gRPC tools : ```python -m pip install grpcio-tools```

Step3: Generate gRPC code : ```python -m grpc_tools.protoc -I./protos protos/example.proto --python_out=. --grpc_python_out=.```

Steps for starting the banking application software:
Step1: Run the server : ```python branch.py```

Step2: Run the client : ```python customer.py```

**Note** : Input data is provided in input.json file
