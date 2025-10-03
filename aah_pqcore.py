#!/usr/bin/env python3
"""
AAH PQ Core - Pluggable Post-Quantum Primitives

Provides a clean interface for:
- KEM (encapsulate/decapsulate)
- Signature (sign/verify)
- AEAD (ChaCha20-Poly1305) with HKDF-SHA256

Backends:
- oqs: Uses the 'oqs' package for Kyber/Dilithium (default)
- stub: Minimal placeholder backend (NOT secure; for testing when oqs is unavailable)

This isolates crypto so the GUI and higher layers don't depend on 3rd-party libs directly.
We can later replace 'oqs' backend with a self-contained lattice implementation.
"""

import os
import json
import base64
from typing import Tuple, Optional

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives import hashes as _hashes

try:
    import oqs  # type: ignore
    OQS_AVAILABLE = True
    OQS_API_OK = hasattr(oqs, 'KeyEncapsulation') and hasattr(oqs, 'Signature')
except Exception:
    oqs = None  # type: ignore
    OQS_AVAILABLE = False
    OQS_API_OK = False


class AEAD:
    """AEAD utility using ChaCha20-Poly1305 with HKDF-SHA256."""

    @staticmethod
    def kdf32(shared_secret: bytes) -> bytes:
        hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'aah-pqcore')
        return hkdf.derive(shared_secret)

    @staticmethod
    def encrypt(key: bytes, plaintext: bytes) -> Tuple[bytes, bytes]:
        aead = ChaCha20Poly1305(key)
        nonce = os.urandom(12)
        ct = aead.encrypt(nonce, plaintext, None)
        return nonce, ct

    @staticmethod
    def decrypt(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
        aead = ChaCha20Poly1305(key)
        return aead.decrypt(nonce, ciphertext, None)


class Backend:
    """Abstract backend for PQC primitives."""

    def kem_generate(self) -> Tuple[bytes, bytes]:
        raise NotImplementedError

    def kem_encap(self, public_key: bytes) -> Tuple[bytes, bytes]:
        raise NotImplementedError

    def kem_decap(self, secret_key: bytes, ciphertext: bytes) -> bytes:
        raise NotImplementedError

    def sig_generate(self) -> Tuple[bytes, bytes]:
        raise NotImplementedError

    def sign(self, secret_key: bytes, message: bytes) -> bytes:
        raise NotImplementedError

    def verify(self, public_key: bytes, message: bytes, signature: bytes) -> bool:
        raise NotImplementedError


class OQSBackend(Backend):
    """Kyber/Dilithium via oqs."""

    def __init__(self, kem: str = 'Kyber1024', sig: str = 'Dilithium5'):
        if not OQS_AVAILABLE:
            raise RuntimeError("oqs not available")
        self.kem = kem
        self.sig = sig

    def kem_generate(self) -> Tuple[bytes, bytes]:
        with oqs.KeyEncapsulation(self.kem) as k:
            pk = k.generate_keypair()
            sk = k.export_secret_key()
        return sk, pk

    def kem_encap(self, public_key: bytes) -> Tuple[bytes, bytes]:
        with oqs.KeyEncapsulation(self.kem) as k:
            ct, ss = k.encap_secret(public_key)
        return ct, ss

    def kem_decap(self, secret_key: bytes, ciphertext: bytes) -> bytes:
        with oqs.KeyEncapsulation(self.kem) as k:
            k.import_secret_key(secret_key)
            ss = k.decap_secret(ciphertext)
        return ss

    def sig_generate(self) -> Tuple[bytes, bytes]:
        with oqs.Signature(self.sig) as s:
            pk = s.generate_keypair()
            sk = s.export_secret_key()
        return sk, pk

    def sign(self, secret_key: bytes, message: bytes) -> bytes:
        with oqs.Signature(self.sig) as s:
            s.import_secret_key(secret_key)
            return s.sign(message)

    def verify(self, public_key: bytes, message: bytes, signature: bytes) -> bool:
        with oqs.Signature(self.sig) as s:
            return s.verify(message, signature, public_key)


class StubBackend(Backend):
    """Insecure stub backend; placeholder for development only."""

    def kem_generate(self) -> Tuple[bytes, bytes]:
        sk = os.urandom(64)
        pk = os.urandom(64)
        return sk, pk

    def kem_encap(self, public_key: bytes) -> Tuple[bytes, bytes]:
        ct = os.urandom(128)
        ss = os.urandom(32)
        return ct, ss

    def kem_decap(self, secret_key: bytes, ciphertext: bytes) -> bytes:
        return os.urandom(32)

    def sig_generate(self) -> Tuple[bytes, bytes]:
        sk = os.urandom(64)
        pk = os.urandom(64)
        return sk, pk

    def sign(self, secret_key: bytes, message: bytes) -> bytes:
        return os.urandom(64)

    def verify(self, public_key: bytes, message: bytes, signature: bytes) -> bool:
        return False


class NativeBackend(Backend):
    """
    Experimental native lattice backend (scaffold).

    WARNING: This is NOT production-ready crypto. It exists to provide a
    self-contained structure for an RLWE-style KEM and a lattice signature
    (e.g., Dilithium-like) implementation. The math-heavy pieces are
    deliberately left unimplemented here and should be filled in by a proper
    cryptographic implementation and review.
    """

    def __init__(self, security_level: str = 'max'):
        self.security_level = security_level

    # --- Key Encapsulation (KEM) placeholders ---
    def kem_generate(self) -> Tuple[bytes, bytes]:
        # AAH-KEM(v0) prototype (for plumbing/tests):
        # secret key: 32 random bytes; public key: SHA3-256(secret)
        sk = os.urandom(32)
        digest = _hashes.Hash(_hashes.SHA3_256())
        digest.update(sk)
        pk = digest.finalize()
        return sk, pk

    def kem_encap(self, public_key: bytes) -> Tuple[bytes, bytes]:
        # Generate ephemeral r and derive shared secret
        r = os.urandom(32)
        # ss = HKDF(public||r)
        hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'aah-native-kem')
        ss = hkdf.derive(public_key + r)
        # Encrypt r with public key (simple XOR with hash of public)
        digest = _hashes.Hash(_hashes.SHA3_256())
        digest.update(public_key)
        mask = digest.finalize()
        ct = bytes(x ^ y for x, y in zip(r, mask))
        return ct, ss

    def kem_decap(self, secret_key: bytes, ciphertext: bytes) -> bytes:
        # Recompute public from secret to unmask r, then derive ss
        digest = _hashes.Hash(_hashes.SHA3_256())
        digest.update(secret_key)
        public_key = digest.finalize()
        # Unmask r using the same mask
        digest = _hashes.Hash(_hashes.SHA3_256())
        digest.update(public_key)
        mask = digest.finalize()
        r = bytes(x ^ y for x, y in zip(ciphertext, mask))
        # Derive same shared secret
        hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'aah-native-kem')
        ss = hkdf.derive(public_key + r)
        return ss

    # --- Signature placeholders ---
    def sig_generate(self) -> Tuple[bytes, bytes]:
        raise NotImplementedError("Native signature not implemented yet")

    def sign(self, secret_key: bytes, message: bytes) -> bytes:
        raise NotImplementedError("Native signing not implemented yet")

    def verify(self, public_key: bytes, message: bytes, signature: bytes) -> bool:
        raise NotImplementedError("Native verification not implemented yet")


class PQCore:
    """High-level PQ operations using selected backend and AEAD."""

    def __init__(self, kem: str = 'Kyber1024', sig: str = 'Dilithium5', prefer_oqs: bool = True, use_native: bool = False):
        self.kem_name = kem
        self.sig_name = sig
        # Backend selection priority: native -> oqs -> stub
        if use_native:
            self.backend: Backend = NativeBackend()
        elif prefer_oqs and OQS_AVAILABLE and OQS_API_OK:
            self.backend: Backend = OQSBackend(kem, sig)
        else:
            self.backend = StubBackend()

    # Key management
    def generate_encryption_keys(self) -> Tuple[str, str]:
        sk, pk = self.backend.kem_generate()
        return base64.b64encode(sk).decode(), base64.b64encode(pk).decode()

    def generate_signature_keys(self) -> Tuple[str, str]:
        sk, pk = self.backend.sig_generate()
        return base64.b64encode(sk).decode(), base64.b64encode(pk).decode()

    # Messaging
    def encrypt_for_pk(self, message: str, kem_public_key_b64: str) -> str:
        pk = base64.b64decode(kem_public_key_b64)
        ct, ss = self.backend.kem_encap(pk)
        key = AEAD.kdf32(ss)
        nonce, c = AEAD.encrypt(key, message.encode('utf-8'))
        
        # Create compact format: ct + nonce + ciphertext
        compact_data = ct + nonce + c
        return base64.b64encode(compact_data).decode()

    def decrypt_with_sk(self, encrypted_data: str, kem_secret_key_b64: str) -> str:
        # Try to parse as JSON envelope first (backward compatibility)
        try:
            env = json.loads(encrypted_data)
            ct = base64.b64decode(env['ct'])
            nonce = base64.b64decode(env['nonce'])
            ciphertext = base64.b64decode(env['ciphertext'])
        except:
            # If not JSON, treat as compact format: ct + nonce + ciphertext
            compact_data = base64.b64decode(encrypted_data)
            # Split the data: ct (32 bytes) + nonce (12 bytes) + ciphertext (rest)
            ct = compact_data[:32]
            nonce = compact_data[32:44]
            ciphertext = compact_data[44:]
        
        sk = base64.b64decode(kem_secret_key_b64)
        ss = self.backend.kem_decap(sk, ct)
        key = AEAD.kdf32(ss)
        pt = AEAD.decrypt(key, nonce, ciphertext)
        return pt.decode('utf-8')

    # Signatures
    def sign(self, sig_secret_key_b64: str, message: str) -> str:
        sk = base64.b64decode(sig_secret_key_b64)
        sig = self.backend.sign(sk, message.encode('utf-8'))
        return base64.b64encode(sig).decode()

    def verify(self, sig_public_key_b64: str, message: str, signature_b64: str) -> bool:
        pk = base64.b64decode(sig_public_key_b64)
        sig = base64.b64decode(signature_b64)
        return self.backend.verify(pk, message.encode('utf-8'), sig)

