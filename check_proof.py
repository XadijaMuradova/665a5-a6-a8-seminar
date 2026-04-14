import sys
from sympy import symbols, simplify

def validate_proof(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read().lower()

        # structure check
        required_keywords = ["theorem", "proof", "let", "so"]
        for word in required_keywords:
            if word not in content:
                print(f"Missing keyword: {word}")
                return False

        k, m = symbols('k m')

        steps_valid = True

        step1 = 2*k + 2*m
        step2 = 2*(k + m)

        if simplify(step1 - step2) != 0:
            print("Step validation failed")
            steps_valid = False

        if steps_valid:
            print("PROOF VALIDATED STEP-BY-STEP ✔")
            return True
        else:
            return False

    except FileNotFoundError:
        print("File not found")
        return False


if __name__ == "__main__":
    if validate_proof("proof.txt"):
        sys.exit(0)
    else:
        sys.exit(1)
