import tkinter as tk
from tkinter import messagebox

class KnowledgeBase:
    def __init__(self):
        self.interpretasi_gejala = {
            'G1': 'Demam',
            'G2': 'Batuk',
            'G3': 'Pilek',
            'G4': 'Ruam',
            'G5': 'Gatal',
            'G6': 'Muntah',
            'G7': 'Diare',
            'G8': 'Lelah',
            'G9': 'Sesak Napas',
            'G10': 'Wheezing',
            'G11': 'Iritabilitas',
            'G12': 'Hilang Nafsu Makan',
            'G13': 'Sakit Tenggorokan',
            'G14': 'Hidung Tersumbat',
            'G15': 'Bersin'
        }

        self.interpretasi_penyakit = {
            'P1': 'Flu',
            'P2': 'Campak',
            'P3': 'Gastroenteritis',
            'P4': 'Asma',
            'P5': 'Tipes',
            'P6': 'Radang Tenggorokan',
            'P7': 'Rhinitis',
            'P8': 'Cacar Air',
            'P9': 'DBD'
        }

    def get_interpretasi_gejala(self, kode_gejala):
        return self.interpretasi_gejala.get(kode_gejala, 'Gejala Tidak Dikenal')

    def get_interpretasi_penyakit(self, kode_penyakit):
        return self.interpretasi_penyakit.get(kode_penyakit, 'Penyakit Tidak Dikenal')

class RuleBase:
    def __init__(self):
        self.rules = [
            Aturan(['G1', 'G2', 'G3'], 'P1'),
            Aturan(['G1', 'G4', 'G5'], 'P2'),
            Aturan(['G6', 'G7', 'G8'], 'P3'),
            Aturan(['G2', 'G9', 'G10'], 'P4'),
            Aturan(['G1', 'G11', 'G12'], 'P5'),
            Aturan(['G1', 'G2', 'G13'], 'P6'),
            Aturan(['G1', 'G14', 'G15'], 'P7'),
            Aturan(['G1', 'G13', 'G4'], 'P8'),
            Aturan(['G6', 'G1', 'G12'], 'P9'),
        ]

class Aturan:
    def __init__(self, kode_gejala, kode_penyakit):
        self.kode_gejala = kode_gejala
        self.kode_penyakit = kode_penyakit

class GUIExpertSistemDiagnostik:
    def __init__(self, master, knowledge_base, rule_base):
        self.master = master
        self.master.title("Sistem Pakar Diagnostik")
        self.master.geometry("550x550")

        self.knowledge_base = knowledge_base
        self.rule_base = rule_base

        self.var_gejala = {kode_gejala: tk.BooleanVar() for aturan in self.rule_base.rules for kode_gejala in aturan.kode_gejala}
        self.buat_gui()

    def buat_gui(self):
        background_color = "#ECECEC"
        widget_color = "#FFFFFF"
        text_color = "#333333"

        self.master.configure(bg=background_color)

        label_judul = tk.Label(self.master, text="Sistem Pakar Diagnostik", font=("Arial", 24, "bold"), bg=background_color, fg="#009688")
        label_judul.pack(pady=10)

        frame_gejala = tk.Frame(self.master, bg=background_color)
        frame_gejala.pack(padx=10, pady=5)

        gejala_list = list(set(kode_gejala for aturan in self.rule_base.rules for kode_gejala in aturan.kode_gejala))
        half_length = len(gejala_list) // 2

        for i, kode_gejala in enumerate(gejala_list):
            text_gejala = self.knowledge_base.get_interpretasi_gejala(kode_gejala)
            row = i % half_length
            column = 0 if i < half_length else 1

            label_gejala = tk.Label(frame_gejala, text=text_gejala, font=("Arial", 12), bg=background_color, fg=text_color, wraplength=150, justify="left")
            label_gejala.grid(row=row, column=column * 2, padx=10, pady=2, sticky="w")

            checkbox = tk.Checkbutton(frame_gejala, variable=self.var_gejala[kode_gejala], font=("Arial", 12), bg=background_color, fg=text_color, selectcolor=widget_color, activebackground=background_color, activeforeground=text_color)
            checkbox.grid(row=row, column=column * 2 + 1, padx=10, pady=2, sticky="w")

        tombol_diagnosa = tk.Button(self.master, text="Diagnosa", command=self.diagnosa, font=("Arial", 14, "bold"), bg="#009688", fg="white", relief=tk.RAISED)
        tombol_diagnosa.pack(pady=20)

        self.label_hasil_diagnosa = tk.Label(self.master, text="", font=("Arial", 12), wraplength=500, justify="left", bg=background_color, fg=text_color)
        self.label_hasil_diagnosa.pack(pady=10)

    def tanya_gejala(self):
        return {kode_gejala: var.get() for kode_gejala, var in self.var_gejala.items()}

    def diagnosa(self):
        gejala_terpilih = self.tanya_gejala()

        if sum(gejala_terpilih.values()) < 3:
            warning_message = "Pilih minimal 3 gejala."
            self.label_hasil_diagnosa.config(text=warning_message, fg="red")
            messagebox.showwarning("Peringatan", warning_message)
        else:
            hasil_diagnosa = self.maju_berantai(gejala_terpilih)
            self.label_hasil_diagnosa.config(fg="black")
            self.tampilkan_hasil_diagnosa(hasil_diagnosa)

    def maju_berantai(self, gejala_terpilih):
        hasil = set()
        for aturan in self.rule_base.rules:
            if all(gejala_terpilih[kode_gejala] for kode_gejala in aturan.kode_gejala):
                hasil.add(aturan.kode_penyakit)
        return hasil

    def tampilkan_hasil_diagnosa(self, hasil):
        if hasil:
            teks_hasil = f"Berdasarkan gejala yang Anda sampaikan, kemungkinan penyakit adalah:\n{', '.join(self.knowledge_base.get_interpretasi_penyakit(kode_penyakit) for kode_penyakit in hasil)}"
        else:
            teks_hasil = "Tidak dapat menentukan penyakit berdasarkan gejala yang diberikan."

        self.label_hasil_diagnosa.config(text=teks_hasil)
        messagebox.showinfo("Hasil Diagnosa", teks_hasil)
class DatasetPercobaan:
    @staticmethod
    def get_dataset():
        # Dataset Percobaan dengan keterangan yang lebih deskriptif
        dataset_percobaan = [
            {'G1': 1, 'G2': 1, 'G3': 1, 'G4': 0, 'G5': 0, 'G6': 0, 'G7': 0, 'G8': 0, 'G9': 0, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 0, 'G15': 0},  # Dataset 1
            {'G1': 1, 'G2': 1, 'G3': 1, 'G4': 0, 'G5': 0, 'G6': 0, 'G7': 0, 'G8': 0, 'G9': 0, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 0, 'G15': 0},  # Dataset 2
            {'G1': 1, 'G2': 1, 'G3': 0, 'G4': 1, 'G5': 1, 'G6': 0, 'G7': 0, 'G8': 0, 'G9': 0, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 0, 'G15': 0},  # Dataset 3
            {'G1': 0, 'G2': 0, 'G3': 0, 'G4': 0, 'G5': 0, 'G6': 1, 'G7': 1, 'G8': 1, 'G9': 0, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 0, 'G15': 0},  # Dataset 4
            {'G1': 1, 'G2': 0, 'G3': 0, 'G4': 0, 'G5': 0, 'G6': 1, 'G7': 0, 'G8': 1, 'G9': 0, 'G10': 1, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 1, 'G15': 0},  # Dataset 5
            {'G1': 0, 'G2': 0, 'G3': 1, 'G4': 0, 'G5': 1, 'G6': 0, 'G7': 0, 'G8': 0, 'G9': 1, 'G10': 0, 'G11': 1, 'G12': 0, 'G13': 0, 'G14': 0, 'G15': 1},  # Dataset 6
            {'G1': 0, 'G2': 1, 'G3': 0, 'G4': 0, 'G5': 0, 'G6': 1, 'G7': 1, 'G8': 0, 'G9': 0, 'G10': 0, 'G11': 1, 'G12': 0, 'G13': 1, 'G14': 0, 'G15': 0},  # Dataset 7
            {'G1': 1, 'G2': 1, 'G3': 1, 'G4': 1, 'G5': 0, 'G6': 0, 'G7': 0, 'G8': 1, 'G9': 0, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 0, 'G15': 1},  # Dataset 8
            {'G1': 0, 'G2': 0, 'G3': 0, 'G4': 1, 'G5': 1, 'G6': 1, 'G7': 0, 'G8': 0, 'G9': 1, 'G10': 0, 'G11': 1, 'G12': 0, 'G13': 0, 'G14': 0, 'G15': 1},  # Dataset 9
            {'G1': 0, 'G2': 1, 'G3': 0, 'G4': 1, 'G5': 1, 'G6': 0, 'G7': 0, 'G8': 1, 'G9': 0, 'G10': 1, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 1, 'G15': 0},  # Dataset 10
            {'G1': 1, 'G2': 0, 'G3': 1, 'G4': 0, 'G5': 0, 'G6': 0, 'G7': 0, 'G8': 0, 'G9': 1, 'G10': 0, 'G11': 0, 'G12': 1, 'G13': 0, 'G14': 0, 'G15': 1},  # Dataset 11
            {'G1': 0, 'G2': 1, 'G3': 1, 'G4': 0, 'G5': 0, 'G6': 0, 'G7': 0, 'G8': 1, 'G9': 0, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 1, 'G15': 0},  # Dataset 12
            {'G1': 0, 'G2': 0, 'G3': 0, 'G4': 0, 'G5': 0, 'G6': 0, 'G7': 1, 'G8': 0, 'G9': 0, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 1, 'G14': 0, 'G15': 1},  # Dataset 13
            {'G1': 0, 'G2': 1, 'G3': 0, 'G4': 0, 'G5': 0, 'G6': 0, 'G7': 0, 'G8': 0, 'G9': 0, 'G10': 0, 'G11': 1, 'G12': 0, 'G13': 1, 'G14': 0, 'G15': 0},  # Dataset 14
            {'G1': 1, 'G2': 0, 'G3': 0, 'G4': 0, 'G5': 0, 'G6': 1, 'G7': 1, 'G8': 0, 'G9': 0, 'G10': 1, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 1, 'G15': 0},  # Dataset 15
            {'G1': 1, 'G2': 0, 'G3': 0, 'G4': 0, 'G5': 0, 'G6': 0, 'G7': 0, 'G8': 0, 'G9': 1, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 1, 'G14': 0, 'G15': 1},  # Dataset 16
            {'G1': 0, 'G2': 1, 'G3': 0, 'G4': 1, 'G5': 1, 'G6': 1, 'G7': 0, 'G8': 0, 'G9': 0, 'G10': 0, 'G11': 1, 'G12': 0, 'G13': 0, 'G14': 0, 'G15': 1},  # Dataset 17
            {'G1': 1, 'G2': 1, 'G3': 0, 'G4': 0, 'G5': 1, 'G6': 0, 'G7': 0, 'G8': 0, 'G9': 0, 'G10': 1, 'G11': 0, 'G12': 1, 'G13': 0, 'G14': 0, 'G15': 0},  # Dataset 18
            {'G1': 0, 'G2': 1, 'G3': 0, 'G4': 0, 'G5': 0, 'G6': 1, 'G7': 1, 'G8': 0, 'G9': 0, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 1, 'G14': 0, 'G15': 0},  # Dataset 19
            {'G1': 0, 'G2': 0, 'G3': 1, 'G4': 1, 'G5': 0, 'G6': 0, 'G7': 0, 'G8': 0, 'G9': 1, 'G10': 0, 'G11': 0, 'G12': 1, 'G13': 0, 'G14': 0, 'G15': 1},  # Dataset 20
            {'G1': 0, 'G2': 0, 'G3': 0, 'G4': 1, 'G5': 0, 'G6': 0, 'G7': 0, 'G8': 1, 'G9': 0, 'G10': 0, 'G11': 0, 'G12': 1, 'G13': 0, 'G14': 1, 'G15': 0},  # Dataset 21
            {'G1': 1, 'G2': 0, 'G3': 0, 'G4': 0, 'G5': 1, 'G6': 1, 'G7': 0, 'G8': 1, 'G9': 0, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 1, 'G15': 0},  # Dataset 22
            {'G1': 0, 'G2': 1, 'G3': 0, 'G4': 1, 'G5': 0, 'G6': 0, 'G7': 1, 'G8': 0, 'G9': 0, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 1, 'G14': 0, 'G15': 0},  # Dataset 23
            {'G1': 1, 'G2': 1, 'G3': 0, 'G4': 1, 'G5': 0, 'G6': 0, 'G7': 0, 'G8': 0, 'G9': 0, 'G10': 1, 'G11': 0, 'G12': 0, 'G13': 1, 'G14': 0, 'G15': 0},  # Dataset 24
            {'G1': 0, 'G2': 0, 'G3': 1, 'G4': 0, 'G5': 0, 'G6': 1, 'G7': 0, 'G8': 0, 'G9': 1, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 0, 'G15': 1},  # Dataset 25
            {'G1': 1, 'G2': 0, 'G3': 1, 'G4': 0, 'G5': 0, 'G6': 1, 'G7': 0, 'G8': 0, 'G9': 1, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 0, 'G15': 1},  # Dataset 26
            {'G1': 0, 'G2': 1, 'G3': 1, 'G4': 0, 'G5': 0, 'G6': 1, 'G7': 0, 'G8': 0, 'G9': 1, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 0, 'G15': 1},  # Dataset 27
            {'G1': 1, 'G2': 1, 'G3': 1, 'G4': 0, 'G5': 0, 'G6': 1, 'G7': 0, 'G8': 0, 'G9': 1, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 0, 'G15': 1},  # Dataset 28
            {'G1': 1, 'G2': 1, 'G3': 1, 'G4': 0, 'G5': 0, 'G6': 0, 'G7': 0, 'G8': 0, 'G9': 1, 'G10': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'G14': 0, 'G15': 1},  # Dataset 29
            {'G1': 1, 'G2': 1, 'G3': 1, 'G4': 1, 'G5': 0, 'G6': 1, 'G7': 0, 'G8': 0, 'G9': 1, 'G10': 0, 'G11': 0, 'G12': 1, 'G13': 0, 'G14': 1, 'G15': 1},  # Dataset 30
        ]
        return dataset_percobaan



if __name__ == "__main__":
    knowledge_base = KnowledgeBase()
    rule_base = RuleBase()

    root = tk.Tk()

    gui_sistem_pakar_diagnostik = GUIExpertSistemDiagnostik(root, knowledge_base, rule_base)

    dataset = DatasetPercobaan.get_dataset()
    for data in dataset:
        print("Gejala yang terpilih:", data)
        hasil_diagnosa = gui_sistem_pakar_diagnostik.maju_berantai(data)
        print("Hasil diagnosa:", hasil_diagnosa)
        print()
    root.mainloop()
