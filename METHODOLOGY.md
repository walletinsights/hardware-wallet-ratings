# Rating methodology

Every model is scored out of 100. Inputs are verified specifications;
an unknown value earns no points. Full explanation with examples:
https://walletinsights.io/en/methodology/

## Overall

```
overall = security × 0.30 + recovery × 0.20 + usability × 0.20
        + ecosystem × 0.15 + privacy × 0.15
if security < 50: overall × 0.8
```

Rounded to an integer. Each category is capped to 0–100.

## Security (30%)

| Factor | Points |
|---|---:|
| Secure element | 18 |
| Secure element certification: EAL6+ / EAL5+ / EAL4+ | 12 / 8 / 4 |
| Open-source firmware | 8 |
| Non-extractable keys | 12 |
| Encrypted communication with the host | 7 |
| Anti-klepto protocol | 8 |
| Firmware attestation | 7 |
| Published third-party audit | 8 |
| Access code | 3 |
| PIN: auto-wipe / randomized keypad / attempt limit | 3 / 3 / 2 |
| Firmware downgrade protection / rollback prevention | 4 / 4 |
| Supply-chain mitigation / tamper-evident design | 3 / 3 |
| Reproducible builds | 4 |
| Secure boot | 3 |

Caps: without a secure element the score is at most 75; without a secure
element and without non-extractable keys, at most 60.

## Recovery (20%)

| Factor | Points |
|---|---:|
| Seed protocol: SLIP-39 / BIP-39 / other / custom or none | 25 / 20 / 15 / 12 |
| Shamir secret sharing | 8 |
| Passphrase on a BIP-39 seed (bonus) | 4 |
| Seedless design with multi-card backup (bonus) | 8 |
| Seedless design with multisig key replacement (bonus) | 8 |
| Seed length: 24+ / 20+ / 12+ words | 6 / 5 / 3 |
| Multi-card backup | 12 |
| Multisig key replacement | 12 |
| Passphrase | 8 |
| BIP-85 | 8 |
| Recovery with an access code | 4 |
| Backup ease (editorial, 1–5) | × 4, max 20 |
| Hidden wallets via passphrase | 4 |
| Social recovery | 3 |
| Vendor cloud backup on by default without opt-in | −3 |

## Usability (20%)

| Factor | Points |
|---|---:|
| Setup ease (editorial, 1–5) | × 4 |
| Interface quality (editorial, 1–5) | × 4 |
| Learning curve (editorial, 1–5, lower is easier) | (6 − score) × 4 |
| Wireless without USB / wireless and USB | 12 / 7 |
| Recipient and amount verified on the device screen | 5 |
| Clear signing: token approvals and EIP-712 typed data decoded on the device | 5 |
| Configuration time: ≤ 5 min / ≤ 15 min | 10 / 5 |
| Interface languages: 10+ / 4+ / 1+ | 8 / 5 / 2 |

Bitcoin-only devices earn the clear-signing points by definition (no token
approvals or typed data to decode).

## Ecosystem (15%)

| Factor | Points |
|---|---:|
| Unified accounts | 15 |
| Exchange integration | 15 |
| Networks: 21+ / 11+ / 6+ / 3+ | 20 / 15 / 10 / 5 |
| Desktop platforms: 3 / 2 / 1 | 10 / 8 / 5 |
| Mobile platforms: 2 / 1 | 10 / 6 |
| WalletConnect | 8 |
| Own full node | 8 |
| Smart-contract interaction | 5 |
| Coin control | 4 |
| Cold staking | 4 |
| Multisig: advanced / basic | 5 / 3 |

## Privacy (15%)

| Factor | Points |
|---|---:|
| Tor support | 15 |
| Open-source firmware | 10 |
| Encrypted communication | 10 |
| No Bluetooth and no NFC / NFC only | 8 / 4 |
| Own full node | 8 |
| No account registration | 12 |
| Works fully offline | 6 |
| CoinJoin | 8 |
| Avoids telemetry | 8 |
| Telemetry present: no opt-out / opt-out, on by default / off by default | −5 / −3 / −1 |
| Metadata protection | 5 |
| Leak resistance | 4 |
| Network fingerprinting resistance | 4 |
| Coin control | 4 |

An opt-out or an off-by-default state counts only when it is documented.

## Value (separate score)

Quality per dollar against a baseline of 65 points per $100:

```
ratio = overall / price_usd / 0.65
ratio ≥ 2      → 100
ratio ≥ 1      → 70 + (ratio − 1) × 30
ratio ≥ 0.5    → 40 + (ratio − 0.5) × 60
otherwise      → max(20, ratio × 80)
```

No price → 50. Value is not part of the overall rating.
