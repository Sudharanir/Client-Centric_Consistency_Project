from concurrent import futures
import multiprocessing
import time
import json

import grpc
import example_pb2
import example_pb2_grpc

class Branch(example_pb2_grpc.RPCServicer):
    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches

    # receives request from customer, process the request and sends back the response
    def MsgDelivery(self, request, context):

        response = example_pb2.Response()
        response.id = request.id

        for x in range(len(request.events)) :
            event = request.events[x]

            # select the branch process with ID equls to destination ID in the event
            self = self.branches[event.dest-1]
            reqType = event.interface

            if reqType == 'query' :
                response.balance = QueryInterface(self)
            elif reqType == 'deposit' :
                DepositInterface(self, event.money)
            elif reqType == 'withdraw' :
                WithdrawInterface(self, event.money)

        return response

# returns the balance in a branch 
def QueryInterface(self) :
    return self.balance

# deposits the money in the branch and propagates the update to fellow branches
def DepositInterface(self, money) :
    self.balance = self.balance + money
    Propagate_Deposit(self, money)

# withdraws the amount from the branch and propagates the update to fellow branches
def WithdrawInterface(self, money) :
    if(self.balance >= money) : 
        self.balance = self.balance - money
        Propagate_Withdraw(self, money)

# increases the balance in the branches with the amount specified
def Propagate_Deposit(self, money) :
    for x in range(len(self.branches)) :
        if self.id != self.branches[x].id :
            self.branches[x].balance = self.branches[x].balance + money
 
# decreases the balance in the branches with the amount specified
def Propagate_Withdraw(self, money) :
    for x in range(len(self.branches)) :
        if self.id != self.branches[x].id :
            self.branches[x].balance = self.branches[x].balance - money

# starts the server for each branch on specified port
def _run_server(bind_address, branch):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5),)
    example_pb2_grpc.add_RPCServicerServicer_to_server(branch, server)
    server.add_insecure_port(bind_address)
    server.start()
    server.wait_for_termination()
    
def main():

    # load branches data from JSON file
    with open('./input.json', 'r') as f:
        data = json.load(f)

    inputBankList = []
    for x in range(len(data)) :
        if data[x]['type'] == 'branch' :
            inputBankList.append(data[x])

    # create branch process for each input branch
    branchProcessesList = []
    for x in range(len(inputBankList)) :
        branch = Branch(inputBankList[x]['id'], inputBankList[x]['balance'], [])
        branchProcessesList.append(branch)

    # assign branch processes list to 'branches' parameter
    for x in range(len(branchProcessesList)) :
        branchProcessesList[x].branches = branchProcessesList

    # generate ports
    basicPort = 50051
    portList = []
    for x in range(len(branchProcessesList)) :
        port = basicPort + x
        portList.append(port)

    # creates process for each branch and starts the server
    workers = []
    for x in range(len(branchProcessesList)):
        bind_address = f"[::]:{portList[x]}"
        worker = multiprocessing.Process(target=_run_server, args=(bind_address, branchProcessesList[x]))
        worker.start()
        print(f'server started on port {portList[x]}')
        workers.append(worker)

    for worker in workers:
        worker.join()

if __name__ == "__main__":
    main()