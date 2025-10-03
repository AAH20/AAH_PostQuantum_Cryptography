# AAH Post-Quantum Cryptography

**Superior Post-Quantum Asymmetric Cryptography Framework**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Post-Quantum](https://img.shields.io/badge/Post--Quantum-Cryptography-green.svg)](https://csrc.nist.gov/Projects/post-quantum-cryptography)

## 🎯 **Overview**

AAH Post-Quantum Cryptography is a comprehensive, self-contained framework for post-quantum cryptographic operations. Built with native Python implementations and designed to exceed intelligence agency capabilities, this framework provides quantum-resistant security for the next generation of applications.

## 🔬 **Key Features**

### **Core Cryptography**
- **Native Post-Quantum Implementation**: Pure Python, no external dependencies
- **Lattice-Based Security**: RLWE (Ring Learning With Errors) foundation
- **Quantum-Resistant**: Designed to withstand quantum computer attacks
- **Multiple Algorithms**: Kyber1024, Dilithium5, and custom implementations

### **Security Capabilities**
- **Key Encapsulation Mechanism (KEM)**: Secure key exchange
- **Digital Signatures**: Lattice-based signature schemes
- **AEAD Encryption**: ChaCha20-Poly1305 for symmetric operations
- **Key Derivation**: HKDF-SHA256 for secure key expansion
- **Quantum Obfuscation**: Advanced code protection techniques

### **User Interface**
- **Cross-Platform GUI**: Works on Windows, macOS, and Linux
- **Intuitive Design**: Easy-to-use interface for all operations
- **Contact Management**: Secure public key sharing
- **Real-time Operations**: Instant encryption/decryption

## 🚀 **Quick Start**

### **Installation**

```bash
# Clone the repository
git clone https://github.com/AAH20/AAH_PostQuantum_Cryptography.git
cd AAH_PostQuantum_Cryptography

# Create virtual environment
python3 -m venv aah_security_env
source aah_security_env/bin/activate  # On Windows: aah_security_env\Scripts\activate

# Install dependencies
pip install -r requirements_aah_security.txt

# Run the application
python aah_security_gui.py
```

### **Basic Usage**

```python
from aah_pqcore import PQCore

# Initialize with native backend
pq = PQCore(use_native=True)

# Generate encryption keys
private_key, public_key = pq.generate_encryption_keys()

# Encrypt message
encrypted = pq.encrypt_for_pk("Hello World!", public_key)

# Decrypt message
decrypted = pq.decrypt_with_sk(encrypted, private_key)
print(decrypted)  # "Hello World!"
```

## 📁 **Project Structure**

```
AAH_PostQuantum_Cryptography/
├── aah_security_gui.py          # Main GUI application
├── aah_pqcore.py               # Post-quantum cryptography core
├── aah_pqmath.py               # Mathematical primitives
├── aah_quantum_obfuscation.py  # Code obfuscation system
├── requirements_aah_security.txt # Dependencies
├── LICENSE                     # Apache 2.0 License
└── README.md                   # This file
```

## 🔑 **Key Types**

### **Encryption Keys**
- **Purpose**: Confidentiality and secure communication
- **Algorithm**: Native RLWE-based KEM + ChaCha20-Poly1305 AEAD
- **Usage**: Encrypt messages that only the private key holder can decrypt

### **Signature Keys**
- **Purpose**: Authentication and message integrity
- **Algorithm**: Lattice-based digital signatures
- **Usage**: Sign messages to prove authenticity and prevent tampering

### **Master Keys**
- **Purpose**: Root authority and key management
- **Usage**: Authorize other keys, manage key lifecycles
- **Security**: Store offline when possible, highest privilege level

## 🔐 **Security Features**

### **Post-Quantum Cryptography**
- **Native Implementation**: Pure Python, no external dependencies
- **Lattice-Based**: RLWE foundation for quantum resistance
- **Compact Format**: Single Base64 string for encrypted data
- **Forward Secrecy**: Ephemeral keys for each encryption

### **Cryptographic Strength**
- **Key Size**: 32-byte secret keys with SHA3-256 derived public keys
- **AEAD Encryption**: ChaCha20-Poly1305 for authenticated encryption
- **Key Derivation**: HKDF-SHA256 for secure key expansion
- **Random Generation**: Cryptographically secure random number generation

## 🛠️ **Development**

### **API Usage**

```python
from aah_pqcore import PQCore

# Initialize with different backends
pq_oqs = PQCore(prefer_oqs=True, use_native=False)  # OQS library
pq_native = PQCore(use_native=True)                 # Native implementation

# Generate different key types
enc_sk, enc_pk = pq.generate_encryption_keys()
sig_sk, sig_pk = pq.generate_signature_keys()

# Encrypt/Decrypt
encrypted = pq.encrypt_for_pk("Message", enc_pk)
decrypted = pq.decrypt_with_sk(encrypted, enc_sk)

# Sign/Verify
signature = pq.sign(sig_sk, "Message")
verified = pq.verify(sig_pk, "Message", signature)
```

### **Integration Examples**

- **Chat Applications**: Secure messaging with post-quantum crypto
- **File Encryption**: Protect sensitive documents and data
- **API Security**: Secure communication between services
- **IoT Devices**: Lightweight crypto for embedded systems

## 📊 **Performance**

- **Lightweight**: Minimal memory footprint
- **Fast Operations**: Optimized for real-time encryption/decryption
- **Scalable**: Efficient key management for multiple users
- **Portable**: Single-file deployment possible

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Development Setup**

```bash
# Fork the repository
git clone https://github.com/yourusername/AAH_PostQuantum_Cryptography.git

# Install development dependencies
pip install -r requirements_aah_security.txt
pip install pytest black flake8

# Run tests
pytest

# Format code
black .

# Lint code
flake8 .
```

## 📄 **License**

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🔬 **Patent Information**

This software is protected by patents owned by Ahmed Hassan (A2Z SOC). The Apache 2.0 license includes a patent grant that allows use of the patented technology under the terms of the license.

## 📞 **Support**

- **GitHub Issues**: [Report bugs and request features](https://github.com/AAH20/AAH_PostQuantum_Cryptography/issues)
- **Documentation**: Comprehensive in-code documentation
- **Community**: Join discussions in GitHub discussions

## 🏆 **Acknowledgments**

- **NIST**: For post-quantum cryptography standards
- **Open Quantum Safe**: For reference implementations
- **Cryptography Community**: For ongoing research and development

---

**AAH Post-Quantum Cryptography**  
*Superior Security for the Quantum Era*

**Author**: Ahmed Hassan (A2Z SOC)  
**Version**: 2.0.0  
**Date**: January 2025