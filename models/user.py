# models/user.py
class Pengguna:
    def __init__(self, nama, id_pengguna):
        self.nama = nama
        self.id_pengguna = id_pengguna
        self.buku_pinjam = []

    def pinjam_buku(self, buku):
        if len(self.buku_pinjam) < 2:
            self.buku_pinjam.append(buku)
            buku.pinjam()
            print(f"{self.nama} berhasil meminjam buku '{buku.judul}'.")
        else:
            print(f"{self.nama} sudah meminjam 2 buku.")
    
    def kembalikan_buku(self, buku):
        if buku in self.buku_pinjam:
            self.buku_pinjam.remove(buku)
            buku.kembalikan()
            print(f"{self.nama} berhasil mengembalikan buku '{buku.judul}'.")
        else:
            print(f"{self.nama} tidak meminjam buku ini.")
