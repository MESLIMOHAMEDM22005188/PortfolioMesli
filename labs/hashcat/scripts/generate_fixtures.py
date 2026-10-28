#!/usr/bin/env python3
"""Generate deterministic, synthetic password-audit fixtures for this lab."""
from hashlib import md5, sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "lab"

# Fictional test strings only; never use these as real credentials.
CANDIDATES = [
    "lab-sample-2026",
    "blue-lab-demo",
    "hashcat-practice",
    "not-a-real-password",
]
WORDLIST = [
    "welcome",
    "password123",
    "lab-sample-2026",
    "blue-lab-demo",
    "hashcat-practice",
    "not-a-real-password",
    "candidate-not-in-fixture",
]


def main() -> None:
    LAB.mkdir(parents=True, exist_ok=True)
    (LAB / "hashes-md5.txt").write_text(
        "".join(f"{md5(value.encode(), usedforsecurity=False).hexdigest()}\n" for value in CANDIDATES),
        encoding="utf-8",
    )
    (LAB / "hashes-sha256.txt").write_text(
        "".join(f"{sha256(value.encode()).hexdigest()}\n" for value in CANDIDATES),
        encoding="utf-8",
    )
    (LAB / "wordlist.txt").write_text("\n".join(WORDLIST) + "\n", encoding="utf-8")
    print(f"Generated {len(CANDIDATES)} synthetic MD5 hashes.")
    print(f"Generated {len(CANDIDATES)} synthetic SHA-256 hashes.")
    print(f"Generated a wordlist with {len(WORDLIST)} candidates.")
    print("Fixtures only; no real credentials or external data were used.")


if __name__ == "__main__":
    main()
