from blspy import (PrivateKey, Util, AugSchemeMPL, PopSchemeMPL,
                   G1Element, G2Element)
import time






# # Example seed, used to generate private key. Always use
# # a secure RNG with sufficient entropy to generate a seed (at least 32 bytes).
# seed: bytes = bytes([0,  50, 6,  244, 24,  199, 1,  25,  52,  88,  192,
#                         19, 18, 12, 89,  6,   220, 18, 102, 58,  209, 82,
#                         12, 62, 89, 110, 182, 9,   44, 20,  254, 22])
# sk1: PrivateKey = AugSchemeMPL.key_gen(seed)
# pk1: G1Element = sk1.get_g1()
# sk2: PrivateKey = AugSchemeMPL.key_gen(seed)
# pk2: G1Element = sk2.get_g1()
# sk3: PrivateKey = AugSchemeMPL.key_gen(seed)
# pk3: G1Element = sk3.get_g1()

# message: bytes = bytes([1, 2, 3, 4, 5])
# # If the same message is signed, you can use Proof of Posession (PopScheme) for efficiency
# # A proof of possession MUST be passed around with the PK to ensure security.
# pop_sig1: G2Element = PopSchemeMPL.sign(sk1, message)
# pop_sig2: G2Element = PopSchemeMPL.sign(sk2, message)
# pop_sig3: G2Element = PopSchemeMPL.sign(sk3, message)
# pop1: G2Element = PopSchemeMPL.pop_prove(sk1)
# pop2: G2Element = PopSchemeMPL.pop_prove(sk2)
# pop3: G2Element = PopSchemeMPL.pop_prove(sk3)

# ok = PopSchemeMPL.pop_verify(pk1, pop1)
# ok = PopSchemeMPL.pop_verify(pk2, pop2)
# ok = PopSchemeMPL.pop_verify(pk3, pop3)

# pop_sig_agg: G2Element = PopSchemeMPL.aggregate([pop_sig1, pop_sig2, pop_sig3])

# ok = PopSchemeMPL.fast_aggregate_verify([pk1, pk2, pk3], message, pop_sig_agg)

# # Aggregate public key, indistinguishable from a single public key
# pop_agg_pk: G1Element = pk1 + pk2 + pk3
# ok = PopSchemeMPL.verify(pop_agg_pk, message, pop_sig_agg)

# # Aggregate private keys
# pop_agg_sk: PrivateKey = PrivateKey.aggregate([sk1, sk2, sk3])
# ok = PopSchemeMPL.sign(pop_agg_sk, message) == pop_sig_agg
# assert ok