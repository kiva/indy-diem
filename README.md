# Indy-Diem
## Indy transaction layer for Diem ledger

### Getting Started 

Requirements:
* Rust lang
* Python 3.6 or greater 

### writing your first transaction to the Diem Test net

First make sure you have python installed on your system by running this command 

```
python --version
```

If this works then you are ready to run the script that will setup your virtual enviroment. This means that your local python packages and setup won't be interupted. If anything fails simply delete the `./venv` directory. 

```
./scripts/createEnv.sh
```

Now you are ready to send a "payment" to another peer and have it written on
the Diem ledger.  In this payment you will send your metadata which will include your Indy transaction. This eventually will be  more sophisticated and have signatures and proof etc. Keep an eye out for this!

```
./venv/bin/python indy-diem/writeATransaction.py
```

FEEL free to modify the variable `INDY_TXN` in `writeATransaction.py` to make the transaction your own.

Now you may want to verify that your transaction is on the ledger. In yor terminal run this:


```
curl -X POST -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","method":"get_account_transaction","params":["<INSERT SENDER OR RECIEVER ID HERE>", 0, true],"id":1}' https://testnet.diem.com/v1

```










