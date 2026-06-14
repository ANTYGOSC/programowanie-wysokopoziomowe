class Book:
    def __init__(self, title, author, total_copies):
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self._available_copies = total_copies
        self.reservations = []  # Lista przechowująca loginy czytelników, którzy zarezerwowali książkę

    @property
    def available_copies(self):
        return self._available_copies

    def borrow(self):
        if self._available_copies > 0:
            self._available_copies -= 1
            return True
        return False

    def __str__(self):
        rez_info = f" [Rezerwacje: {len(self.reservations)}]" if self.reservations else ""
        return f"'{self.title}' autor: {self.author} (Dostępne: {self.available_copies}/{self.total_copies}){rez_info}"


class User:
    def __init__(self, login, password, role):
        self._login = login        
        self._password = password  
        self.role = role

    @property
    def login(self):
        return self._login

    def authenticate(self, password):
        return self._password == password

    def menu(self, library):
        pass


class Reader(User):
    def __init__(self, login, password):
        super().__init__(login, password, "czytelnik")
        self.borrowed_books = []

    def menu(self, library):
        while True:
            print(f"\n--- MENU CZYTELNIKA ({self.login}) ---")
            print("1. Przeglądaj katalog (Filtrowanie i Sortowanie)")
            print("2. Wypożycz lub Zarezerwuj książkę")
            print("3. Moje wypożyczenia")
            print("4. Poproś o przedłużenie książki")
            print("5. Wyloguj")
            
            wybor = input("Wybierz opcję (1-5): ")
            if wybor == '1':
                library.advanced_catalog()
            elif wybor == '2':
                library.borrow_book(self)
            elif wybor == '3':
                library.show_user_borrows(self)
            elif wybor == '4':
                library.request_extension(self)
            elif wybor == '5':
                print("Wylogowano.")
                break
            else:
                print("Nieprawidłowy wybór.")


class Librarian(User):
    def __init__(self, login, password):
        super().__init__(login, password, "bibliotekarz")

    def menu(self, library):
        while True:
            print(f"\n--- MENU BIBLIOTEKARZA ({self.login}) ---")
            print("1. Przeglądaj katalog (Filtrowanie i Sortowanie)")
            print("2. Lista wszystkich wypożyczeń")
            print("3. Obsługa próśb o przedłużenie (Zarządzanie Rezerwacjami)")
            print("4. Statystyki systemu (Wersja Funkcyjna)")
            print("5. Wyloguj")
            
            wybor = input("Wybierz opcję (1-5): ")
            if wybor == '1':
                library.advanced_catalog()
            elif wybor == '2':
                library.show_all_borrows()
            elif wybor == '3':
                library.handle_extensions()
            elif wybor == '4':
                library.show_stats()
            elif wybor == '5':
                print("Wylogowano.")
                break
            else:
                print("Nieprawidłowy wybór.")


class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.extension_requests = []

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    def login_system(self):
        proby = 0
        while proby < 3:
            login = input("Podaj login: ")
            haslo = input("Podaj hasło: ")
            
            # Wyszukiwanie użytkownika bez pętli for (użycie filter i lambdy)
            user = next(filter(lambda u: u.login == login and u.authenticate(haslo), self.users), None)
            
            if user:
                print(f"\nZalogowano pomyślnie. Rola: {user.role.upper()}")
                return user
            
            proby += 1
            print(f"Błędne dane. Pozostało prób: {3 - proby}\n")
            
        print("Przekroczono limit prób logowania.")
        return None


    def display_collection(self, collection, predicate, action):
        """
        Przyjmuje kolekcję, funkcję filtrującą (predicate) i funkcję akcji (action).
        Wykorzystuje map i filter, by uniknąć tradycyjnej pętli 'for'.
        """

        list(map(action, filter(predicate, collection)))


    def advanced_catalog(self):
        print("\n=== ZAAWANSOWANY KATALOG ===")
        fraza = input("Szukaj w tytule/autorze (Enter by pominąć): ").lower()
        tylko_dostepne = input("Pokazać tylko dostępne? (t/n): ").lower() == 't'
        sort_opcja = input("Sortuj wg: 1. Tytuł | 2. Autor | 3. Liczba sztuk (malejąco): ")

        if tylko_dostepne:
            predykat = lambda b: (fraza in b.title.lower() or fraza in b.author.lower()) and b.available_copies > 0
        else:
            predykat = lambda b: fraza in b.title.lower() or fraza in b.author.lower()

        filtered_books = list(filter(predykat, self.books))

        if sort_opcja == '1':
            filtered_books = sorted(filtered_books, key=lambda b: b.title)
        elif sort_opcja == '2':
            filtered_books = sorted(filtered_books, key=lambda b: b.author)
        elif sort_opcja == '3':
            filtered_books = sorted(filtered_books, key=lambda b: b.available_copies, reverse=True)

        print("\nWyniki wyszukiwania:")
        if not filtered_books:
            print("Brak książek spełniających kryteria.")
        else:

            self.display_collection(filtered_books, lambda b: True, print)
        print("============================")

    def borrow_book(self, reader):
        tytul = input("Podaj dokładny tytuł książki: ")
        
        ksiazka = next(filter(lambda b: b.title.lower() == tytul.strip().lower(), self.books), None)

        if not ksiazka:
            print("Nie znaleziono takiej książki w katalogu.")
            return

        if ksiazka.borrow():
            reader.borrowed_books.append(ksiazka)
            print(f"Sukces! Wypożyczono '{ksiazka.title}'.")
        else:
            print(f"Brak wolnych egzemplarzy '{ksiazka.title}'.")
            decyzja = input("Czy chcesz zarezerwować ten tytuł? (t/n): ").lower()
            if decyzja == 't':
                ksiazka.reservations.append(reader.login)
                print("Zarezerwowano pomyślnie. Zostaniesz uwzględniony w kolejce.")

    def show_user_borrows(self, reader):
        print("\n--- MOJE WYPOŻYCZENIA ---")
        if not reader.borrowed_books:
            print("Brak wypożyczonych książek.")
        else:
           
            self.display_collection(
                reader.borrowed_books, 
                lambda b: True, 
                lambda b: print(f"- {b.title} ({b.author})")
            )

    def request_extension(self, reader):
        self.show_user_borrows(reader)
        if not reader.borrowed_books:
            return
            
        tytul = input("Podaj tytuł książki, którą chcesz przedłużyć: ")
        ksiazka = next(filter(lambda b: b.title.lower() == tytul.strip().lower(), reader.borrowed_books), None)
        
        if ksiazka:
            self.extension_requests.append({"czytelnik": reader, "ksiazka": ksiazka})
            print(f"Wysłano prośbę o przedłużenie książki '{ksiazka.title}'.")
        else:
            print("Nie masz takiej książki w wypożyczeniach.")

    def show_all_borrows(self):
        print("\n=== WSZYSTKIE WYPOŻYCZENIA ===")
        # List comprehension wybierające aktywnych czytelników
        aktywni_czytelnicy = [u for u in self.users if isinstance(u, Reader) and u.borrowed_books]
        
        if not aktywni_czytelnicy:
            print("Obecnie nikt nie ma wypożyczonych książek.")
            return

        for user in aktywni_czytelnicy:
            self.display_collection(
                user.borrowed_books,
                lambda b: True,
                lambda b: print(f"Użytkownik: {user.login} | Książka: '{b.title}'")
            )

    def handle_extensions(self):
        print("\n=== PROŚBY O PRZEDŁUŻENIE ===")
        if not self.extension_requests:
            print("Brak oczekujących próśb.")
            return

        for prosba in self.extension_requests[:]:
            czytelnik = prosba["czytelnik"]
            ksiazka = prosba["ksiazka"]
            
            # Info o rezerwacjach
            rez_info = f" [UWAGA: Książkę zarezerwowało {len(ksiazka.reservations)} osób!]" if ksiazka.reservations else " [Brak rezerwacji na ten tytuł]"
            
            print(f"\nCzytelnik '{czytelnik.login}' prosi o przedłużenie '{ksiazka.title}'.{rez_info}")
            decyzja = input("Zaakceptować przedłużenie? (t/n): ").lower()
            
            if decyzja == 't':
                print("Przedłużono pomyślnie.")
            else:
                print("Odrzucono prośbę.")
            self.extension_requests.remove(prosba)


    def show_stats(self):
        print("\n=== STATYSTYKI BIBLIOTEKI ===")
        if not self.books:
            return

        najpopularniejsza = max(self.books, key=lambda b: b.total_copies - b.available_copies)
        wypozyczono = najpopularniejsza.total_copies - najpopularniejsza.available_copies
        print(f"Najpopularniejsza książka: '{najpopularniejsza.title}' (Wypożyczono: {wypozyczono} szt.)")

 
        czytelnicy = filter(lambda u: isinstance(u, Reader), self.users)
        suma_wypozyczen = sum(map(lambda r: len(r.borrowed_books), czytelnicy))
        print(f"Łączna liczba aktywnych wypożyczeń w systemie: {suma_wypozyczen}")

 
        czytelnicy_lista = [u for u in self.users if isinstance(u, Reader) and len(u.borrowed_books) > 0]
        posortowani = sorted(czytelnicy_lista, key=lambda r: len(r.borrowed_books), reverse=True)

        print("\nRanking najbardziej aktywnych czytelników:")
   
        ranking = {r.login: len(r.borrowed_books) for r in posortowani}
        
        if not ranking:
            print("Brak aktywnych czytelników.")
        else:
            #
            self.display_collection(
                ranking.items(),
                lambda item: True,
                lambda item: print(f"- Użytkownik '{item[0]}' ma {item[1]} wypożyczonych książek.")
            )


def main():
    moja_biblioteka = Library()

    moja_biblioteka.add_book(Book("Pan Tadeusz", "Adam Mickiewicz", 3))
    moja_biblioteka.add_book(Book("Wiedźmin", "Andrzej Sapkowski", 0))
    moja_biblioteka.add_book(Book("Dziady", "Adam Mickiewicz", 5))
    moja_biblioteka.add_book(Book("Lalka", "Bolesław Prus", 1))
    moja_biblioteka.add_book(Book("Opowieść wigilijna", "Charles Dickens", 2))

    moja_biblioteka.add_user(Reader("janek", "haslo123"))
    moja_biblioteka.add_user(Reader("ania", "admin1"))
    moja_biblioteka.add_user(Reader("oski", "qwerty!"))
    
    moja_biblioteka.add_user(Librarian("admin", "admin123"))

    print("Witamy w Funkcyjnym Systemie Bibliotecznym!")
    
    while True:
        aktywny_uzytkownik = moja_biblioteka.login_system()
        if aktywny_uzytkownik:
            aktywny_uzytkownik.menu(moja_biblioteka)
        else:
            break

if __name__ == "__main__":
    main()