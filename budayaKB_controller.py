#!/usr/bin/env python3
"""

TEMPLATE TP4 DDP1 Semester Gasal 2019/2020

Author: 
Ika Alfina (ika.alfina@cs.ui.ac.id)
Evi Yulianti (evi.yulianti@cs.ui.ac.id)
Meganingrum Arista Jiwanggi (meganingrum@cs.ui.ac.id)

Gita Permatasari Sujatmiko (gita.permatasari91@ui.ac.id)

Nama		: Gita Permatasari Sujatmiko
Kelas		: DDP1-C
Kode Asods	: YAS

"""
from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template
import string

app = Flask(__name__)
app.secret_key ="tp4"

#inisialisasi objek budayaData
databasefilename = ""
budayaData = BudayaCollection()

#merender tampilan default(index.html)
@app.route('/')
def index():
	index_page = True
	return render_template("index.html", index_page=index_page)

# Bagian ini adalah implementasi fitur Impor Budaya, yaitu:
# - merender tampilan saat menu Impor Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Import Data" diklik
# - menampilkan notifikasi bahwa data telah berhasil diimport 	
@app.route('/imporBudaya', methods=['GET', 'POST'])
def importData():
	if request.method == "GET":
		return render_template("imporBudaya.html")
	elif request.method == "POST":
		f = request.files['file']
		global databasefilename
		databasefilename=f.filename
		try:
			if databasefilename[-3:] == "csv":	# hanya bisa file berformat csv
				budayaData.importFromCSV(f.filename)
				n_data = len(budayaData.koleksi)
				error = False
			else:	# selain file berformat csv tidak bisa
				error = True
		except FileNotFoundError:	# file di directory beda dengan controller juga tidak bisa
			error = True
		
		try:
			return render_template("imporBudaya.html", result=n_data, fname=f.filename, error=error)
		except UnboundLocalError:
			return render_template("imporBudaya.html", fname=f.filename, error=error)

# Bagian ini adalah implementasi fitur Tambah Budaya, yaitu:
# - merender tampilan saat menu Tambah Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Tambah Data" diklik
# - jika data belum ada dalam sistem maka akan menampilkan notifikasi bahwa data telah berhasil ditambahkan
# - jika data sudah ada dalam sistem atau input dari user berupa whitespace maka akan menampilkan notif bahwa data tidak berhasil ditambahkan
# - jika data masih kosong, akan menampilkan notifikasi bahwa data masih kosong
@app.route('/tambahBudaya', methods=['GET', 'POST'])
def tambahBudaya():
	if request.method == "GET":
		return render_template("tambahBudaya.html")
	elif request.method == "POST":
		nama, tipe, prov, url = request.form['nama'], request.form['tipe'], request.form['prov'], request.form['url']
		nama, tipe, prov = nama.strip().title(), tipe.strip().title(), prov.strip().title()
		if nama not in budayaData.koleksi and nama not in string.whitespace and tipe not in string.whitespace and prov not in string.whitespace:
			budayaData.tambah(nama, tipe, prov, url)
			added = True
		elif nama in string.whitespace or tipe in string.whitespace or prov in string.whitespace:
			added = "whitespace detected"
		else:
			added = False
		n_data = len(budayaData.koleksi)
		try:
			budayaData.exportToCSV(databasefilename)
		except FileNotFoundError:
			pass
		return render_template("tambahBudaya.html", result=n_data, namaBudaya=nama, added=added)

# Bagian ini adalah implementasi fitur Ubah Budaya, yaitu:
# - merender tampilan saat menu Ubah Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Ubah Data" diklik
# - jika data ada dalam sistem maka akan menampilkan notifikasi bahwa data telah berhasil diubah
# - jika data tidak ada dalam sistem maka akan menampilkan notif bahwa data tidak berhasil diubah
# - jika data masih kosong, akan menampilkan notifikasi bahwa data masih kosong
@app.route('/ubahBudaya', methods=['GET', 'POST'])
def ubahBudaya():
	if request.method == "GET":
		return render_template("ubahBudaya.html")
	elif request.method == "POST":
		nama, tipe, prov, url = request.form['nama'], request.form['tipe'], request.form['prov'], request.form['url']
		nama, tipe, prov = nama.strip().title(), tipe.strip().title(), prov.strip().title()
		changed = budayaData.ubah(nama, tipe, prov, url)
		n_data = len(budayaData.koleksi)
		try:
			budayaData.exportToCSV(databasefilename)
		except FileNotFoundError:
			pass
		return render_template("ubahBudaya.html", result=n_data, namaBudaya=nama, changed=changed)

# Bagian ini adalah implementasi fitur Hapus Budaya, yaitu:
# - merender tampilan saat menu Hapus Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Hapus Data" diklik
# - jika data ada salam sistem maka akan menampilkan notifikasi bahwa data telah berhasil dihapus
# - jika data tidak ada dalam sistem maka akan menampilkan notif bahwa data tidak berhasil dihapus
# - jika data masih kosong, akan menampilkan notifikasi bahwa data masih kosong
@app.route('/hapusBudaya', methods=['GET', 'POST'])
def hapusBudaya():
	if request.method == "GET":
		return render_template("hapusBudaya.html")
	elif request.method == "POST":
		nama = request.form['nama']
		nama = nama.strip().title()
		hapus = budayaData.hapus(nama)
		n_data = len(budayaData.koleksi)
		try:
			budayaData.exportToCSV(databasefilename)
		except FileNotFoundError:
			pass
		return render_template("hapusBudaya.html", result=n_data, hapus=hapus, namaBudaya=nama)

# Bagian ini adalah implementasi fitur Cari Budaya, yaitu:
# - merender tampilan saat menu Cari Budaya diklik	
# - melakukan pemrosesan terhadap isian form dengan kriteria yang dipilih setelah tombol "Cari" diklik
# - jika data yang dicari ada dalam sistem maka akan menampilkan notifikasi berapa banyak data yang ditemukan dan tabel berisi kumpulan data yang dicari
# - jika data yang dicari tidak ada dalam sistem maka akan menampilkan notifikasi bahwa data tidak ada dalam sistem
# - jika data masih kosong, akan menampilkan notifikasi bahwa data masih kosong
@app.route('/cariBudaya', methods=['GET', 'POST'])
def cariBudaya():
	if request.method == "GET":
		return render_template("cariBudaya.html")
	elif request.method == "POST":
		kriteria = request.form.get('kriteria')
		user_input = request.form['user_input']
		if kriteria == 'nama':
			data = budayaData.cariByNama(user_input)
		elif kriteria == 'tipe':
			data = budayaData.cariByTipe(user_input)
		elif kriteria == 'prov':
			data = budayaData.cariByProv(user_input)
		data_len = len(data)
		n_data = len(budayaData.koleksi)
		return render_template("cariBudaya.html", result=n_data, data=data, data_len=data_len, user_input=user_input, kriteria=kriteria)

# Bagian ini adalah implementasi fitur Statistik Budaya, yaitu:
# - merender tampilan saat menu Statistik Budaya diklik	
# - melakukan pemrosesan terhadap isian form (select) setelah tombol "Tampilkan" diklik
# - jika yang dipilih oleh user adalah 'All' maka akan menampilkan banyaknya data budaya yang ada dalam sistem
# - jika yang dipilih oleh user adalah 'Tipe Budaya' maka akan menampilkan tabel berisi masing-masing tipe budaya dengan jumlahnya dalam sistem
# - jika yang dipilih oleh user adalah 'Asal Provinsi Budaya' maka akan menampilkan tabel berisi masing-masing asal prov budaya dengan jumlahnya dalam sistem
# - jika data masih kosong, akan menampilkan notifikasi bahwa data masih kosong
@app.route('/statsBudaya', methods=['GET', 'POST'])
def statBudaya():
	if request.method == "GET":
		return render_template("statBudaya.html")
	elif request.method == "POST":
		kriteria = request.form.get('kriteria')
		if kriteria == 'all':
			data = budayaData.stat()
			sorted_jml = None
		elif kriteria == 'tipe':
			data = budayaData.statByTipe()
			sorted_jml = sorted(data.items(), key = lambda k:(k[1], k[0]))[::-1]
		elif kriteria == 'prov':
			data = budayaData.statByProv()
			sorted_jml = sorted(data.items(), key = lambda k:(k[1], k[0]))[::-1]

		data_is_dict = isinstance(data, dict)
		n_data = len(budayaData.koleksi)
		return render_template("statBudaya.html", result=n_data, data=data, data_is_dict=data_is_dict, sorted_jml=sorted_jml, kriteria=kriteria)

# run main app
if __name__ == "__main__":
	app.run()
