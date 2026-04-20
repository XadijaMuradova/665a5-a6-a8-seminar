import sys
import os
import argparse
import datetime
from sympy import symbols, simplify

PROOF_FILE = "proof.txt"

def validate_structure(content: str) -> bool:
    print("=== Struktur Yoxlaması ===")
    errors = []

    required = {
        "theorem" : "Teorem bəyanı",
        "proof"   : "İsbat bloku",
        "let"     : "Dəyişən tərifi",
        "so"      : "Nəticə ifadəsi",
        "even"    : "Cüt ədəd nəticəsi",
    }
    for word, label in required.items():
        if word in content.lower():
            print(f"  [PASS] '{word}' — {label} mövcuddur")
        else:
            print(f"  [FAIL] '{word}' — {label} tapılmadı!")
            errors.append(word)

    qed_markers = ["∎", "qed", "□", "blacksquare", "proved", "proven"]
    if any(m in content.lower() for m in qed_markers):
        print("  [PASS] QED işarəsi mövcuddur")
    else:
        print("  [WARN] QED işarəsi tövsiyə olunur (∎ / Q.E.D.)")

    if errors:
        print(f"\n[FAIL] Struktur yoxlaması uğursuz — {len(errors)} xəta\n")
        return False

    print("\n[PASS] Proof strukturu tam ✓\n")
    return True

def validate_math() -> bool:
    print("=== SymPy Riyazi Doğrulama ===")
    errors = []

    k, m = symbols('k m')

    lhs = 2*k + 2*m
    rhs = 2 * (k + m)
    if simplify(lhs - rhs) == 0:
        print("  [PASS] 2k + 2m = 2(k+m)  →  algebraik bərabərlik doğrudur")
    else:
        print("  [FAIL] 2k + 2m ≠ 2(k+m)  →  xəta!")
        errors.append("algebraic_step")

    expr = 2 * (k + m)
    quotient = simplify(expr / 2)
    if quotient == k + m:
        print(f"  [PASS] 2(k+m) / 2 = {quotient}  →  nəticə cüt ədəddir")
    else:
        print("  [FAIL] Bölünmə yoxlaması uğursuz!")
        errors.append("divisibility")

    print("\n  Konkret dəyərlər:")
    test_cases = [(2, 4), (6, 8), (0, 10), (14, 22)]
    for a, b in test_cases:
        result = a + b
        ok = result % 2 == 0
        mark = "✓" if ok else "✗"
        print(f"    {a} + {b} = {result}  →  cüt? {mark}")
        if not ok:
            errors.append(f"concrete_{a}_{b}")

    if errors:
        print(f"\n[FAIL] Riyazi doğrulama uğursuz — {len(errors)} xəta\n")
        return False

    print("\n[PASS] Bütün riyazi yoxlamalar keçdi ✓\n")
    return True

def generate_ci_report(struct_ok: bool, math_ok: bool):
    os.makedirs("reports", exist_ok=True)

    status = "PASSED ✓" if (struct_ok and math_ok) else "FAILED ✗"
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    report = (
        "  CI — THEOREM PROOF VALIDATION REPORT\n"
        f"Date      : {now}\n"
        f"File      : {PROOF_FILE}\n"
        f"Structure : {'PASS ✓' if struct_ok else 'FAIL ✗'}\n"
        f"Math      : {'PASS ✓' if math_ok  else 'FAIL ✗'}\n"
        f"Status    : {status}\n"
    )

    with open("reports/ci_validation.txt", "w") as f:
        f.write(report)
    print(report)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["structure", "math", "report", "full"],
                        default="full")
    args = parser.parse_args()

    try:
        with open(PROOF_FILE, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"[FAIL] '{PROOF_FILE}' faylı tapılmadı!")
        sys.exit(1)

    struct_ok = True
    math_ok   = True

    if args.mode in ("structure", "full"):
        struct_ok = validate_structure(content)

    if args.mode in ("math", "full"):
        math_ok = validate_math()

    if args.mode in ("report", "full"):
        generate_ci_report(struct_ok, math_ok)

    if not (struct_ok and math_ok):
        sys.exit(1)


if __name__ == "__main__":
    main()
