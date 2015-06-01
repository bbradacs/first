import sys
import getpass
import pybitcointools as bitcoin

# send BTC here!
fromAddress = '1AG6FXCHJSdtZtvsfwZYo6dVzGNV9gzDqG'
toAddress = fromAddress
amount = int(0.0001 * 100000000)
fee = 0.0

# In our case MultiSig works with three parties.  Each party keeps
# his own private key and never shares it.  A public key is created
# for each of the three private keys -- these public keys
# *are* shared between the the parties.  This way each member of
# the party can recreate the same script.
# privkey1 = bitcoin.random_key()
# privkey2 = bitcoin.random_key()
# privkey3 = bitcoin.random_key()

# use previously defined private keys
privkey1 = 'eeaef3180e49e1910e7fb5aff6047d04c2d29aa26c84686be82fd2fbb58f22c9'
privkey2 = '17b10bb69ee84975776fe3b9af8ee6fed3709484afdb915eca6d5a1968352b8c'
privkey3 = '897c738ca8aa4dca96a68926b1877bdbcc8e198eac85d26f3fc6f8c4b1673974'

pwd = getpass.getpass('Password: ')
privkey = bitcoin.sha256(pwd)

pubkey1 = bitcoin.privtopub(privkey1)
pubkey2 = bitcoin.privtopub(privkey2)
pubkey3 = bitcoin.privtopub(privkey3)

print 'privkey'
print '    ' + repr(privkey)
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
pub = [pubkey1, pubkey2, pubkey3]

print 'len(privkey1 = %d), len(pubkey1 = %d)' % (len(privkey1), len(pubkey1))
print 'len(privkey) = %d)' % len(privkey)
print ' ' 

# create the redemption script and its address 
script = bitcoin.mk_multisig_script(pub[0], pub[1], pub[2], 2, 3)
address = bitcoin.scriptaddr(script)

print 'script'
print '    ' + script
print '(script) address'
print '    ' + address

# just for kicks, see if the order of the keys matter when generating
# a script address; as far as I can tell the order does matter
script1 = bitcoin.mk_multisig_script(pub[2], pub[0], pub[1], 2, 3)
address1 = bitcoin.scriptaddr(script1)
print 'script1'
print '    ' + script1
print '(script1) address1'
print '    ' + address1
print ' '

# are they equal?
if script == script1:
    print '* the two scripts are the same *'
else:
    print '* the two scripts are different *'
if address == address1:
    print '* the two addresses are the same *'
else:
    print '* the two addresses are different *'
print ' ' 

# print 79 character separator
print '-' * 79

# figure out how much bitcoin is available at this address
history = bitcoin.unspent(fromAddress)
outputs = bitcoin.multiaccess(history, 'output')
values = bitcoin.multiaccess(history, 'value')
total = bitcoin.sum(values)

print 'history'
print '    ' + repr(history)
print 'outputs'
print '    ' + repr(outputs)
print 'values'
print '    ' + repr(values)
print 'total'
print '    ' + repr(total)
print ' '

# calculate the amount to send to the new (multisig) address
totalSend = amount + fee
currentValue = 0.0
inputs = []
for trans in history:
    inputs.append(trans)
    currentValue += trans['value']
    if currentValue >= totalSend:
        break 

print 'inputs'
print '    ' + repr(inputs)
print 'totalSend'
print '    ' + repr(totalSend)
print 'currentValue'
print '    ' + repr(currentValue)
print ' '

# calculate an appropriate mining fee based upon the length of
# the transaction inputs
inputLen = len(inputs)
neededFee = int(0.001 * 0) # int(.001 * 100000000)
transSize = inputLen * 400 + 34 * 2 + 10
if transSize > 10000:
    while transSize > 1000:
        neededFee += 0 # int(0.0001 * 100000000)
        transSize -= 1000

print 'inputLen'
print '    ' + repr(inputLen)
print 'transSize'
print '    ' + repr(transSize)
print 'neededFee'
print '    ' + repr(neededFee)


# ----------------------------------------------------------------------------
# The is where the real work starts
# At this point we have all of our inputs ready for the transaction.
# ----------------------------------------------------------------------------



# create the raw transaction using our private key (I'll assume that our
# private key is privkey1)
# Of course in a real application such code would never be put on a publicly
# available code repository.  ;)
myPrivKey = privkey1

rawTX = bitcoin.mksend(inputs, [toAddress+':'+str(amount)], fromAddress, neededFee)

# create a signature for each input
mySig = []
for x in range(0, inputLen):
    sig = bitcoin.multisign(rawTX, x, script, myPrivKey)
    mySig.append(sig)

print 'rawTX'
print '    ' + rawTX
print 'mySig[]'
print '    ' + repr(mySig)
print ' '


# now we need the following data for the next step of the multisig process
# rawTX: The original raw transaction
# script: The redemption script
# mySig[]: The signature for each input

# assume the other key is privkey2
otherPrivKey = privkey2

otherSig = []
for x in range(0, inputLen):
    sig = bitcoin.multisign(rawTX, x, script, otherPrivKey)
    if mySig[x] == sig:
        print " You already signed this. Send it to another key holder."
        sys.exit(0)
    otherSig.append(sig)

# now finish the signing with a second key holder
for x in range(0,inputLen):
    fullySignedTx = bitcoin.apply_multisignatures(rawTX, x, script, mySig[x], otherSig[x])

answer = raw_input("Do you want to send this transaction (Y/N)? ")
if answer in 'yY':
    # Don't actually do it until we understand what we're doing
    # bitcoind.eligius_pushtx(fullySignedTx)
    print 'Not implemented'
    pass
else:
    print 'Your transactons was not broadcast'
    sys.exit(0)



# the end.

