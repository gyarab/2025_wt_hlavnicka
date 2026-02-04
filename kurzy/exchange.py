import httpx

import sys

CNB_URL = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt"

def ziskej_kurz(mena):

    try:
        response = httpx.get(CNB_URL)
        response.raise_for_status()  #ověří, zda požadavek proběhl v pořádku (kód 200)
        data = response.text
        
        # Procházíme řádky a hledáme EUR
        for radek in data.splitlines():
            # např.: "EMU|euro|1|EUR|25,123"
            parts = radek.split("|")
            
            if len(parts) >= 5 and parts[3] == mena:
                kurz_str = parts[4].replace(",", ".")
                mnozstvi = float(parts[2]) 
                kurz = float(kurz_str)
                return kurz / mnozstvi
                
    except Exception as e:
        print(f"Chyba při stahování kurzu: {e}")
        return None
def ziskej_meny():
    try:
        response = httpx.get(CNB_URL)
        response.raise_for_status()
        data = response.text
        
        meny = []
        for radek in data.splitlines():
            parts = radek.split("|")
            if len(parts) >= 5:
                meny.append(parts[3] + " = " + parts[1] +", " + parts[0])
        return meny
    except Exception as e:
        print(f"Chyba při stahování měn: {e}")
        return []
        
def main():
    print("--- PŘEVODNÍK MĚN (ČNB) ---")
    print("\n1: ukázat dostupné měny")
    print("2: převést měnu")
    print("3: ukončit program")

    volba = input("Zvolte akci (1-3): ")

    if volba == "1":
        meny = ziskej_meny()
        if not meny:
            print("Nepodařilo se načíst seznam měn.")
            sys.exit(1)

        print("Dostupné měny:")
        for m in meny:
            if m.startswith("země"):
                continue
            print(f" - {m}")

    elif volba == "2":
        prevest_meny()

    elif volba == "3":
        print("Děkuji za využití!")
        sys.exit(0)

    else:
        print("Neplatná volba.")


def prevest_meny():
    mena = input("Vyberte měnu na převod: ")

    kurz = ziskej_kurz(mena)

    if kurz is None:
        print("Nepodařilo se načíst aktuální kurz.")
        sys.exit(1)

    print(f"Aktuální kurz {mena}: {kurz} CZK")
    print("-" * 30)

    while True:
        try:
            castka_input = input("Zadejte částku k převodu: ")
            castka = float(castka_input)
            if castka < 0:
                print("Částka nesmí být záporná.")
                continue
            break
        except ValueError:
            print("Neplatný vstup! Zadejte prosím číslo (např. 100 nebo 10.5).")

    print("\nVyberte směr převodu:")
    print(f"1: CZK -> {mena}")
    print(f"2: {mena} -> CZK")

    while True:
        volba = input("Vaše volba (1 nebo 2): ").strip()
        
        if volba == "1":
            vysledek = castka / kurz
            print(f"\n{castka:.2f} CZK = {vysledek:.2f} {mena}")
            break
        elif volba == "2":
            vysledek = castka * kurz
            print(f"\n{castka:.2f} {mena} = {vysledek:.2f} CZK")
            break
        else:
            print("Neplatná volba. Zadejte pouze 1 nebo 2.")


while True:
    main()
    input("\n\nStiskněte Enter pro pokračování...")

