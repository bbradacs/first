import sys
import pybitcointools as bitcoin

# send BTC here!
fromAddress = '1AG6FXCHJSdtZtvsfwZYo6dVzGNV9gzDqG'
amount = 0.1
fee = 0.0

privkey1 = bitcoin.random_key()
privkey2 = bitcoin.random_key()
privkey3 = bitcoin.random_key()

pubkey1 = bitcoin.privtopub(privkey1)
pubkey2 = bitcoin.privtopub(privkey2)
pubkey3 = bitcoin.privtopub(privkey3)

pub = []
for x in range(0,3):
    pub.append(pubkey1)
script = bitcoin.mk_multisig_script(pub[0], pub[1], pub[2], 2, 3)
address = bitcoin.scriptaddr(script)

print script
print address

# figure out how much bitcoin is available at this address
history = bitcoin.unspent(fromAddress)
print history
total = bitcoin.sum(bitcoin.multiaccess(history, 'value'))

totalSend = amount + fee
currentValue = 0.0
inputs = []
for trans in history:
    inputs.append(trans)
    currentValue += trans['value']
    if currentValue >= totalSend:
        break 

inputLen = len(inputs)
transSize = inputLen * 400 + 34 * 2 + 10
if transSize > 10000:
    neededFee = 0.0
    transSize -= 1000

rawTX = bitcoin.mksend(inputs,    
