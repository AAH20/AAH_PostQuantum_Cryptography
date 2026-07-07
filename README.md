# AAH Post-Quantum Cryptography

A Python toolkit and desktop GUI for post-quantum key encapsulation and digital signatures, plus an experimental native lattice-scheme scaffold.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Post-Quantum](https://img.shields.io/badge/Post--Quantum-Cryptography-green.svg)](https://csrc.nist.gov/Projects/post-quantum-cryptography)

## What this actually is

This repo has two distinct parts with very different maturity levels. Read this section before using either.

### 1. OQS backend — real, standards-based, usable today

`PQCore` with the default `OQSBackend` wraps [liboqs](https://github.com/open-quantum-safe/liboqs) via the `oqs` Python bindings to perform ML-KEM (Kyber1024) key encapsulation and ML-DSA (Dilithium5) signatures, the actual NIST-standardized (FIPS 203 / FIPS 204) algorithms, plus ChaCha20-Poly1305 AEAD with HKDF-SHA256 key derivation. This path is only as secure as the upstream `liboqs` implementation it calls, this repo does not reimplement Kyber or Dilithium itself, it is a thin, convenience wrapper around an existing, audited library.

### 2. Native backend — experimental scaffold, not secure, do not use for real data

`NativeBackend` (`use_native=True`) is a from-scratch, dependency-free prototype. It is **not** Kyber, **not** Dilithium, and **not** RLWE-based despite earlier claims in this README. Specifically, as currently implemented:

- `aah_pqmath.py`'s NTT/INTT functions are unimplemented stubs (`ntt()` returns its input unchanged), and the noise samplers are placeholders. No lattice arithmetic is actually performed anywhere in the KEM path.
- `NativeBackend.kem_encap` derives its masking value as `SHA3-256(public_key)`. Because that mask depends only on the public key, anyone who has the public key and an intercepted ciphertext, not just the holder of the secret key, can recompute the same mask and recover the encapsulated value. That means the native KEM as written does **not** provide confidentiality against a passive observer holding only the public key. This is a real, exploitable break, not a hypothetical one.
- Native signature generation, signing, and verification are all unimplemented and raise `NotImplementedError`.

If you use this repo, use the OQS backend (the default). Do not use `use_native=True` for anything beyond studying or extending the scaffold itself.

### 3. Code obfuscation module

`aah_quantum_obfuscation.py` mixes several hash functions (SHA3-256, BLAKE2b) and random entropy sources to obscure strings and code. This is an obfuscation utility, not a cryptographic security boundary, and prior wording describing it as "quantum-resistant" overstated what hash-based obfuscation actually provides. Do not rely on it to protect secrets; use the AEAD/KEM path above for that.

## Why this repo exists

It's a working space for two things: a practical, correct-by-construction wrapper around the real NIST PQC algorithms (via liboqs) for anyone who wants Kyber/Dilithium in a Python project without hand-rolling the FFI themselves, and an open, honestly-labeled scaffold for eventually building a from-scratch RLWE implementation, useful for learning, not yet for production.

## Quick Start

### Installation

```bash
git clone https://github.com/AAH20/AAH_PostQuantum_Cryptography.git
cd AAH_PostQuantum_Cryptography

python3 -m venv aah_security_env
source aah_security_env/bin/activate  # On Windows: aah_security_env\Scripts\activate

pip install -r requirements_aah_security.txt
python aah_security_gui.py
```

### Basic usage (OQS backend, real Kyber1024 + Dilithium5)

```python
from aah_pqcore import PQCore

# Default backend: OQS (Kyber1024 KEM, Dilithium5 signatures)
pq = PQCore()

private_key, public_key = pq.generate_encryption_keys()
encrypted = pq.encrypt_for_pk("Hello World!", public_key)
decrypted = pq.decrypt_with_sk(encrypted, private_key)
print(decrypted)  # "Hello World!"

sig_sk, sig_pk = pq.generate_signature_keys()
signature = pq.sign(sig_sk, "Hello World!")
assert pq.verify(sig_pk, "Hello World!", signature)
```

## Project structure

```
AAH_PostQuantum_Cryptography/
├── aah_security_gui.py          # Desktop GUI application
├── aah_pqcore.py                # Backend selection: OQS (real) / Native (experimental) / Stub (test-only)
├── aah_pqmath.py                # Lattice math scaffold (NTT is currently a stub)
├── aah_quantum_obfuscation.py   # Hash-based code/string obfuscation utility
├── requirements_aah_security.txt
├── LICENSE                      # Apache 2.0
└── README.md
```

## Roadmap for the native backend

To make `NativeBackend` a real, reviewable RLWE implementation, the following need to happen before it should be trusted with any real data:

1. Implement actual NTT/INTT for the chosen ring and modulus.
2. Implement real centered binomial / discrete Gaussian noise sampling.
3. Replace the current public-key-derivable mask with an actual RLWE encryption scheme (e.g., following the Kyber/ML-KEM construction) so confidentiality depends on the hardness of Ring-LWE, not on keeping a hash secret.
4. Validate against the official NIST FIPS 203/204 test vectors, or clearly document that this is a distinct, non-standard scheme rather than compatible with Kyber/Dilithium.
5. Get independent cryptographic review before any claim of production-readiness.

Contributions on any of these are welcome.

## Contributing

Pull requests welcome, especially toward the native backend roadmap above. Please open an issue describing the change before large PRs.

```bash
pip install -r requirements_aah_security.txt
pip install pytest black flake8

pytest
black .
flake8 .
```

## License

Apache License 2.0, see [LICENSE](LICENSE).

## Acknowledgments

- [NIST](https://csrc.nist.gov/Projects/post-quantum-cryptography) for the post-quantum cryptography standards (FIPS 203, FIPS 204).
- [Open Quantum Safe](https://openquantumsafe.org/) for `liboqs` and the Kyber/Dilithium implementations this repo wraps by default.

---

Author: Ahmed Hassan (A2Z SOC)
Version: 2.0.1
