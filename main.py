# Zdefiniowane na sztywno 5 książek jako lista słowników
ksiazki = [
    {"tytul": "Pan Tadeusz", "autor": "Adam Mickiewicz", "sztuk": 3},
    {"tytul": "Wiedźmin", "autor": "Andrzej Sapkowski", "sztuk": 0},
    {"tytul": "Dziady", "autor": "Adam Mickiewicz", "sztuk": 5},
    {"tytul": "Lalka", "autor": "Bolesław Prus", "sztuk": 1},
    {"tytul": "Opowieść wigilijna", "autor": "Charles Dickens", "sztuk": 2 }
]

# Każdy użytkownik ma własną pustą listę "wypozyczenia", do której będą trafiać książki
uzytkownicy = [
    {"login": "janek", "haslo": "haslo123", "rola": "czytelnik", "wypozyczenia": []},
    {"login": "ania", "haslo": "admin1", "rola": "czytelnik", "wypozyczenia": []},
    {"login": "oski", "haslo": "qwerty!", "rola": "czytelnik", "wypozyczenia": []}
]

def logowanie(lista_uzytkownikow):
    """Obsługuje proces logowania z limitem 3 prób."""
    proby = 0
    while proby < 3:
        podany_login = input("Podaj login: ")
        podane_haslo = input("Podaj hasło: ")
        
        # Iterujemy przez bazę użytkowników, aby sprawdzić poprawność danych
        for uzytkownik in lista_uzytkownikow:
            if uzytkownik["login"] == podany_login and uzytkownik["haslo"] == podane_haslo:
                print(f"\nZalogowano pomyślnie. Witaj, {podany_login}!")
                return uzytkownik
                
        proby += 1
        pozostalo = 3 - proby
        print(f"Błędny login lub hasło. Pozostało prób: {pozostalo}\n")
        
    print("Przekroczono limit prób logowania. Zamykanie programu.")
    return None

def pokaz_katalog(lista_ksiazek):
    """Wyświetla wszystkie dostępne książki w bibliotece."""
    print("\n--- KATALOG KSIĄŻEK ---")
    for ksiazka in lista_ksiazek:
        print(f"Tytuł: '{ksiazka['tytul']}' | Autor: {ksiazka['autor']} | Dostępne sztuki: {ksiazka['sztuk']}")
    print("-----------------------\n")

def wypozycz_ksiazke(zalogowany_uzytkownik, lista_ksiazek):
    """Obsługuje wypożyczanie książki i aktualizuje stan magazynowy."""
    szukany_tytul = input("Podaj dokładny tytuł książki, którą chcesz wypożyczyć: ")
    
    for ksiazka in lista_ksiazek:
        # Sprawdzamy czy tytuł się zgadza (ignorujemy wielkość liter dla wygody)
        if ksiazka["tytul"].strip().lower() == szukany_tytul.strip().lower():
            if ksiazka["sztuk"] > 0:
                ksiazka["sztuk"] -= 1  # Zmniejszamy stan w magazynie
                zalogowany_uzytkownik["wypozyczenia"].append(ksiazka["tytul"]) # Dodajemy do konta
                print(f"Pomyślnie wypożyczono książkę: '{ksiazka['tytul']}'.")
            else:
                print(f"Przepraszamy, brak wolnych egzemplarzy książki '{ksiazka['tytul']}'.")
            return 
            
    print("Nie znaleziono książki o takim tytule w naszym katalogu.")

def pokaz_moje_wypozyczenia(zalogowany_uzytkownik):
    """Wyświetla książki przypisane do konta zalogowanego użytkownika."""
    print("\n--- MOJE WYPOŻYCZENIA ---")
    lista_wypozyczen = zalogowany_uzytkownik["wypozyczenia"]
    
    if len(lista_wypozyczen) == 0:
        print("Nie masz obecnie wypożyczonych żadnych książek.")
    else:
        for nr, tytul in enumerate(lista_wypozyczen, start=1):
            print(f"{nr}. {tytul}")
    print("-------------------------\n")

def menu_glowne(zalogowany_uzytkownik, lista_ksiazek):

    while True:
        print("\n=== MENU GŁÓWNE ===")
        print("1. Przeglądaj katalog")
        print("2. Wypożycz książkę")
        print("3. Moje wypożyczenia")
        print("4. Wyloguj")
        
        wybor = input("Wybierz opcję (1-4): ")
        
        if wybor == '1':
            pokaz_katalog(lista_ksiazek)
        elif wybor == '2':
            wypozycz_ksiazke(zalogowany_uzytkownik, lista_ksiazek)
        elif wybor == '3':
            pokaz_moje_wypozyczenia(zalogowany_uzytkownik)
        elif wybor == '4':
            print("Wylogowano. Do widzenia!")
            break 
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

# --- GŁÓWNA FUNKCJA URUCHAMIAJĄCA ---
def main():
    print("Witamy w Systemie Bibliotecznym!")
    
    aktywny_uzytkownik = logowanie(uzytkownicy)
    
    # Jeśli logowanie się powiodło (zwrócono użytkownika zamiast None)
    if aktywny_uzytkownik is not None:
        menu_glowne(aktywny_uzytkownik, ksiazki)

# Ten warunek upewnia się, że funkcja main() odpali się tylko, gdy bezpośrednio uruchamiamy ten plik
if __name__ == "__main__":
    main()