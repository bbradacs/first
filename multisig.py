import sys
import pybitcointools as bitcoin

# send BTC here!
fromAddress = '1AG6FXCHJSdtZtvsfwZYo6dVzGNV9gzDqG'
amount = 0.01
fee = 0.0

# In our case MultiSig works with three parties.  Each party keeps
# his own private key and never shares it.  A public key is created
# for each of the three private keys -- these public keys
# *are* shared between the the parties.  This way each member of
# the party can recreate the same script.
privkey1 = bitcoin.random_key()
privkey2 = bitcoin.random_key()
privkey3 = bitcoin.random_key()

pubkey1 = bitcoin.privtopub(privkey1)
pubkey2 = bitcoin.privtopub(privkey2)
pubkey3 = bitcoin.privtopub(privkey3)

print 'privkey1'
print '    ' + repr(privkey1)
print 'privkey2'
print '    ' + repr(privkey2)
print 'privkey3'
print '    ' + repr(privkey3)
print ' ' 

print 'pubkey1'
print '    ' + repr(pubkey1)
print 'pubkey2'
print '    ' + repr(pubkey2)
print 'pubkey3'
print '    ' + repr(pubkey3) 
print ' '

# Make a list of the public keys
pub = []
for x in range(0,3):
    pub.append(pubkey1)

print 'len(pub)'
print '    ' + repr(len(pub))
print ' ' 

# 
script = bitcoin.mk_multisig_script(pub[0], pub[1], pub[2], 2, 3)
address = bitcoin.scriptaddr(script)

print 'script'
print '    ' + script
print '(script) address'
print '    ' + address

# just for kicks, see if the order of the keys matter when generating
# a script address; as far as I can tell, order does not matter
script1 = bitcoin.mk_multisig_script(pub[2], pub[0], pub[1], 2, 3)
address1 = bitcoin.scriptaddr(script)
print 'script2'
print '    ' + script1
print 'address1'
print '    ' + address1
print ' '

# are they equal?
if script == script1:
    print 'the two scripts are the same'
else:
    print ' the two scripts are different'

print ' ' 

# figure out how much bitcoin is available at this address
history = bitcoin.unspent(fromAddress)
total = bitcoin.sum(bitcoin.multiaccess(history, 'value'))

print 'history'
print '    ' + repr(history)
print 'total'
print '    ' + repr(total)

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

