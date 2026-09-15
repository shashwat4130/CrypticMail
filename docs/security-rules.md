# CrypticMail Security Standards & Rules Specification (Step 4)

## 1. Overview & Forensic Philosophy

CrypticMail is a passive network forensic framework analyzing SMTP, IMAP, and POP3 communications.
Its deterministic security engine operates under strict evidentiary constraints:
1. **Passive Observation Only**: A PCAP records observed traffic; it does not actively probe the server.
2. **Defensible Claims**: Assertions must trace directly to standards (NIST SP 800-52r2, RFC 8446, RFC 8996, RFC 3207, RFC 8314, RFC 2595, RFC 5280).
3. **Absence of Proof is Not Proof of Malice**: Incomplete captures, missing extensions, or absent parameters must be classified as `UNKNOWN`, never synthesized into confirmed attacks or false negatives.

> **Note**: NIST SP 800-52 Rev. 2 is under review. It is referenced here as authoritative federal baseline guidance, but not as an unrevised modern terminus.

---

## 2. Evidence Confidence Model

Every evaluation condition produces findings associated with an explicit confidence level:
* **CONFIRMED_OBSERVED**: The parameter was directly parsed from unambiguous packet handshake or certificate fields.
* **INFERRED**: Derived from multiple correlated observations.
* **SUSPECTED**: Traffic shows anomalous or inconsistent state patterns suggesting an issue.
* **UNKNOWN**: Capture lacks the requisite frames to establish presence or absence.

---

## 3. Passive Forensics Limitations (What CrypticMail Cannot Claim)

To remain legally and technically defensible before evaluators and forensic analysts:
1. **No Proof of Active Exploitation**: Observing a vulnerable primitive (e.g., 3DES) proves the session is susceptible to SWEET32; it does not prove the session was decrypted or exploited.
2. **No Proof of Server-Wide Configuration**: Passive PCAPs only capture parameters negotiated for that specific connection. An unobserved cipher suite is not proven unsupported.
3. **No Definitive Live Revocation Proof**: A passive PCAP cannot determine if a certificate is currently revoked unless a cached OCSP Staple (`status_request`) or CRL distribution payload is captured in the stream.
4. **No Definitive MITM Accusation from Absent STARTTLS**: The absence of a STARTTLS advertisement may indicate a legacy server configuration rather than an active adversary stripping headers.
5. **No Domain Spoofing Accusation from HELO/EHLO Discrepancies**: In enterprise email, the HELO/EHLO greeting name often represents internal gateways or multi-tenant relays. Identity mismatch is evaluated strictly between TLS SNI and Certificate SANs.

---

## 4. Severity Policy Framework

Findings are assigned severity based on objective risk criteria:
* **CRITICAL**: Clear, present cryptographic compromise (NULL ciphers, SSL 2.0/3.0, RC4, RSA modulus < 2048 bits, MD5/SHA-1 signatures).
* **HIGH**: Formally deprecated protocols or primitives (TLS 1.0/1.1, 3DES, missing PFS, expired certificates).
* **MEDIUM**: Configurations vulnerable under specific conditions (TLS 1.2 CBC-mode, weak DH group < 2048-bit, self-signed certificates, SNI/SAN mismatches).
* **LOW**: Non-critical policy deviations or deprecated non-cryptographic extensions.
* **INFO**: Informational compliance notes (TLS 1.3 usage, acceptable TLS 1.2 AEAD deployments).

---

## 5. Security Rules Catalog

### Category 1: TLS Version Security

#### RULE-TLS-001: Obsolete SSL Protocol Negotiated
* **Category**: TLS_VERSION
* **Title**: Obsolete SSL Protocol Version (SSL 2.0 / SSL 3.0)
* **Required Evidence**: Handshake version field in ServerHello (0x0200 or 0x0300).
* **Detection Condition**: Negotiated protocol version is SSL 2.0 or SSL 3.0.
* **Reference Standard**: RFC 6176 / RFC 7568.
* **Severity**: CRITICAL
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Disable SSL 2.0 and SSL 3.0 across all mail listeners. Mandate TLS 1.2 or TLS 1.3.
* **Limitation**: Identifies negotiated session only; does not evaluate unexercised server fallback options.
* **Must NOT Claim**: Must not claim remote code execution occurred.

#### RULE-TLS-002: Deprecated TLS Protocol (TLS 1.0 / TLS 1.1)
* **Category**: TLS_VERSION
* **Title**: Deprecated TLS Protocol Version (TLS 1.0 / TLS 1.1)
* **Required Evidence**: Negotiated `server_hello.version` or `supported_versions` extension selecting 0x0301 or 0x0302.
* **Detection Condition**: Observed TLS version is TLS 1.0 or TLS 1.1.
* **Reference Standard**: RFC 8996, NIST SP 800-52r2.
* **Severity**: HIGH
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Enforce TLS 1.2 as minimum baseline; deploy TLS 1.3 per RFC 8446.
* **Limitation**: Observation proves negotiation, not that downgrade was maliciously induced.
* **Must NOT Claim**: Must not claim the session was decrypted or an active adversary was present.

#### RULE-TLS-003: Legacy Acceptable TLS 1.2 Baseline
* **Category**: TLS_VERSION
* **Title**: TLS 1.2 Protocol Negotiated
* **Required Evidence**: `server_hello.version` equal to 0x0303.
* **Detection Condition**: Observed TLS version is TLS 1.2.
* **Reference Standard**: RFC 5246, NIST SP 800-52r2.
* **Severity**: INFO
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Plan migration to TLS 1.3 for mandatory forward secrecy.
* **Limitation**: TLS 1.2 security is contingent on cipher suite and key exchange parameters.
* **Must NOT Claim**: Must not declare TLS 1.2 inherently insecure or fully hardened without evaluating ciphers and certificates.

#### RULE-TLS-004: Modern TLS 1.3 Deployment
* **Category**: TLS_VERSION
* **Title**: Modern TLS 1.3 Protocol Negotiated
* **Required Evidence**: `server_hello.supported_versions` extension equal to 0x0304.
* **Detection Condition**: Observed TLS version is TLS 1.3.
* **Reference Standard**: RFC 8446.
* **Severity**: INFO
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Maintain configuration.
* **Limitation**: Does not inspect server private key handling.
* **Must NOT Claim**: Must not claim entire mail architecture is impervious to other network or application threats.

---

### Category 2: Cipher Suite Security

#### RULE-CIPHER-001: Plaintext / NULL Cipher Suite
* **Category**: CIPHER_SUITE
* **Title**: Insecure NULL Encryption Cipher Suite
* **Required Evidence**: Negotiated cipher suite identifier matching `*_WITH_NULL_*`.
* **Detection Condition**: Selected cipher suite provides zero payload encryption.
* **Reference Standard**: RFC 5246, NIST SP 800-52r2.
* **Severity**: CRITICAL
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Purge all NULL cipher suites from server configuration.
* **Limitation**: Relies on accurate IANA cipher suite mapping.
* **Must NOT Claim**: Must not claim data was intercepted by a third party.

#### RULE-CIPHER-002: Broken Stream Cipher (RC4)
* **Category**: CIPHER_SUITE
* **Title**: Broken RC4 Stream Cipher Negotiated
* **Required Evidence**: Negotiated cipher suite containing `RC4`.
* **Detection Condition**: Selected cipher suite uses the RC4 algorithm.
* **Reference Standard**: RFC 7465.
* **Severity**: CRITICAL
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Disable all RC4 suites across all endpoints.
* **Limitation**: Identifies protocol negotiation; does not compute exact ciphertext entropy.
* **Must NOT Claim**: Must not assert keystream bias was actively exploited in this flow.

#### RULE-CIPHER-003: 64-bit Block Cipher (SWEET32 / 3DES)
* **Category**: CIPHER_SUITE
* **Title**: Vulnerable 64-bit Block Cipher (3DES / Triple-DES)
* **Required Evidence**: Negotiated cipher suite containing `3DES` or `DES`.
* **Detection Condition**: Negotiated cipher suite employs a 64-bit block size.
* **Reference Standard**: RFC 8996, CVE-2016-2183, NIST SP 800-52r2.
* **Severity**: HIGH
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Replace 3DES with AES-128-GCM, AES-256-GCM, or ChaCha20-Poly1305.
* **Limitation**: Exploitation requires capturing tens of gigabytes within a single TLS session context.
* **Must NOT Claim**: Must not claim a short email session was cracked via SWEET32 collisions.

#### RULE-CIPHER-004: Legacy CBC-Mode Symmetric Ciphers
* **Category**: CIPHER_SUITE
* **Title**: CBC-Mode Cipher Suite in TLS 1.2
* **Required Evidence**: TLS 1.2 session negotiating cipher suite ending in `_CBC_SHA` or `_CBC_SHA256/384`.
* **Detection Condition**: Session uses TLS 1.2 with CBC mode encryption.
* **Reference Standard**: RFC 5246, NIST SP 800-52r2.
* **Severity**: MEDIUM
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Migrate to Authenticated Encryption with Associated Data (AEAD) ciphers.
* **Limitation**: Passive capture cannot determine whether the host implementation possesses side-channel timing mitigations.
* **Must NOT Claim**: Must not claim the server is vulnerable to padding oracle exploitation without active timing verification.

---

### Category 3: Key Exchange & Perfect Forward Secrecy

#### RULE-KEX-001: Missing Perfect Forward Secrecy (Static RSA)
* **Category**: KEY_EXCHANGE
* **Title**: Static RSA Key Exchange (Missing Forward Secrecy)
* **Required Evidence**: Negotiated cipher suite commencing with `TLS_RSA_WITH_*`.
* **Detection Condition**: Session employs static RSA key transport.
* **Reference Standard**: NIST SP 800-52r2, RFC 8446.
* **Severity**: HIGH
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Mandate Ephemeral Diffie-Hellman (ECDHE or DHE).
* **Limitation**: True solely for the observed session.
* **Must NOT Claim**: Must not claim historical traffic has been decrypted.

#### RULE-KEX-002: Insufficient Finite-Field Diffie-Hellman Parameter Length (Logjam)
* **Category**: KEY_EXCHANGE
* **Title**: Weak Diffie-Hellman Modulus (< 2048 bits)
* **Required Evidence**: `ServerKeyExchange` record containing DH modulus parameter p with bit length < 2048.
* **Detection Condition**: Observed DH modulus is smaller than 2048 bits.
* **Reference Standard**: NIST SP 800-52r2, RFC 7919, CVE-2015-4000.
* **Severity**: HIGH
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Configure custom DH parameters >= 2048 bits or transition to ECDHE.
* **Limitation**: Applicable only when DHE is negotiated and parameters are visible in TLS <= 1.2.
* **Must NOT Claim**: Must not infer DH modulus size from cipher name alone without inspecting raw handshake parameters.

#### RULE-KEX-003: Unapproved or Deprecated Elliptic Curve
* **Category**: KEY_EXCHANGE
* **Title**: Deprecated or Weak Named Curve
* **Required Evidence**: Named Curve ID extracted from Supported Groups or KeyShare extension.
* **Detection Condition**: Negotiated curve is not in NIST SP 800-52r2 approved list.
* **Reference Standard**: NIST SP 800-52r2, RFC 8446.
* **Severity**: MEDIUM
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Restrict named curve support to X25519 and standard NIST curves.
* **Limitation**: Dependent on client-server extension negotiation visibility.
* **Must NOT Claim**: Must not claim the elliptic curve contains an intentional mathematical backdoor.

---

### Category 4: Certificate Security

#### RULE-CERT-001: Expired Server Certificate
* **Category**: CERTIFICATE_VALIDITY
* **Title**: Expired X.509 Server Certificate
* **Required Evidence**: Certificate NotAfter timestamp precedes the session capture UTC reference timestamp.
* **Detection Condition**: `session.start_time > cert.not_after`.
* **Reference Standard**: RFC 5280.
* **Severity**: HIGH
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Renew and deploy a valid certificate immediately.
* **Limitation**: Evaluated strictly relative to the timestamp of packet capture ingestion.
* **Must NOT Claim**: Must not claim the certificate was expired at issuance.

#### RULE-CERT-002: Not-Yet-Valid Server Certificate
* **Category**: CERTIFICATE_VALIDITY
* **Title**: Certificate Not Yet Valid
* **Required Evidence**: Certificate NotBefore timestamp is in the future relative to the session capture timestamp.
* **Detection Condition**: `session.start_time < cert.not_before`.
* **Reference Standard**: RFC 5280.
* **Severity**: MEDIUM
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Synchronize system clocks via NTP and verify certificate activation dates.
* **Limitation**: May result from capture clock skew on the monitoring sensor.
* **Must NOT Claim**: Must not claim malicious spoofing if clock desynchronization is plausible.

#### RULE-CERT-003: Insufficient Public Key Strength (RSA < 2048 bits)
* **Category**: CERTIFICATE_VALIDITY
* **Title**: Insufficient RSA Public Key Length (< 2048 bits)
* **Required Evidence**: Certificate `SubjectPublicKeyInfo` containing an RSA modulus length < 2048 bits.
* **Detection Condition**: Observed RSA key length < 2048 bits.
* **Reference Standard**: NIST SP 800-52r2, RFC 5280.
* **Severity**: CRITICAL
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Re-issue certificate using RSA >= 2048 bits or ECDSA >= 256 bits.
* **Limitation**: Applies only to public key algorithms with modulus definitions (RSA/DSA).
* **Must NOT Claim**: Must not assert the private key has been factored.

#### RULE-CERT-004: Deprecated Certificate Signature Digest (MD5 / SHA-1)
* **Category**: CERTIFICATE_VALIDITY
* **Title**: Weak Signature Algorithm in Certificate (MD5 / SHA-1)
* **Required Evidence**: Certificate `signatureAlgorithm` ASN.1 field indicating MD5 or SHA-1.
* **Detection Condition**: Certificate signed with MD5 or SHA-1 digest.
* **Reference Standard**: RFC 5280, NIST SP 800-52r2, RFC 9155.
* **Severity**: CRITICAL
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Replace certificate with one signed via SHA-256 or stronger digest.
* **Limitation**: Applies to end-entity and intermediate certs, not local trust-store root anchors.
* **Must NOT Claim**: Must not declare a root CA invalid solely due to a SHA-1 self-signature.

---

### Category 5: Certificate Trust & PKI

#### RULE-PKI-001: Self-Signed End-Entity Certificate
* **Category**: CERTIFICATE_CHAIN
* **Title**: Self-Signed Server Certificate
* **Required Evidence**: Subject DN equals Issuer DN, signature self-validates, and cert is absent from root CA store.
* **Detection Condition**: `is_self_signed == TRUE` and certificate is an end-entity certificate.
* **Reference Standard**: RFC 5280.
* **Severity**: MEDIUM
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Deploy a certificate issued by a recognized public or enterprise CA.
* **Limitation**: Internal networks or test harnesses may legitimately utilize self-signed certs.
* **Must NOT Claim**: Must not claim Subject == Issuer alone proves self-signing without verifying cryptographic signature self-consistency.

#### RULE-PKI-002: Incomplete Certificate Chain / Untrusted Root
* **Category**: CERTIFICATE_CHAIN
* **Title**: Certificate Chain Path Validation Failed
* **Required Evidence**: Inability to construct a valid certificate chain path to a trusted root CA bundle.
* **Detection Condition**: `chain_valid == FALSE`.
* **Reference Standard**: RFC 5280.
* **Severity**: HIGH
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Ensure the mail server bundles all required intermediate CA certificates.
* **Limitation**: Offline forensic analyzers validate against a local CA bundle.
* **Must NOT Claim**: Must not claim a certificate is fraudulent without accounting for private enterprise trust anchors.

---

### Category 6: STARTTLS Security

#### RULE-STARTTLS-001: Cleartext Transmission of Mail Protocol
* **Category**: STARTTLS_SECURITY
* **Title**: Unencrypted Mail Session (No TLS / No STARTTLS)
* **Required Evidence**: Complete SMTP, IMAP, or POP3 conversation without implicit TLS and without successful STARTTLS transition.
* **Detection Condition**: Mail session terminates or exchanges application data in cleartext.
* **Reference Standard**: RFC 8314.
* **Severity**: CRITICAL
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Configure mandatory TLS (implicit TLS or mandatory STARTTLS upgrade).
* **Limitation**: Assumes captured packets reflect the entire connection lifetime.
* **Must NOT Claim**: Must not claim credentials were stolen without observing an unencrypted AUTH command.

#### RULE-STARTTLS-002: Suspicious STARTTLS Downgrade / Stripping
* **Category**: STARTTLS_SECURITY
* **Title**: Suspected STARTTLS Stripping / Downgrade
* **Required Evidence**: Server banner/EHLO advertises `250-STARTTLS`, followed by client reverting to cleartext without attempting STARTTLS.
* **Detection Condition**: `starttls_state == DOWNGRADE_SUSPECTED`.
* **Reference Standard**: RFC 3207, RFC 8314.
* **Severity**: HIGH
* **Confidence**: SUSPECTED
* **Recommendation**: Enforce mandatory STARTTLS or switch to implicit TLS (Port 465).
* **Limitation**: Misconfigured client software may ignore STARTTLS advertisements without active adversary interference.
* **Must NOT Claim**: Must NOT state that an active Man-in-the-Middle attack is proven. The finding must be phrased as "Suspected Downgrade / Inconsistent Protocol Transition".

---

### Category 7: Email Transport Architecture

#### RULE-EMAIL-001: Deprecated Cleartext Submission / Access Port
* **Category**: PROTOCOL_FLOW
* **Title**: Insecure Cleartext Email Access Port Observed
* **Required Evidence**: Session on Port 110 (POP3) or Port 143 (IMAP) without successful TLS upgrade.
* **Detection Condition**: Connection observed on legacy plaintext access ports without encryption.
* **Reference Standard**: RFC 8314.
* **Severity**: HIGH
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Migrate users to Port 993 (IMAPS) and Port 995 (POP3S) using implicit TLS.
* **Limitation**: Does not evaluate firewall-restricted internal management networks.
* **Must NOT Claim**: Must not conflate SMTP relay (Port 25) with submission/access (Ports 587/465/993/995).

---

### Category 8: Identity & Hostname Alignment

#### RULE-IDENTITY-001: TLS SNI Does Not Match Certificate SAN
* **Category**: IDENTITY_ALIGNMENT
* **Title**: Certificate Identity (SAN) Does Not Match Observed TLS SNI
* **Required Evidence**: ClientHello presents server_name extension, and the value is absent from certificate SubjectAlternativeName entries.
* **Detection Condition**: `sni_matches_san == FALSE`.
* **Reference Standard**: RFC 6066, RFC 5280.
* **Severity**: MEDIUM
* **Confidence**: CONFIRMED_OBSERVED
* **Recommendation**: Update server certificate to include the connecting hostname in Subject Alternative Names.
* **Limitation**: Many mail servers serve multiple domains using a single shared relay hostname.
* **Must NOT Claim**: Must NOT claim the certificate is spoofed or an attack occurred.

---

### Category 9: Protocol Anomalies & Downgrade Behavior

#### RULE-ANOMALY-001: Handshake Version / Extension Inconsistency
* **Category**: PROTOCOL_FLOW
* **Title**: Inconsistent TLS Record and Handshake Version
* **Required Evidence**: `record_layer.version` indicates TLS 1.0 while `handshake.version` indicates TLS 1.2 without appropriate client greeting structure.
* **Detection Condition**: Contradictory version markers across TLS boundaries.
* **Reference Standard**: RFC 8446.
* **Severity**: LOW
* **Confidence**: SUSPECTED
* **Recommendation**: Audit network paths for legacy TLS inspection proxies.
* **Limitation**: Compatibility shims in TLS 1.3 intentionally use 0x0303 record versions.
* **Must NOT Claim**: Must not classify standardized TLS 1.3 middlebox compatibility mechanisms as malicious tampering.