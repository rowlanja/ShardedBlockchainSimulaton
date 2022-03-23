from blspy import (PrivateKey, Util, AugSchemeMPL, PopSchemeMPL,
                   G1Element, G2Element)

seed: bytes = bytes([0,  50, 6,  244, 24,  199, 1,  25,  52,  88,  192,
                        19, 18, 12, 89,  6,   220, 18, 102, 58,  209, 82,
                        12, 62, 89, 110, 182, 9,   44, 20,  254, 22])

sk: PrivateKey = AugSchemeMPL.key_gen(seed)
pk: G1Element = sk.get_g1()

message: bytes = bytes([1, 2, 3, 4, 5])
signatureAug: G2Element = AugSchemeMPL.sign(sk, message)
signaturePop: G2Element = PopSchemeMPL.sign(sk, message)

# Verify the signature
print(signatureAug)
print(signaturePop)
ok: bool = AugSchemeMPL.verify(pk, message, signatureAug)
assert ok