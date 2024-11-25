import json
from models.book import Buku

class Library:
    def __init__(self, data_file):
        self.data_file = data_file
        self.buku_list = self.load_books()

    def load_books(self):
        try:
            with open(self.data_file, 'r') as f:
                books_data = json.load(f)
            return [Buku(**data) for data in books_data]
        except FileNotFoundError:
            return []

    def save_books(self):
        with open(self.data_file, 'w') as f:
            json.dump([vars(buku) for buku in self.buku_list], f, indent=4)

    def tambah_buku(self, judul, pengarang, tahun_terbit):
        buku_baru = Buku(judul, pengarang, tahun_terbit)
        self.buku_list.append(buku_baru)
        self.save_books()
        print(f"Buku '{judul}' berhasil ditambahkan.")
        
    def cari_buku(self, judul):
        hasil_cari = [buku for buku in self.buku_list if judul.lower() in buku.judul.lower()]
        return hasil_cari if hasil_cari else "buku tidak ditemukan."

    def pinjam_buku(self, judul):
        for buku in self.buku_list:
            if buku.judul == judul:
                buku.pinjam()
                self.save_books()
                return
        print(f"Buku dengan judul '{judul}' tidak ditemukan.")

    def kembalikan_buku(self, judul):
        for buku in self.buku_list:
            if buku.judul == judul:
                buku.kembalikan()
                self.save_books()
                return
        print(f"Buku dengan judul '{judul}' tidak ditemukan.")
        
    def tampilkan_daftar_buku(self):
        if not self.buku_list:
            print("tidak ada buku yang tersedia")
        else: 
            print("\ndaftar buku di perpustakaan")
            for index, buku in enumerate(self.buku_list, start=1):
                print(f"{index}. judul: {buku.judul}, pengarang: {buku.pengarang}: tahun terbit: {buku.tahun_terbit}")