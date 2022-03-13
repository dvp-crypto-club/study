"""
이 파일은 Ethereum Client (Ganache, geth, parity 등) 에 대해 Python 으로 인터페이스 하기 위한 web.py 의 튜토리얼 파일임. 

Prerequisites
    1. Ganache 환경셋업 (포트는 8545 로 설정 및 본인이 설정한 포트로 URL 업데이트)
    2. pip install web3 수행하여 Python 환경에 라이브러리 설치


Rules
    1. 함수 및 변수 이름은 camelcase 로 작성 
    2. ALL 대문자는 상수 

"""

import web3
URL = "http://127.0.0.1:8545" # Ganache 로 구성한 Local Network 의 URL


def isValidAddress(w3, addr: str):
    """
    네트워크에 등록되어 있는 Address 가 valid 한 것인지 확인함.
    """

    print ("Check if the address is valid: ", addr)
    return w3.isAddress(addr)

def getLatestBlock(w3):
    """
    현재 네트워크에서 가장 최근 Block을 가져옴.
    """

    print ("Try to get the latest block")
    return w3.eth.get_block("latest")

def getAccounts(w3):
    """
    TODO: 테스트 필요 
    클라이언트에 등록되어 있는 모든 Account를 가져옴.
    """

    print ("Try to get accounts")
    #return w3.get_accounts()
    return []

def getBalance(w3, addr: str):
    """
    """
    print ("Try to get balance")
    checkSumAddr = w3.toChecksumAddress(addr)
    wei = w3.eth.get_balance(checkSumAddr)
    balance = w3.fromWei(wei, "ether")
    return balance

def getTransaction(w3, tx: str):
    print ("Try to get transaction")
    return w3.eth.get_transaction(tx)

def sendSignedTx(w3, sender: str, receiver: str, amount: int, key: str):

    print ("[Before] Sender's balance: {}".format(getBalance(w3, sender)))
    print ("[Before] Receiver's balance: {}".format(getBalance(w3, receiver)))

    wei = w3.toWei(amount, "ether")
    txn = {
        "from": sender,
        "to": receiver,
        "value": wei,
        "gas": 21000,
        "nonce": 2,
        "gasPrice": 0
    }

    signedTx = w3.eth.account.sign_transaction(txn, key)

    txnHash = w3.eth.send_raw_transaction(signedTx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(txnHash)

    print ("{} is transferred from {} to {}".format(amount, sender, receiver))
    print ("[After] Sender's balance: {}".format(getBalance(w3, sender)))
    print ("[After] Receiver's balance: {}".format(getBalance(w3, receiver)))

    return True


def sendEth(w3, sender: str, receiver: str, amount: int):
    print ("Try to send eth from {} to {}".format(sender, receiver))

    print ("[Before] Sender's balance: {}".format(getBalance(w3, sender)))
    print ("[Before] Receiver's balance: {}".format(getBalance(w3, receiver)))

    wei = w3.toWei(amount, "ether")
    txn = {
        "from": sender,
        "to": receiver,
        "value": wei,
        "gas": 21000,
        "gasPrice": 0
    }

    txnHash = w3.eth.send_transaction(txn)
    w3.eth.wait_for_transaction_receipt(txnHash)

    print ("{} is transferred from {} to {}".format(amount, sender, receiver))
    print ("[After] Sender's balance: {}".format(getBalance(w3, sender)))
    print ("[After] Receiver's balance: {}".format(getBalance(w3, receiver)))

    return True

    
def main():
    print ("main")
    w3 = web3.Web3(web3.HTTPProvider(URL))
    
    if w3.isConnected():
        addr = "0xfD9a5ae61f01b7b725B65d721C6fd57D6AA18b28"
        tx = "0x8e307720fc05325eb2ce6acb66f0f2da4d4e3832e5b0bdf33282c59b38c5e24c"
        sender = "0x21299d3962e184cd6d3aD229F470Ea42820a6469"
        receiver = "0xFd74714FDD8C7e8E74A2faf828719FDcC05D2DFd"

        # TEST 1 
        print ("***** Test 1 *****")
        if isValidAddress(w3, addr):
            print ("{} is a valid address!".format(addr))
        else:
            print ("{} is not a valid address!".format(addr))
        print ()

        # TEST 2
        print ("***** Test 2 *****")
        print ("Latest block info: {}".format(str(getLatestBlock(w3))))
        print ()

        # TEST 3
        print ("***** Test 3 *****")
        accounts = getAccounts(w3)
        print ("A list of accounts: ", accounts)
        print ()

        # TEST 4
        print ("***** Test 4 *****")
        balance = getBalance(w3, addr)
        print ("{} has {} eth".format(addr, balance))
        print ()

        # TEST 5
        print ("***** Test 5 *****")
        tx = getTransaction(w3, tx)
        print ("Transaction info : ", tx)
        print ()

        # TEST 6
        print ("***** Test 6 *****")
        senderKey = "01f0960c4a7dd77a33997dec97ca1eb2b83cddc163af66e400d0227a8a3707d5"
        signedTx = sendSignedTx(w3, sender, receiver, 1, senderKey)
        print ("Signed Tx: {}".format(signedTx))
        print ()

        """
        # TEST 7
        print ("***** Test 7 *****")
        tx = sendEth(w3, sender, receiver, 1)
        print ("Transaction info : ", tx)
        """


    else:
        print ("not avail")

def test():
    w3 = web3.Web3(web3.HTTPProvider(URL))
    tx = "0x8e307720fc05325eb2ce6acb66f0f2da4d4e3832e5b0bdf33282c59b38c5e24c"
    gas = w3.eth.estimate_gas(tx)
    print (gas)
    

if __name__ == "__main__":
    try:
        main()
        #test()
    except Exception as e:
        import traceback
        traceback.print_exc()
        
        print ("unexepcted error: ", str(e))
