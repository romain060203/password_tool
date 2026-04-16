# main.py
import sys
from generator import generate_password
from checker import analyze_password
import argparse

def cli_menu():
    print("=== Password_tool ===")
    print("1. Générer un mot de passe")
    print("2. Tester un mot de passe")
    print("3. Quitter")
    choice = input("Choix: ").strip()
    return choice

def prompt_generate():
    try:
        length = int(input("Longueur souhaitée (ex: 12): ").strip() or "12")
    except ValueError:
        print("Entrée invalide, longueur par défaut 12.")
        length = 12
    use_upper = input("Inclure majuscules ? (Y/n): ").strip().lower() != 'n'
    use_lower = input("Inclure minuscules ? (Y/n): ").strip().lower() != 'n'
    use_digits = input("Inclure chiffres ? (Y/n): ").strip().lower() != 'n'
    use_specials = input("Inclure caractères spéciaux ? (Y/n): ").strip().lower() != 'n'
    try:
        pw = generate_password(length=length, use_upper=use_upper, use_lower=use_lower,
                               use_digits=use_digits, use_specials=use_specials)
        print("\nMot de passe généré :\n" + pw + "\n")
    except Exception as e:
        print("Erreur:", e)

def prompt_test():
    pw = input("Entrez le mot de passe à tester: ").strip()
    if not pw:
        print("Aucun mot de passe fourni.")
        return
    result = analyze_password(pw)
    print("\n--- Résultat ---")
    print(f"Longueur: {result['length']}")
    print(f"Présence: majuscule={result['has_upper']}, minuscule={result['has_lower']}, chiffre={result['has_digit']}, spécial={result['has_special']}")
    print(f"Motifs faibles détectés: {result['found_patterns'] or 'Aucun'}")
    print(f"Score: {result['score']} ({result['label']})")
    print("Feedback:")
    for f in result['feedback']:
        print(" -", f)
    print("----------------\n")

def main():
    while True:
        choice = cli_menu()
        if choice == '1':
            prompt_generate()
        elif choice == '2':
            prompt_test()
        elif choice == '3':
            print("Au revoir.")
            sys.exit(0)
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()