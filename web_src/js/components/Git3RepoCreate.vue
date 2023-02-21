<template>
  <div id="git3-repo-create" class="ui middle very relaxed page one column grid">
    <div class="column">
      <form class="ui form" method="post" action="javascript:void(0);">
        <h3 class="ui top attached header">
          {{ mode }} Repository
        </h3>
        <div class="ui attached segment">
          <div class="inline required field">
            <label for="repoName">Repo Name</label>
            <input name="repoName" v-model="repoName" autofocus required :disabled="mode != 'Create'">
          </div>
          <br />

          <div v-if="mode != 'Create'" class="inline field">
            <label for="owner">Owner</label>
            <span>{{ owner }}</span>
          </div>
          <br v-if="mode != 'Create'" />

          <div v-if="mode != 'Create'" class="inline required field">
            <label for="newOwner">New Owner</label>
            <input name="newOwner" v-model="newOwner" autofocus required>
          </div>
          <br v-if="mode != 'Create'" />

          <div v-if="errorTips" class="inline field" style="color: #ff3b3b;"><label></label>
            <span class="ui">
              {{ errorTips }}
            </span>
          </div>
          <br />

          <div class="inline field">
            <label></label>
            <button class="ui green button " :class="{ 'disabled': !isActive && isConnected }" @click="clickSubmit">
              {{ isConnected ? (mode == "Create" ? "Create" : "Transfer Owner") : "Connect Wallet" }}
            </button>
          </div>

          <div v-if="mode == 'Create'" class="inline field markup">
            <pre>You can also use: <span style="background-color: #00000045;font-size: 12px;padding: 4px;border-radius: 5px;">git3 create [hub_address]/[repo_name] </span> command to create the repo.</pre>
          </div>

        </div>

      </form>
    </div>
  </div>
</template>

<script>
import Onboard from '@web3-onboard/core'
import injectedModule from '@web3-onboard/injected-wallets'
import walletConnectModule from '@web3-onboard/walletconnect'
import { ethers } from 'ethers'
import { Buffer } from 'buffer'
import transactionPreviewModule from '@web3-onboard/transaction-preview'
import keystoneModule from '@web3-onboard/keystone'

const keystone = keystoneModule()

const transactionPreview = transactionPreviewModule()
const injected = injectedModule()
const walletConnect = walletConnectModule()
const onboard = Onboard({
  transactionPreview,
  wallets: [injected, walletConnect, keystone],
  apiKey: 'a6d67945-a99e-4d06-bbf8-1eed0cb76529',
  chains: [
    {
      id: '0xd06',
      token: 'W3Q',
      label: 'Web3Q Galileo',
      rpcUrl: 'https://galileo.web3q.io:8545',
      blockExplorerUrl: "https://explorer.galileo.web3q.io"
    }
  ],
  appMetadata: {
    name: "Git3",
    icon: "/assets/img/logo.png",
    description: "Git3: Git protocol for web3"
  },
  accountCenter: {
    desktop: {
      enabled: true,
      position: "bottomRight"
    }
  }
})

const Git3HubAddr = "0x59ef6b2dbfE86CcAaD84E2d8e78177f528521Da9"
const Git3HubAbi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes","name":"repoName","type":"bytes"},{"indexed":false,"internalType":"bytes","name":"ref","type":"bytes"}],"name":"PushRef","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes","name":"repoName","type":"bytes"},{"indexed":false,"internalType":"address","name":"owner","type":"address"}],"name":"RepoCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes","name":"repoName","type":"bytes"},{"indexed":false,"internalType":"address","name":"oldOwner","type":"address"},{"indexed":false,"internalType":"address","name":"newOwner","type":"address"}],"name":"RepoOwnerTransfer","type":"event"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"uint256","name":"chunkId","type":"uint256"}],"name":"chunkStakeTokens","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"name","type":"bytes"}],"name":"countChunks","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"}],"name":"createRepo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"ref","type":"bytes"}],"name":"delRef","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"}],"name":"download","outputs":[{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"uint256","name":"chunkId","type":"uint256"}],"name":"getChunkAddr","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isOptimize","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"}],"name":"listRefs","outputs":[{"components":[{"internalType":"bytes20","name":"hash","type":"bytes20"},{"internalType":"bytes","name":"name","type":"bytes"}],"internalType":"struct Git3HubStorage.refData[]","name":"list","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"","type":"bytes"}],"name":"nameToRefInfo","outputs":[{"internalType":"bytes20","name":"hash","type":"bytes20"},{"internalType":"uint96","name":"index","type":"uint96"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"}],"name":"remove","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"uint256","name":"chunkId","type":"uint256"}],"name":"removeChunk","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"","type":"bytes"}],"name":"repoNameToOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"repoNameToRefs","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"ref","type":"bytes"},{"internalType":"bytes20","name":"refHash","type":"bytes20"}],"name":"setRef","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"name","type":"bytes"}],"name":"size","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"}],"name":"stakeTokens","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upload","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes","name":"repoName","type":"bytes"},{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"uint256","name":"chunkId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"uploadChunk","outputs":[],"stateMutability":"payable","type":"function"}]'

export default {
  name: 'Git3RepoCreate',

  data: () => {
    return {
      isConnected: false,
      isActive: false,
      repoName: location.href.split("transfer=")[1],
      contract: null,
      errorTips: "",
      mode: location.href.indexOf("transfer") >= 0 ? "Transfer" : "Create",
      address: null,
      newOwner: "",
      owner: ""
    };
  },

  watch: {
    repoName(newVal) {
      if (newVal) {
        if (/^[a-zA-Z0-9.\-_]+$/.test(newVal)) {
          this.isActive = true
          this.errorTips = ""
          return
        }
        else {
          this.errorTips = "only letters, numbers, '.', '-', '_' are allowed"
        }
        console.log("watch repoName", newVal)
      }
      this.isActive = false
    }
  },

  async mounted() {
    const walletsSub = onboard.state.select('wallets')
    const { unsubscribe } = walletsSub.subscribe((wallets) => {
      console.log("subscribe", wallets)
      if (wallets.length == 0) {
        this.isConnected = false
      } else {
        this.initWallet(wallets)
      }
      const connectedWallets = wallets.map(({ label }) => label)
      window.localStorage.setItem('connectedWallets', JSON.stringify(connectedWallets))

    })
    this.unsubscribe = unsubscribe

    const previouslyConnectedWallets = JSON.parse(window.localStorage.getItem('connectedWallets'))

    if (previouslyConnectedWallets) {
      const wallets = await onboard.connectWallet({
        autoSelect: { label: previouslyConnectedWallets[0], disableModals: true }
      })
      // this.initWallet(wallets)
    }
  },

  unmounted() {
    this.unsubscribe()
  },

  methods: {

    async initWallet(wallets) {
      this.errorTips = ""
      this.isActive = true

      console.log(wallets[0])
      const success = await onboard.setChain({ chainId: '0xd06' })
      console.log(success)
      const ethersProvider = new ethers.providers.Web3Provider(
        wallets[0].provider,
        'any'
      )
      let signer = ethersProvider.getSigner()
      this.contract = new ethers.Contract(Git3HubAddr, Git3HubAbi, signer)
      this.address = await signer.getAddress()
      window.contract = this.contract

      this.isConnected = true

      // init data
      if (this.mode != "Create") {
        this.owner = await this.contract.repoNameToOwner(Buffer.from(this.repoName))
        if (this.owner != this.address) {
          this.errorTips = "You are not the owner of this repo"
          this.isActive = false
        }
      }

    },
    async clickSubmit() {
      if (!this.isConnected) {
        const wallets = await onboard.connectWallet()
        this.initWallet(wallets)
      } else {
        let owner = await this.contract.repoNameToOwner(Buffer.from(this.repoName))
        console.log(owner)

        if (this.mode == "Create") {
          if (owner != "0x0000000000000000000000000000000000000000") {
            this.errorTips = "Repo name already exists"
            return
          } else {
            try {
              let rept = await this.contract.createRepo(Buffer.from(this.repoName))
              console.log(rept)
            }
            catch (e) {
              console.error(e)
            }
          }
        } else {

          if (owner != this.address) {
            this.errorTips = "You are not the owner of this repo"
            return
          } else {
            try {
              let rept = await this.contract.transferOwnership(Buffer.from(this.repoName), this.newOwner)
              console.log(rept)
            }
            catch (e) {
              console.error(e)
            }
          }
        }

      }
    }
  },
};
</script>
