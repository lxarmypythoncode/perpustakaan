class Buku:
    def __init__(self, judul, pengarang, tahun_terbit, dipinjam=False):
        self.judul = judul
        self.pengarang = pengarang
        self.tahun_terbit = tahun_terbit
        self.dipinjam = dipinjam

    def pinjam(self):
        if not self.dipinjam:
            self.dipinjam = True
            print(f"Buku {self.judul} berhasil dipinjam.")
        else:
            print(f"Buku {self.judul} sedang dipinjam.")

    def kembalikan(self):
        if self.dipinjam:
            self.dipinjam = False
            print(f"Buku {self.judul} berhasil dikembalikan.")
        else:
            print(f"Buku {self.judul} tidak sedang dipinjam.")
