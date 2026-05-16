class Book:
    def __init__(self, title, author, total_copies):
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self._available_copies = total_copies  

    @property
    def available_copies(self):
        """Getter dla liczby dostępnych sztuk."""
        return self._available_copies

    def borrow(self):
        """Zmniejsza liczbę dostępnych sztuk, jeśli to możliwe."""
        if self._available_copies > 0:
            self._available_copies -= 1
            return True
        return False

    def __str__(self):
        """Magiczna metoda (dunder) do ładnego wyświetlania książki."""
        return f"'{self.title}' autorstwa: {self.author} (Dostępne: {self.available_copies}/{self.total_copies})"


class User:
    def __init__(self, login, password, role):
        self._login = login        
        self._password = password  
        self.role = role

    @property
    def login(self):
        return self._login

    def authenticate(self, password):
        """Sprawdza, czy podane hasło jest poprawne."""
        return self._password == password

    def menu(self, library):
        """Metoda, która zostanie nadpisana przez klasy pochodne (Polimorfizm)."""
        pass


class Reader(User):
    def __init__(self, login, password):
        super().__init__(login, password, "czytelnik")  # Dziedziczenie z klasy User
        self.borrowed_books = []  # Lista przechowująca obiekty klasy Book

    def menu(self, library):
        """Menu specyficzne dla czytelnika."""
        while True:
            print(f"\n--- MENU CZYTELNIKA ({self.login}) ---")
            print("1. Przeglądaj katalog")
            print("2. Wypożycz książkę")
            print("3. Moje wypożyczenia")
            print("4. Poproś o przedłużenie książki")
            print("5. Wyloguj")
            
            wybor = input("Wybierz opcję (1-5): ")
            if wybor == '1':
                library.show_catalog()
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
        """Menu specyficzne dla bibliotekarza."""
        while True:
            print(f"\n--- MENU BIBLIOTEKARZA ({self.login}) ---")
            print("1. Przeglądaj katalog")
            print("2. Lista wszystkich wypożyczeń")
            print("3. Obsługa próśb o przedłużenie")
            print("4. Wyloguj")
            
            wybor = input("Wybierz opcję (1-4): ")
            if wybor == '1':
                library.show_catalog()
            elif wybor == '2':
                library.show_all_borrows()
            elif wybor == '3':
                library.handle_extensions()
            elif wybor == '4':
                print("Wylogowano.")
                break
            else:
                print("Nieprawidłowy wybór.")


class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.extension_requests = []  # Przechowuje słowniki z prośbami o przedłużenie

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    def login_system(self):
        """Obsługuje proces logowania."""
        proby = 0
        while proby < 3:
            login = input("Podaj login: ")
            haslo = input("Podaj hasło: ")
            
            for user in self.users:
                if user.login == login and user.authenticate(haslo):
                    print(f"\nZalogowano pomyślnie. Rola: {user.role.upper()}")
                    return user
            
            proby += 1
            print(f"Błędne dane. Pozostało prób: {3 - proby}\n")
            
        print("Przekroczono limit prób logowania.")
        return None

    def show_catalog(self):
        print("\n=== KATALOG BIBLIOTEKI ===")
        for book in self.books:
            print(book)  
        print("==========================")

    def borrow_book(self, reader):
        tytul = input("Podaj dokładny tytuł książki, którą chcesz wypożyczyć: ")
        for book in self.books:
            if book.title.lower() == tytul.strip().lower():
                if book.borrow():
                    reader.borrowed_books.append(book)
                    print(f"Sukces! Wypożyczono '{book.title}'.")
                else:
                    print(f"Brak wolnych egzemplarzy '{book.title}'.")
                return
        print("Nie znaleziono takiej książki.")

    def show_user_borrows(self, reader):
        print("\n--- MOJE WYPOŻYCZENIA ---")
        if not reader.borrowed_books:
            print("Brak wypożyczonych książek.")
        else:
            for i, book in enumerate(reader.borrowed_books, 1):
                print(f"{i}. {book.title} ({book.author})")

    def request_extension(self, reader):
        self.show_user_borrows(reader)
        if not reader.borrowed_books:
            return
            
        tytul = input("Podaj tytuł książki, którą chcesz przedłużyć: ")
        for book in reader.borrowed_books:
            if book.title.lower() == tytul.strip().lower():
                self.extension_requests.append({"czytelnik": reader, "ksiazka": book})
                print(f"Wysłano prośbę o przedłużenie książki '{book.title}'.")
                return
        print("Nie masz takiej książki w wypożyczeniach.")

    def show_all_borrows(self):
        print("\n=== WSZYSTKIE WYPOŻYCZENIA (WIDOK BIBLIOTEKARZA) ===")
        znaleziono = False
        for user in self.users:
            if isinstance(user, Reader) and user.borrowed_books:
                for book in user.borrowed_books:
                    znaleziono = True
                    print(f"Użytkownik: {user.login} | Książka: '{book.title}'")
        if not znaleziono:
            print("Obecnie nikt nie ma wypożyczonych książek.")

    def handle_extensions(self):
        print("\n=== PROŚBY O PRZEDŁUŻENIE ===")
        if not self.extension_requests:
            print("Brak oczekujących próśb.")
            return

        for prosba in self.extension_requests[:]:
            czytelnik = prosba["czytelnik"]
            ksiazka = prosba["ksiazka"]
            print(f"\nCzytelnik {czytelnik.login} prosi o przedłużenie '{ksiazka.title}'.")
            decyzja = input("Zaakceptować? (t/n): ").lower()
            
            if decyzja == 't':
                print("Przedłużono pomyślnie.")
            else:
                print("Odrzucono prośbę.")
            
            self.extension_requests.remove(prosba)



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

    print("Witamy w Obiektowym Systemie Bibliotecznym!")
    
    while True:
        aktywny_uzytkownik = moja_biblioteka.login_system()
        if aktywny_uzytkownik:
            aktywny_uzytkownik.menu(moja_biblioteka)
        else:
            break

if __name__ == "__main__":
    main()