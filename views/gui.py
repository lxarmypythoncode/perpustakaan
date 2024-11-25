import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # add parent directory
import json
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.animation import Animation
from controllers.library import Library
from models.user import Pengguna


class LibraryApp(App):
    def build(self):
        self.library = Library('data/books.json')
        self.pengguna = None  # Pengguna yang login
        self.selected_book = None  # Buku yang dipilih

        # Atur ukuran window
        Window.size = (800, 600)

        # Layout utama (BoxLayout)
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Bagian header
        header_label = Label(text='Sistem Manajemen Perpustakaan', font_size=24, size_hint=(1, 0.1))
        main_layout.add_widget(header_label)

        # Tombol Login/Daftar
        login_button = Button(text="Login/Daftar", size_hint=(1, 0.1))
        login_button.bind(on_press=self.open_login_popup)
        main_layout.add_widget(login_button)

        # Layout untuk daftar buku dan fitur perpustakaan
        self.content_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.8))

        # Daftar Buku
        self.books_layout = BoxLayout(orientation='vertical')
        books_label = Label(text='Daftar Buku', font_size=18)
        self.books_layout.add_widget(books_label)

        # Scrollable list for book display
        self.books_list_label = Label(text=self.get_books_list(), halign='left', valign='top', size_hint_y=None)
        self.books_list_label.bind(size=self.books_list_label.setter('text_size'))  # Align text
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        scroll_view.add_widget(self.books_list_label)
        self.books_layout.add_widget(scroll_view)

        # Fungsi perpustakaan (cari, pinjam, kembalikan)
        self.functions_layout = GridLayout(cols=2, spacing=10, size_hint=(0.6, 1))

        # Input untuk pencarian, peminjaman, dan pengembalian
        self.search_input = TextInput(hint_text='Masukkan judul buku', size_hint=(1, 0.1))
        self.action_label = Label(text='Hasil tindakan akan muncul di sini', size_hint=(1, 0.2))

        # Tombol Cari Buku
        search_button = Button(text='Cari Buku', size_hint=(1, 0.2))
        search_button.bind(on_press=self.search_book)

        # Tombol Pinjam Buku
        borrow_button = Button(text='Pinjam Buku', size_hint=(1, 0.2))
        borrow_button.bind(on_press=self.open_borrow_form)

        # Tombol Kembalikan Buku
        return_button = Button(text='Kembalikan Buku', size_hint=(1, 0.2))
        return_button.bind(on_press=self.open_return_form)

        self.functions_layout.add_widget(self.search_input)
        self.functions_layout.add_widget(search_button)
        self.functions_layout.add_widget(borrow_button)
        self.functions_layout.add_widget(return_button)
        self.functions_layout.add_widget(self.action_label)

        # Efek animasi pada label action
        anim = Animation(opacity=0, duration=1)
        anim += Animation(opacity=1, duration=1)
        anim.repeat = True
        anim.start(self.action_label)

        self.content_layout.add_widget(self.books_layout)
        self.content_layout.add_widget(self.functions_layout)

        # Tambahkan layout buku dan fungsi perpustakaan ke layout utama
        main_layout.add_widget(self.content_layout)

        return main_layout

    def open_login_popup(self, instance):
        # Popup untuk login atau registrasi user
        layout = GridLayout(cols=2, padding=10)
        layout.add_widget(Label(text="Nama Pengguna"))
        self.username_input = TextInput()
        layout.add_widget(self.username_input)

        login_button = Button(text="Login")
        login_button.bind(on_press=self.login)
        layout.add_widget(login_button)

        close_button = Button(text="Tutup")
        close_button.bind(on_press=self.close_popup)
        layout.add_widget(close_button)

        self.popup = Popup(title="Login/Daftar", content=layout, size_hint=(0.6, 0.4))
        self.popup.open()

    def close_popup(self, instance):
        self.popup.dismiss()

    def login(self, instance):
        nama_pengguna = self.username_input.text
        if nama_pengguna:
            self.pengguna = Pengguna(nama_pengguna, id_pengguna=1)  # Dummy ID untuk sekarang
            self.action_label.text = f"Selamat datang, {nama_pengguna}!"
        else:
            self.action_label.text = "Nama pengguna tidak boleh kosong."
        self.popup.dismiss()

    def get_books_list(self):
        books = "\n".join([f"{buku.judul} oleh {buku.pengarang} - Tahun: {buku.tahun_terbit}" for buku in self.library.buku_list])
        return books if books else 'Tidak ada buku yang tersedia.'

    def search_book(self, instance):
        judul = self.search_input.text
        hasil = self.library.cari_buku(judul)

        if isinstance(hasil, str):
            self.action_label.text = hasil
        else:
            hasil_teks = "\n".join([f"{buku.judul} oleh {buku.pengarang}" for buku in hasil])
            self.action_label.text = hasil_teks

    def open_borrow_form(self, instance):
        if not self.pengguna:
            self.action_label.text = "Anda harus login dulu."
            return
        
        layout = GridLayout(cols=2, padding=10)
        layout.add_widget(Label(text="Judul Buku"))
        self.book_title_input = TextInput()
        layout.add_widget(self.book_title_input)

        borrow_button = Button(text="Pinjam")
        borrow_button.bind(on_press=self.borrow_book)
        layout.add_widget(borrow_button)

        close_button = Button(text="Tutup")
        close_button.bind(on_press=self.close_popup)
        layout.add_widget(close_button)

        self.popup = Popup(title="Formulir Peminjaman", content=layout, size_hint=(0.6, 0.4))
        self.popup.open()

    def borrow_book(self, instance):
        judul = self.book_title_input.text
        if judul:
            self.library.pinjam_buku(judul)
            self.action_label.text = f"Buku '{judul}' berhasil dipinjam."
            self.update_books_list()
        else:
            self.action_label.text = "Judul buku harus diisi."
        self.popup.dismiss()

    def open_return_form(self, instance):
        if not self.pengguna:
            self.action_label.text = "Anda harus login dulu."
            return

        layout = GridLayout(cols=2, padding=10)
        layout.add_widget(Label(text="Judul Buku"))
        self.book_title_input = TextInput()
        layout.add_widget(self.book_title_input)

        return_button = Button(text="Kembalikan")
        return_button.bind(on_press=self.return_book)
        layout.add_widget(return_button)

        close_button = Button(text="Tutup")
        close_button.bind(on_press=self.close_popup)
        layout.add_widget(close_button)

        self.popup = Popup(title="Formulir Pengembalian", content=layout, size_hint=(0.6, 0.4))
        self.popup.open()

    def return_book(self, instance):
        judul = self.book_title_input.text
        if judul:
            self.library.kembalikan_buku(judul)
            self.action_label.text = f"Buku '{judul}' berhasil dikembalikan."
            self.update_books_list()
        else:
            self.action_label.text = "Judul buku harus diisi."
        self.popup.dismiss()

    def update_books_list(self):
        self.books_list_label.text = self.get_books_list()


if __name__ == '__main__':
    LibraryApp().run()
