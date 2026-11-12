# Data guide for manufacturers

How WalletInsights collects the data behind its hardware wallet ratings, and
how a manufacturer can submit or correct it.

The short version: every rating is computed from public, checkable facts by
the formula in [METHODOLOGY.md](METHODOLOGY.md). Send us a fact with a public
source and the score follows from the formula. Nothing else changes a score.

## What we accept

| Accepted as a source | Not accepted on its own |
|---|---|
| Your documentation, help center, product page or spec sheet | Marketing claims without technical detail ("military-grade", "unhackable") |
| Firmware release notes and changelogs, with the version | Statements in private email, calls or partner kits |
| Firmware or app source code (public repository, tag or commit) | Screenshots that are not published anywhere |
| Certificates from the issuing body (Common Criteria certificate ID, certification report) | "EAL6+" without the chip model and certificate |
| Published third-party audit reports (auditor, date, scope) | Audit announcements without the report |
| Independent research, CVE entries, conference talks | |

A public page on your own site is enough. If the information exists only in
a private document, publish it (a help-center article or a GitHub file is
fine) and send us the link.

When a feature depends on the firmware version, give the first version that
has it. We record the version and credit the feature from that version on.

## What earns points and what does not

- **Unknown earns nothing.** A field without a public source stays empty and
  scores 0. Most score increases after a vendor contact come from filling
  these gaps, not from disputes.
- **A documented "no" is recorded as "no".** Some fields carry a risk line
  when false (for example, no on-device verification). Correct them with a
  source if the device has changed.
- **Editorial scores are ours.** Setup ease, interface quality, learning curve
  and backup ease (1–5) are set by our reviewers on the device. You can point
  us to new firmware or a redesigned flow; the score is reassessed, not
  negotiated.
- **Formula changes are separate.** If you think a factor is weighted wrongly,
  say so — but that is a change for every wallet, decided and published as a
  formula change, never for one brand.

We do not publish partner copy, follow brand messaging guidelines, use
suggested anchor text or sell placements. Affiliate relationships do not enter
the formula.

## How to submit

The simplest way is email: **contact@walletinsights.io**. No GitHub account
needed.

1. **Check what we hold for your models.** Ask us for the data sheet of a
   model: a spreadsheet with one row per field and our current value. Correct
   what is wrong, fill what is empty (empty rows score 0), add a public source
   for each change, and send it back.
2. **New model** — fill in the blank sheet
   [`templates/wallet-data.xlsx`](templates/wallet-data.xlsx) (Excel, Google
   Sheets or Numbers; values are picked from drop-down lists) and email it, or
   attach it to a
   [New model](https://github.com/walletinsights/hardware-wallet-ratings/issues/new?template=new-model.yml)
   issue.
3. **A single correction** — email it, or use the
   [Data correction](https://github.com/walletinsights/hardware-wallet-ratings/issues/new?template=data-correction.yml)
   form.

Every change needs a public source URL. Leave a field empty if you have no
public source — that is better than a guess, and we will look for one.

We check every source ourselves. Accepted changes appear on the site and in
`data/` with the next update; the change history is public in this
repository.

## Fields

Field keys match the data files and our database. Points are the maximum the
field can add to its category (see [METHODOLOGY.md](METHODOLOGY.md) for the
full formula).

Fields marked † do not have a published one-line definition yet. For those,
describe what the device does, with a source, and we classify it; the
definition we settle on is published here and applied to every wallet.

### Security (30% of the overall rating)

| Field | Question | Points | Typical source |
|---|---|---:|---|
| `security_hardware_has_secure_element` | Does the device store keys in a secure element? | 18 | Spec sheet, teardown, chip documentation |
| `security_hardware_secure_element_level` | Certification level of that chip (EAL4+ / EAL5+ / EAL6+) | 4–12 | Common Criteria certificate ID and chip model (`security_hardware_chip_model`, `security_hardware_chip_manufacturer`) |
| `security_software_is_open_source` | Is the device firmware open source? (`security_software_open_source_scope`: firmware / partial / client / none) | 8 (+10 privacy) | Public repository |
| `security_non_extractable_keys` | After setup, is there **no** function that shows or exports the seed or keys (QR, microSD, file, plain text over a link), and no known unpatched extraction? Showing the words once at setup is allowed | 12 | Docs listing device menus; absence of a "show recovery phrase" function |
| `security_communication_encrypted` | Is the link between device and host app encrypted? | 7 (+10 privacy) | Protocol documentation |
| `security_anti_klepto` | Anti-klepto / anti-exfil signing protocol | 8 | Docs, firmware source |
| `security_anti_counterfeit_firmware_attestation` | Can the device prove genuine firmware/hardware to the app (attestation)? | 7 | Docs |
| `security_audits_audited` | Published third-party security audit (`security_audits_reports`, `security_audits_auditors`, `security_audits_last_audit_date`) | 8 | Audit report URL |
| `security_access_code_supported` † | Access code protecting the device or the wallet | 3 | Docs |
| `pin_security_auto_wipe` | Wipe after a number of wrong PINs | 3 | Docs |
| `pin_security_randomized_keypad` | Randomized PIN layout | 3 | Docs |
| `pin_security_attempt_limit` | Number of PIN attempts allowed | 2 | Docs |
| `firmware_security_downgrade_protection` | Refuses to install older firmware | 4 | Docs, source |
| `firmware_security_rollback_prevention` | Prevents rollback after an update | 4 | Docs, source |
| `threat_model_supply_chain_mitigation` † | Measures against tampering between factory and user | 3 | Docs |
| `threat_model_tamper_evident_design` † | Tamper-evident enclosure or packaging | 3 | Docs |
| `security_software_reproducible_builds` | Firmware builds reproducibly from source | 4 | Build instructions, independent verification |
| `security_hardware_secure_boot` / `security_software_secure_boot` | Secure boot chain | 3 | Docs |

Without a secure element the security score is capped at 75; without a secure
element and without non-extractable keys, at 60.

### Recovery (20%)

| Field | Question | Points | Typical source |
|---|---|---:|---|
| `recovery_seed_type` | Which standard recovery phrases can the device create? Write tokens only: `BIP39`, `SLIP39` (default first, comma-separated) or `NONE` if no standard phrase is possible | 12–25 | Setup documentation |
| `recovery_seed_word_count` | Longest phrase supported (12 / 20 / 24 words) | 3–6 | Docs |
| `recovery_shamir_secret_sharing` | Threshold (k-of-n) split of the secret: SLIP-39, Codex32 or a vendor scheme. Seed XOR does not count | 8 | Docs |
| `recovery_passphrase_support` | Optional passphrase (25th word) | 8 (+4 with BIP39) | Docs |
| `recovery_multi_card_backup` | In the **default** setup, the key is backed up on extra smart cards instead of a written phrase | 12 | Docs |
| `recovery_multisig_key_replacement` | Lost keys replaced through a multisig arrangement (seedless designs) | 12 | Docs |
| `recovery_bip85_support` | BIP-85 child seeds | 8 | Docs, changelog |
| `security_access_code_recovery` | Recovery protected by an access code | 4 | Docs |
| `recovery_hidden_wallets_by_passphrase` | Hidden wallets through passphrases | 4 | Docs |
| `recovery_social_recovery` | Social recovery | 3 | Docs |
| `recovery_vendor_backup_supported`, `recovery_vendor_backup_default_enabled`, `recovery_vendor_backup_opt_in` | Do you or your partners hold an encrypted copy or shares of the seed? Is it on by default, or opt-in? A backup in the user's own iCloud/Google account does not count | −3 if on by default without opt-in | Docs, terms of service |

`recovery_backup_ease` (1–5) is editorial.

### Usability (20%)

| Field | Question | Points | Typical source |
|---|---|---:|---|
| `security_transfer_on_device_verification` | Does the device's **own screen** show the recipient address and amount of a native transfer? | 5 | Docs, screenshots in docs |
| `security_clear_signing_supported` | Does the device's own screen decode an ERC-20 `approve` (token, spender, amount) **and** EIP-712 typed data as readable fields, not only a hash? Bitcoin-only devices: true by definition | 5 | Docs, firmware changelog with version |
| `connectivity_usb`, `connectivity_bluetooth`, `connectivity_nfc`, `connectivity_qr` | Connection methods | 7–12 | Spec sheet |
| `ux_configuration_time_min` | Minutes from unboxing to a ready wallet | 5–10 | Setup guide; we verify |
| `ux_multi_language_support` | Interface languages on the device/app (list) | 2–8 | Docs |

`ux_setup_ease`, `ux_interface_quality` and `ux_learning_curve` (1–5) are
editorial.

### Ecosystem (15%)

| Field | Question | Points | Typical source |
|---|---|---:|---|
| `features_unified_accounts` | Does **your own** companion app show all networks from one seed as one portfolio with a total balance, with send/receive from that app? | 15 | App documentation |
| `features_exchange_integration` | Buy/sell/swap inside your app | 15 | App documentation |
| `chain_support_networks_count` | Number of blockchain networks supported natively | 5–20 | Supported-coins page |
| `compatibility_windows`, `compatibility_macos`, `compatibility_linux` | Desktop platforms | 5–10 | Downloads page |
| `compatibility_ios`, `compatibility_android` | Mobile platforms | 6–10 | App stores |
| `features_wallet_connect_support` | WalletConnect | 8 | Docs |
| `features_full_node_support` | Use with the user's own Bitcoin node (in your app or a documented coordinator such as Sparrow) | 8 (+8 privacy) | Docs |
| `features_smart_contract_interaction` † | Signing smart-contract calls | 5 | Docs |
| `features_coin_control` | Manual UTXO selection in your app or a coordinator you document | 4 (+4 privacy) | Docs |
| `features_cold_staking_support` † | Staking with keys kept on the device | 4 | Docs |
| `features_multisig` † | Multisig support, and in which form | 3–5 | Docs |

### Privacy (15%)

| Field | Question | Points | Typical source |
|---|---|---:|---|
| `privacy_tor_support` | Tor in your app | 15 | Docs |
| `privacy_no_account_registration` | Works without creating an account | 12 | Docs |
| `privacy_coin_join_support` | CoinJoin | 8 | Docs |
| `privacy_avoids_telemetry` | No telemetry at all | 8 | Privacy policy, source |
| `security_software_telemetry_present`, `security_software_telemetry_opt_out_possible`, `security_software_telemetry_enabled_by_default` | Is there telemetry? Can it be turned off? Is it on by default? (`security_software_telemetry_details`: what is collected) | −5 to −1 | Privacy policy, settings documentation, source |
| `privacy_can_work_fully_offline` | Setup, signing and use work without the device or app ever touching an internet-connected host | 6 | Docs |
| `privacy_metadata_protection` † | Protection of wallet metadata (balances, addresses) from third parties | 5 | Docs |
| `privacy_leak_resistance` † | Measures against leaking addresses or public keys | 4 | Docs |
| `privacy_network_fingerprinting_resistance` † | Measures against network fingerprinting of the user | 4 | Docs |

An opt-out or "off by default" counts only when it is documented.

### Price and identity (not scored, but needed)

`name`, `brand`, `release_year`, `price_usd` (list price on your official
store, without temporary discounts), `discontinued`, official product URL,
product images on a transparent background (PNG, at least 1200 px).

## Contact

contact@walletinsights.io — corrections and submissions.
security@walletinsights.io — security incidents and disclosures.
