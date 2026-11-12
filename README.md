# WalletInsights hardware wallet data

Open data behind [WalletInsights](https://walletinsights.io): ratings of
hardware wallets computed with a published formula, the specifications they
are computed from, and a tracker of hardware wallet security incidents.

- **Ratings and specs** — 41 models, one row per model: overall rating
  (0–100), five category scores, value score, secure element, open-source
  scope, connectivity, recovery options, supported networks.
- **Security incidents** — 75 incidents: date, affected models, type,
  severity, attack vector, fix status, who disclosed it, reported losses,
  vendor statement and sources.
- **Formula** — [METHODOLOGY.md](METHODOLOGY.md) lists every factor and its
  points. The same formula produces every number in `data/`.

Licence: [CC BY 4.0](LICENSE). Archived on Zenodo:
[doi:10.5281/zenodo.24104206](https://doi.org/10.5281/zenodo.24104206)
(the DOI always resolves to the latest version).

## Files

| File | Contents |
|---|---|
| `data/wallets.csv`, `data/wallets.json` | Ratings and specifications. The JSON adds field descriptions and metadata. |
| `data/security-incidents.csv`, `data/security-incidents.json` | Security incident tracker. |
| `METHODOLOGY.md` | The rating formula, factor by factor. |
| `scripts/update.py` | Refreshes the snapshot from walletinsights.io and regenerates the table below. Standard library only. |
| `scripts/zenodo.py` | Archives a new Zenodo version when incidents change, 5+ overall ratings change, or anything changed and the last version is 30+ days old. |

The live versions are always at `https://walletinsights.io/data/<file>`;
this repository is refreshed weekly and keeps the history of every change
in git.

## Ratings

<!-- ratings:start -->
_Snapshot of 2026-11-12; discontinued models are in the data files but not in this table._

| # | Model | Overall | Security | Recovery | Usability | Ecosystem | Privacy | Price, USD |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | [Trezor Safe 7](https://walletinsights.io/en/hardware-wallets/trezor-safe-7/) | **85** | 93 | 66 | 84 | 100 | 79 | 249 |
| 2 | [Trezor Safe 5](https://walletinsights.io/en/hardware-wallets/trezor-safe-5/) | **80** | 86 | 70 | 68 | 98 | 77 | 129 |
| 3 | [BitBox02 Nova](https://walletinsights.io/en/hardware-wallets/bitbox02-nova/) | **78** | 91 | 66 | 67 | 80 | 80 | 196 |
| 4 | [OneKey Pro](https://walletinsights.io/en/hardware-wallets/onekey-pro/) | **78** | 90 | 75 | 82 | 100 | 29 | 278 |
| 5 | [OneKey Pro 2](https://walletinsights.io/en/hardware-wallets/onekey-pro-2/) | **77** | 88 | 75 | 82 | 100 | 29 | 299 |
| 6 | [OneKey Neo](https://walletinsights.io/en/hardware-wallets/onekey-neo/) | **76** | 85 | 75 | 82 | 100 | 29 | 179 |
| 7 | [Trezor Safe 3](https://walletinsights.io/en/hardware-wallets/trezor-safe-3/) | **76** | 83 | 70 | 57 | 98 | 73 | 59 |
| 8 | [BitBox02](https://walletinsights.io/en/hardware-wallets/bitbox02/) | **73** | 79 | 66 | 56 | 76 | 88 | 167 |
| 9 | [Keystone 3 Pro](https://walletinsights.io/en/hardware-wallets/keystone-pro-3/) | **72** | 82 | 71 | 67 | 60 | 69 | 149 |
| 10 | [Ledger Stax](https://walletinsights.io/en/hardware-wallets/ledger-stax/) | **70** | 83 | 58 | 66 | 100 | 33 | 399 |
| 11 | [Tangem Wallet (3 Cards)](https://walletinsights.io/en/hardware-wallets/tangem-wallet-3-cards/) | **70** | 78 | 74 | 86 | 77 | 21 | 69.9 |
| 12 | [Foundation Passport Prime](https://walletinsights.io/en/hardware-wallets/foundation-passport-prime/) | **69** | 67 | 80 | 74 | 52 | 67 | 349 |
| 13 | [Keycard Shell](https://walletinsights.io/en/hardware-wallets/keycard-shell/) | **69** | 87 | 71 | 60 | 42 | 66 | 129 |
| 14 | [OneKey Classic 1S](https://walletinsights.io/en/hardware-wallets/onekey-classic-1s/) | **69** | 88 | 54 | 63 | 98 | 29 | 99 |
| 15 | [Tangem Wallet (2 Cards)](https://walletinsights.io/en/hardware-wallets/tangem-wallet-2-cards/) | **69** | 78 | 70 | 86 | 77 | 21 | 54.9 |
| 16 | [Blockstream Jade Plus](https://walletinsights.io/en/hardware-wallets/blockstream-jade-plus/) | **68** | 71 | 66 | 60 | 67 | 77 | 149 |
| 17 | [Ledger Nano X](https://walletinsights.io/en/hardware-wallets/ledger-nano-x/) | **68** | 79 | 58 | 66 | 100 | 33 | 99 |
| 18 | [Blockstream Jade Core](https://walletinsights.io/en/hardware-wallets/blockstream-jade-core/) | **67** | 71 | 66 | 60 | 67 | 71 | 99 |
| 19 | [Ledger Nano Gen5](https://walletinsights.io/en/hardware-wallets/ledger-nano-gen5/) | **67** | 75 | 54 | 71 | 100 | 33 | 179 |
| 20 | [Ledger Nano S Plus](https://walletinsights.io/en/hardware-wallets/ledger-nano-s-plus/) | **67** | 75 | 58 | 59 | 98 | 41 | 69 |
| 21 | [OneKey Classic 1S Pure](https://walletinsights.io/en/hardware-wallets/onekey-classic-1s-pure/) | **67** | 88 | 58 | 56 | 90 | 29 | 79 |
| 22 | [Ledger Flex](https://walletinsights.io/en/hardware-wallets/ledger-flex/) | **66** | 75 | 54 | 62 | 100 | 33 | 249 |
| 23 | [SafePal S1](https://walletinsights.io/en/hardware-wallets/safepal-s1/) | **66** | 76 | 54 | 66 | 78 | 48 | 49.99 |
| 24 | [SafePal X1](https://walletinsights.io/en/hardware-wallets/safepal-x1/) | **66** | 81 | 58 | 66 | 78 | 36 | 69.99 |
| 25 | [Tangem Ring](https://walletinsights.io/en/hardware-wallets/tangem-wallet-ring/) | **66** | 78 | 70 | 70 | 77 | 21 | 160 |
| 26 | [Coinkite Coldcard Mk5](https://walletinsights.io/en/hardware-wallets/coinkite-coldcard-mk5/) | **65** | 77 | 74 | 52 | 37 | 71 | 219 |
| 27 | [Cryptnox Hardware Wallet](https://walletinsights.io/en/hardware-wallets/cryptnox-hardware-wallet/) | **65** | 77 | 70 | 64 | 78 | 21 | 49.9 |
| 28 | [UKey Core 26](https://walletinsights.io/en/hardware-wallets/ukey-core-26/) | **64** | 80 | 58 | 73 | 68 | 27 | 258 |
| 29 | [Blockstream Jade Classic](https://walletinsights.io/en/hardware-wallets/blockstream-jade/) | **63** | 61 | 66 | 56 | 67 | 71 | 79 |
| 30 | [Coinkite Coldcard Q](https://walletinsights.io/en/hardware-wallets/coinkite-coldcard-q/) | **63** | 74 | 74 | 56 | 37 | 62 | 319 |
| 31 | [Cypherock X1](https://walletinsights.io/en/hardware-wallets/cypherock-x1/) | **63** | 70 | 86 | 54 | 68 | 23 | 99 |
| 32 | [SafePal S1 Pro](https://walletinsights.io/en/hardware-wallets/safepal-s1-pro/) | **63** | 72 | 54 | 71 | 78 | 34 | 89.99 |
| 33 | [Ellipal X Card](https://walletinsights.io/en/hardware-wallets/ellipal-x-card/) | **62** | 66 | 70 | 70 | 80 | 14 | 69 |
| 34 | [Ellipal Titan 2](https://walletinsights.io/en/hardware-wallets/ellipal-titan-2/) | **58** | 55 | 58 | 76 | 80 | 21 | 169 |
| 35 | [Ellipal Titan Mini](https://walletinsights.io/en/hardware-wallets/ellipal-titan-mini/) | **56** | 52 | 55 | 76 | 73 | 21 | 99 |
| 36 | [Ngrave Zero](https://walletinsights.io/en/hardware-wallets/ngrave-zero/) | **56** | 61 | 58 | 66 | 70 | 15 | 398 |
| 37 | [CoolWallet Pro](https://walletinsights.io/en/hardware-wallets/coolwallet-pro/) | **49** | 55 | 38 | 62 | 76 | 5 | 149 |
| 38 | [Bitkey](https://walletinsights.io/en/hardware-wallets/bitkey-hardware-wallet/) | **42** | 48 | 51 | 77 | 51 | 32 | 250 |
<!-- ratings:end -->

Category weights: security 30%, recovery 20%, usability 20%, ecosystem 15%,
privacy 15%. If security is below 50, the overall score is multiplied by
0.8. Value is a separate score and is not part of the overall rating.

## Wallet fields

| Field | Meaning |
|---|---|
| `slug` | Stable identifier of the model |
| `name`, `brand` | Model name and manufacturer |
| `review_url` | Full review on walletinsights.io |
| `price_usd` | Manufacturer list price, USD |
| `release_year` | Year of release |
| `discontinued` | No longer sold |
| `rating_overall` | Overall rating, 0–100 |
| `rating_security`, `rating_recovery`, `rating_usability`, `rating_ecosystem`, `rating_privacy` | Category scores, 0–100 |
| `rating_value` | Value for money, 0–100 (separate from the overall rating) |
| `secure_element`, `secure_element_level` | Secure element chip and its stated certification, e.g. EAL6+ |
| `open_source_scope` | `firmware`, `partial`, `client` (companion app only) or `none` |
| `usb`, `bluetooth`, `nfc`, `qr`, `microsd` | Connectivity |
| `ios`, `android` | Works with the phone platform |
| `networks_count` | Blockchain networks supported, where known |
| `bitcoin_mode` | `bitcoin_only`, `optional_bitcoin_only` (separate firmware) or `multi_coin` |
| `shamir_backup`, `passphrase` | SLIP-39 Shamir backup; optional passphrase (25th word) |
| `wallet_apps` | Third-party wallet apps documented to work with the device, `;`-separated |
| `updated_at` | Last change to the model's data |

Incident fields are described in `data/security-incidents.json` (`fields`).

## Corrections

Open an issue with the field, the value you believe is correct and a
public source (manufacturer documentation, release notes, audit report,
certificate). Corrections change scores only through the formula. Unknown
values earn no points: a feature is credited only when a source confirms
it.

## Disclosure

walletinsights.io earns affiliate commissions from some manufacturers'
stores. Commissions do not enter the formula, and no manufacturer can pay
for a score or a position.

## Citation

> WalletInsights (2026). *WalletInsights hardware wallet ratings and
> security incidents* [Data set]. Zenodo.
> https://doi.org/10.5281/zenodo.24104206

When you use the data on the web, link to walletinsights.io or to the
model's `review_url`.
