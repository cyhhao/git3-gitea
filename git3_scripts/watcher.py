import json
import os
import time
import requests
from web3 import Web3
from web3.middleware import geth_poa_middleware


rpc = "https://galileo.web3q.io:8545"
web3 = Web3(Web3.HTTPProvider(rpc))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

abi = json.loads(
    '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes","name":"repoName","type":"bytes"},{"indexed":false,"internalType":"bytes","name":"ref","type":"bytes"}],"name":"PushRef","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes","name":"repoName","type":"bytes"},{"indexed":false,"internalType":"address","name":"owner","type":"address"}],"name":"RepoCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes","name":"repoName","type":"bytes"},{"indexed":false,"internalType":"address","name":"oldOwner","type":"address"},{"indexed":false,"internalType":"address","name":"newOwner","type":"address"}],"name":"RepoOwnerTransfer","type":"event"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"uint256","name":"chunkId","type":"uint256"}],"name":"chunkStakeTokens","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"name","type":"bytes"}],"name":"countChunks","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"}],"name":"createRepo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"ref","type":"bytes"}],"name":"delRef","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"}],"name":"download","outputs":[{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"uint256","name":"chunkId","type":"uint256"}],"name":"getChunkAddr","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isOptimize","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"}],"name":"listRefs","outputs":[{"components":[{"internalType":"bytes20","name":"hash","type":"bytes20"},{"internalType":"bytes","name":"name","type":"bytes"}],"internalType":"struct Git3Hub.refData[]","name":"list","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"","type":"bytes"}],"name":"nameToRefInfo","outputs":[{"internalType":"bytes20","name":"hash","type":"bytes20"},{"internalType":"uint96","name":"index","type":"uint96"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"}],"name":"remove","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"uint256","name":"chunkId","type":"uint256"}],"name":"removeChunk","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"","type":"bytes"}],"name":"repoNameToOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"repoNameToRefs","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"ref","type":"bytes"},{"internalType":"bytes20","name":"refHash","type":"bytes20"}],"name":"setRef","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"name","type":"bytes"}],"name":"size","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"}],"name":"stakeTokens","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upload","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"uint256","name":"chunkId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"uploadChunk","outputs":[],"stateMutability":"payable","type":"function"}]'
)

contract = web3.eth.contract(
    address="0x608860940b8f3D3247E1B301Cf2fA5690e6504DD", abi=abi
)


def main():
    base_auth = os.environ.get("base_auth")
    if not base_auth:
        raise Exception("base_auth not set")
    print(base_auth)

    last_end = os.environ.get("last") or 4304571
    N = 10000
    while True:
        current_block = web3.eth.block_number
        for start in range(last_end + 1, current_block, N):
            event_filter = contract.events.RepoCreated.createFilter(
                fromBlock=start,
                toBlock=start + N if start + N < current_block else current_block,
            )
            for RepoCreated in event_filter.get_all_entries():
                repoName = RepoCreated.args.repoName.decode()
                owner = str(RepoCreated.args.owner)
                print(
                    "RepoCreated",
                    RepoCreated.args.repoName.decode(),
                )

                res = requests.post(
                    "https://git3.link/api/v1/repos/migrate",
                    headers={
                        "Authorization": f"Basic {base_auth}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "auth_password": "",
                        "auth_token": "",
                        "auth_username": "",
                        "clone_addr": f"git3://{repoName}",
                        "description": f"owner: {owner}",
                        "issues": True,
                        "labels": True,
                        "lfs": False,
                        "lfs_endpoint": "",
                        "milestones": True,
                        "mirror": True,
                        "mirror_interval": "1h",
                        "private": False,
                        "pull_requests": True,
                        "releases": True,
                        "repo_name": repoName,
                        "repo_owner": "git3.w3q",
                        "service": "git",
                        "uid": 0,
                        "wiki": True,
                    },
                )
                print(res.status_code, res.text)
                print()

            event_filter = contract.events.PushRef.createFilter(
                fromBlock=start,
                toBlock=start + N if start + N < current_block else current_block,
            )
            for PushRef in event_filter.get_all_entries():
                repoName = PushRef.args.repoName.decode()
                print(
                    "PushRef",
                    PushRef.args.repoName.decode(),
                )
                res = requests.post(
                    f"https://git3.link/api/v1/repos/git3.w3q/{repoName}/mirror-sync",
                    headers={
                        "Authorization": f"Basic {base_auth}",
                        "Content-Type": "application/json",
                    },
                )
                print(res.status_code, res.text)
                print()

        last_end = current_block
        time.sleep(5)


if __name__ == "__main__":
    main()
