from controllers.library import Library

def main_menu():
    library = Library('data/books.json')  # Buat instance library
    # Menampilkan menu atau melakukan operasi lainnya
    while True:
        print("Menu:")
        print("1. Daftar Buku")
        print("2. Pinjam Buku")
        print("3. Kembalikan Buku")
        print("4. Keluar")
        choice = input("Pilih opsi: ")

        if choice == '1':
            show_books(library)
        elif choice == '2':
            borrow_book(library)
        elif choice == '3':
            return_book(library)
        elif choice == '4':
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def show_books(library):
    # Logika untuk menampilkan daftar buku
    pass

def borrow_book(library):
    # Logika untuk meminjam buku
    pass

def return_book(library):
    # Logika untuk mengembalikan buku
    pass

if __name__ == "__main__":
    main_menu()
