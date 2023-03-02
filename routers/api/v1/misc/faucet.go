package misc

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"strings"
	"time"

	"math/big"

	webcontext "code.gitea.io/gitea/modules/context"
	api "code.gitea.io/gitea/modules/structs"
	"code.gitea.io/gitea/modules/web"
	"github.com/ethereum/go-ethereum"
	"github.com/ethereum/go-ethereum/accounts"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/ethclient"
	hdwallet "github.com/miguelmota/go-ethereum-hdwallet"
)

var account accounts.Account
var wallet *hdwallet.Wallet
var client_arbg *ethclient.Client
var client_w3q *ethclient.Client

var explorer_arbg = "https://goerli.arbiscan.io/"
var explorer_w3q = "https://explorer.galileo.web3q.io/"

var requestAddress = map[common.Address]int64{}

func RequestFaucet(ctx *webcontext.APIContext) {
	form := web.GetForm(ctx).(*api.RequestFaucet)

	if len(form.Address) != 42 {
		ctx.Error(http.StatusBadRequest, "address", "Address is not valid")
		return
	}

	toAddr := common.HexToAddress(form.Address)

	if requestAddress[toAddr] > 0 && requestAddress[toAddr]+60*60*24 > time.Now().Unix() {
		ctx.Error(http.StatusBadRequest, "address", "This address has been claimed once within 24 hours")
		return
	}

	if wallet == nil {
		var mnemonic = os.Getenv("mm") //0x9E52bffd628596082f81dAAA3e2aB1408E9E0865
		var err error
		wallet, err = hdwallet.NewFromMnemonic(strings.TrimSpace(string(mnemonic)))
		if err != nil {
			ctx.Error(http.StatusInternalServerError, "mnemonic", "mnemonic is not valid")
			return
		}
		path := hdwallet.MustParseDerivationPath(fmt.Sprintf("m/44'/60'/0'/0/%d", 0))
		account, err = wallet.Derive(path, true)
		if err != nil {
			ctx.Error(http.StatusInternalServerError, "path", "path is not valid")
			return
		}
		client_arbg, _ = ethclient.Dial("https://goerli-rollup.arbitrum.io/rpc")
		client_w3q, _ = ethclient.Dial("https://galileo.web3q.io:8545")
	}

	w3q_txid, err := sendETHTo(client_w3q, big.NewInt(1e18), toAddr)
	if err != nil {
		ctx.Error(http.StatusInternalServerError, "sendETHTo", err.Error())
		return
	}

	arbg_txid, err := sendETHTo(client_arbg, big.NewInt(1e16*5), common.HexToAddress(form.Address))
	if err != nil {
		ctx.Error(http.StatusInternalServerError, "sendETHTo", err.Error())
		return
	}

	requestAddress[toAddr] = time.Now().Unix()

	ctx.JSON(http.StatusOK, map[string]interface{}{
		"address":     form.Address,
		"w3q_amount":  "1",
		"arbg_amount": "0.05",
		"w3q_tx":      fmt.Sprintf("%s/tx/%s", explorer_w3q, w3q_txid),
		"arbg_tx":     fmt.Sprintf("%s/tx/%s", explorer_arbg, arbg_txid),
	})
}

func sendETHTo(client *ethclient.Client, amount *big.Int, to common.Address) (string, error) {
	chainId, _ := client.ChainID(context.Background())
	nonce, _ := client.PendingNonceAt(context.Background(), account.Address)
	gasPrice, _ := client.SuggestGasPrice(context.Background())
	maxPriorityFeePerGas := big.NewInt(1500000000)
	gasLimit, _ := client.EstimateGas(context.Background(), ethereum.CallMsg{
		From:  account.Address,
		To:    &to,
		Value: amount,
		Data:  []byte{},
	})
	fmt.Println("sendETHTo", chainId, gasLimit)
	unsignTx := types.NewTx(&types.DynamicFeeTx{
		ChainID:   chainId,
		Nonce:     nonce,
		To:        &to,
		Value:     amount,
		GasTipCap: maxPriorityFeePerGas,
		GasFeeCap: gasPrice.Add(gasPrice, maxPriorityFeePerGas),
		Gas:       gasLimit,
		Data:      []byte{},
	})
	fmt.Println("unsignTx", unsignTx.GasTipCap(), unsignTx.GasFeeCap())
	signer := types.NewLondonSigner(chainId)
	priv, _ := wallet.PrivateKey(account)
	signedTx, err := types.SignTx(unsignTx, signer, priv)
	// signedTx, err := wallet.SignTxEIP155(account, unsignTx, chainId)
	if err != nil {
		fmt.Println("Sign", err)
		return "", err
	}
	err = client.SendTransaction(context.Background(), signedTx)
	if err != nil {
		fmt.Println("Boardcast", err)
		return "", err
	}
	return signedTx.Hash().Hex(), nil

}
