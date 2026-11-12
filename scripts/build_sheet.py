#!/usr/bin/env python3
"""Build the manufacturer data sheet (.xlsx), blank or pre-filled.

  python3 scripts/build_sheet.py --blank templates/wallet-data.xlsx
  python3 scripts/build_sheet.py --prefill export.json --slug bitbox02 out.xlsx

`export.json` is a list of wallets with flat field keys (as in our database).
Requires openpyxl. Definitions and points: MANUFACTURERS.md.
"""

import argparse
import datetime as dt
import json

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

GUIDE = "https://github.com/walletinsights/hardware-wallet-ratings/blob/main/MANUFACTURERS.md"
B = "bool"

# (group, key, question, max points, kind, options)
FIELDS = [
    ("Identity", "name", "Model name", "", "text", None),
    ("Identity", "lifecycle_release_year", "Year of release", "", "number", None),
    ("Identity", "product_url", "Official product page", "", "text", None),
    ("Identity", "price_usd", "List price on your official store, USD, without temporary discounts", "", "number", None),
    ("Identity", "is_sold_out", "No longer sold (discontinued)", "", B, None),
    ("Security", "security_hardware_has_secure_element", "Keys stored in a secure element?", "18", B, None),
    ("Security", "security_hardware_chip_manufacturer", "Secure element manufacturer", "", "text", None),
    ("Security", "security_hardware_chip_model", "Secure element model", "", "text", None),
    ("Security", "security_hardware_secure_element_level", "Certification level of that chip", "4–12", "enum", ["EAL4+", "EAL5+", "EAL6+", "none"]),
    ("Security", "security_hardware_chip_certifications", "Common Criteria certificate ID(s)", "", "text", None),
    ("Security", "security_software_is_open_source", "Device firmware open source?", "8 (+10 privacy)", B, None),
    ("Security", "security_software_open_source_scope", "What is open source", "", "enum", ["firmware", "partial", "client", "none"]),
    ("Security", "security_non_extractable_keys", "After setup, NO function shows or exports the seed/keys (QR, microSD, file, plain text), and no known unpatched extraction. Showing words once at setup is allowed", "12", B, None),
    ("Security", "security_communication_encrypted", "Device ↔ host link encrypted?", "7 (+10 privacy)", B, None),
    ("Security", "security_anti_klepto", "Anti-klepto / anti-exfil signing", "8", B, None),
    ("Security", "security_anti_counterfeit_firmware_attestation", "Device proves genuine firmware/hardware to the app", "7", B, None),
    ("Security", "security_audits_audited", "Published third-party security audit", "8", B, None),
    ("Security", "security_audits_auditors", "Auditor(s)", "", "text", None),
    ("Security", "security_audits_last_audit_date", "Date of the latest audit (YYYY-MM-DD)", "", "text", None),
    ("Security", "security_access_code_supported", "Access code protecting the device or wallet †", "3", B, None),
    ("Security", "pin_security_auto_wipe", "Wipe after too many wrong PINs", "3", B, None),
    ("Security", "pin_security_randomized_keypad", "Randomized PIN layout", "3", B, None),
    ("Security", "pin_security_attempt_limit", "Number of PIN attempts allowed", "2", "number", None),
    ("Security", "firmware_security_downgrade_protection", "Refuses older firmware", "4", B, None),
    ("Security", "firmware_security_rollback_prevention", "Prevents rollback after an update", "4", B, None),
    ("Security", "threat_model_supply_chain_mitigation", "Measures against tampering between factory and user †", "3", B, None),
    ("Security", "threat_model_tamper_evident_design", "Tamper-evident enclosure or packaging †", "3", B, None),
    ("Security", "security_software_reproducible_builds", "Firmware builds reproducibly from source", "4", B, None),
    ("Security", "security_hardware_secure_boot", "Secure boot chain", "3", B, None),
    ("Recovery", "recovery_seed_type", "Standard recovery phrases the device can create, default first", "12–25", "enum", ["BIP39", "SLIP39", "BIP39, SLIP39", "SLIP39, BIP39", "NONE"]),
    ("Recovery", "recovery_seed_word_count", "Longest phrase supported (words)", "3–6", "enum", ["12", "18", "20", "24", "33"]),
    ("Recovery", "recovery_shamir_secret_sharing", "Threshold (k-of-n) split: SLIP-39, Codex32 or vendor scheme. Seed XOR does not count", "8", B, None),
    ("Recovery", "recovery_passphrase_support", "Optional passphrase (25th word)", "8 (+4 with BIP39)", B, None),
    ("Recovery", "recovery_multi_card_backup", "DEFAULT setup backs up to extra smart cards instead of a written phrase", "12", B, None),
    ("Recovery", "recovery_recovery_card_support", "Any smart-card backup available (default or optional accessory)", "", B, None),
    ("Recovery", "recovery_multisig_key_replacement", "Lost keys replaced through multisig (seedless designs)", "12", B, None),
    ("Recovery", "recovery_bip85_support", "BIP-85 child seeds", "8", B, None),
    ("Recovery", "security_access_code_recovery", "Recovery protected by an access code", "4", B, None),
    ("Recovery", "recovery_hidden_wallets_by_passphrase", "Hidden wallets through passphrases", "4", B, None),
    ("Recovery", "recovery_social_recovery", "Social recovery", "3", B, None),
    ("Recovery", "recovery_vendor_backup_supported", "You or partners hold an encrypted copy or shares of the seed (user's own iCloud/Google does not count)", "", B, None),
    ("Recovery", "recovery_vendor_backup_default_enabled", "…and it is on by default", "−3", B, None),
    ("Recovery", "recovery_vendor_backup_opt_in", "…and the user must opt in", "", B, None),
    ("Usability", "security_transfer_on_device_verification", "Device's OWN screen shows recipient and amount of a native transfer", "5", B, None),
    ("Usability", "security_clear_signing_supported", "Device's own screen decodes ERC-20 approve (token, spender, amount) AND EIP-712 typed data. Bitcoin-only: true", "5", B, None),
    ("Usability", "connectivity_usb", "USB", "7–12", B, None),
    ("Usability", "connectivity_bluetooth", "Bluetooth", "", B, None),
    ("Usability", "connectivity_nfc", "NFC", "", B, None),
    ("Usability", "connectivity_qr", "QR codes (air-gapped)", "", B, None),
    ("Usability", "ux_configuration_time_min", "Minutes from unboxing to a ready wallet", "5–10", "number", None),
    ("Usability", "ux_multi_language_support", "Interface languages (comma-separated)", "2–8", "text", None),
    ("Ecosystem", "features_unified_accounts", "YOUR OWN app shows all networks from one seed as one portfolio with a total balance, with send/receive", "15", B, None),
    ("Ecosystem", "features_exchange_integration", "Buy / sell / swap inside your app", "15", B, None),
    ("Ecosystem", "chain_support_networks_count", "Blockchain networks supported natively", "5–20", "number", None),
    ("Ecosystem", "compatibility_windows", "Windows", "5–10", B, None),
    ("Ecosystem", "compatibility_macos", "macOS", "", B, None),
    ("Ecosystem", "compatibility_linux", "Linux", "", B, None),
    ("Ecosystem", "compatibility_ios", "iOS", "6–10", B, None),
    ("Ecosystem", "compatibility_android", "Android", "", B, None),
    ("Ecosystem", "features_wallet_connect_support", "WalletConnect", "8", B, None),
    ("Ecosystem", "features_full_node_support", "Use with the user's own Bitcoin node (your app or a documented coordinator such as Sparrow)", "8 (+8 privacy)", B, None),
    ("Ecosystem", "features_smart_contract_interaction", "Signing smart-contract calls †", "5", B, None),
    ("Ecosystem", "features_coin_control", "Manual UTXO selection in your app or a coordinator you document", "4 (+4 privacy)", B, None),
    ("Ecosystem", "features_cold_staking_support", "Staking with keys kept on the device †", "4", B, None),
    ("Ecosystem", "features_multisig", "Multisig support †", "3–5", "enum", ["none", "basic", "advanced"]),
    ("Privacy", "privacy_tor_support", "Tor in your app", "15", B, None),
    ("Privacy", "privacy_no_account_registration", "Works without creating an account", "12", B, None),
    ("Privacy", "privacy_coin_join_support", "CoinJoin", "8", B, None),
    ("Privacy", "privacy_avoids_telemetry", "No telemetry at all", "8", B, None),
    ("Privacy", "security_software_telemetry_present", "Telemetry present in your app", "−5 to −1", B, None),
    ("Privacy", "security_software_telemetry_opt_out_possible", "…can be turned off", "", B, None),
    ("Privacy", "security_software_telemetry_enabled_by_default", "…is on by default", "", B, None),
    ("Privacy", "security_software_telemetry_details", "What telemetry collects", "", "text", None),
    ("Privacy", "privacy_can_work_fully_offline", "Setup, signing and use without the device or app ever touching an internet-connected host", "6", B, None),
    ("Privacy", "privacy_metadata_protection", "Protection of wallet metadata (balances, addresses) from third parties †", "5", B, None),
    ("Privacy", "privacy_leak_resistance", "Measures against leaking addresses or public keys †", "4", B, None),
    ("Privacy", "privacy_network_fingerprinting_resistance", "Measures against network fingerprinting of the user †", "4", B, None),
]

HEAD = ["Group", "Field", "Question", "Max points", "Our current value", "Your value", "Public source (URL)", "Since firmware", "Comment"]
WIDTH = [11, 34, 60, 11, 22, 18, 44, 14, 30]
BOLD = Font(bold=True)
HEAD_FILL = PatternFill("solid", fgColor="0F172A")
UNKNOWN_FILL = PatternFill("solid", fgColor="FEF3C7")
WRAP = Alignment(wrap_text=True, vertical="top")


def show(v, key=""):
    if key == "features_multisig" and v == "secure":
        return "advanced"
    if v is None or v == "":
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    return str(v)


def build(path, wallet=None):
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    title = f"{wallet['name']} — data held by WalletInsights" if wallet else "WalletInsights — hardware wallet data sheet"
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = (
        f"Exported {dt.date.today().isoformat()}. Check 'Our current value'; where it is wrong or empty, "
        "fill 'Your value' and a public source. Empty yellow rows are unknown to us and score 0."
        if wallet else
        "Fill 'Your value' and a public source for each field you can document. Leave unknown fields empty."
    )
    ws["A3"] = f"Definitions, points and what counts as a source: {GUIDE}   († = definition to be published; describe what the device does)"
    for c in ("A2", "A3"):
        ws[c].alignment = Alignment(wrap_text=False)
    ws.append([])
    ws.append(HEAD)
    hr = ws.max_row
    for i, _ in enumerate(HEAD, 1):
        cell = ws.cell(hr, i)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = HEAD_FILL
    for i, w in enumerate(WIDTH, 1):
        ws.column_dimensions[chr(64 + i)].width = w
    ws.freeze_panes = f"C{hr + 1}"

    dv_bool = DataValidation(type="list", formula1='"true,false"', allow_blank=True)
    ws.add_data_validation(dv_bool)
    for group, key, question, points, kind, options in FIELDS:
        current = show(wallet.get(key), key) if wallet else ""
        ws.append([group, key, question, points, current, "", "", "", ""])
        r = ws.max_row
        for i in range(1, len(HEAD) + 1):
            ws.cell(r, i).alignment = WRAP
        if kind == B:
            dv_bool.add(f"F{r}")
        elif kind == "enum":
            dv = DataValidation(type="list", formula1='"' + ",".join(o.replace(",", " +") if "," in o else o for o in options) + '"', allow_blank=True)
            ws.add_data_validation(dv)
            dv.add(f"F{r}")
        if wallet and current == "" and points:
            for i in range(1, 6):
                ws.cell(r, i).fill = UNKNOWN_FILL

    note = wb.create_sheet("Read me")
    for line in [
        "How this sheet works",
        "",
        "1. One row per field. 'Our current value' is what WalletInsights holds today (empty = unknown, scores 0).",
        "2. Where it is wrong or empty, choose or type 'Your value' and add a public URL that shows it.",
        "3. Accepted sources: documentation, help center, firmware changelogs (with version), source code,",
        "   Common Criteria certificates, published audit reports. Marketing claims and private emails are not enough.",
        "4. If a feature depends on firmware, give the first version that has it.",
        "5. Recovery phrase types with two standards: 'BIP39 + SLIP39' means both, the first one is the default.",
        "6. Editorial scores (setup ease, interface quality, learning curve, backup ease) are set by our reviewers",
        "   and are not part of this sheet.",
        "",
        "Corrections change scores only through the published formula. Scores and placements are not for sale.",
        f"Full guide: {GUIDE}",
        "Send the filled sheet to contact@walletinsights.io",
    ]:
        note.append([line])
    note["A1"].font = Font(bold=True, size=14)
    note.column_dimensions["A"].width = 110
    wb.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--blank", action="store_true")
    ap.add_argument("--prefill")
    ap.add_argument("--slug")
    ap.add_argument("out")
    a = ap.parse_args()
    if a.blank:
        build(a.out)
        return
    data = json.load(open(a.prefill))
    rows = data["data"] if isinstance(data, dict) else data
    wallet = next(w for w in rows if w["slug"] == a.slug)
    build(a.out, wallet)


if __name__ == "__main__":
    main()
