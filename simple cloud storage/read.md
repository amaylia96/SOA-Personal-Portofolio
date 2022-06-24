SIMPLE CLOUD STORAGE
1. aktifkan gateway.py dan storage.py
2. untuk upload: 
	masuk ke postman, pilih metode POST -> 127.0.0.1/8000/api/upload
3. untuk cek file yang ingin di download:
	a. aktifkan python -m http.server 9000 di cmd
 	b. kembali ke postman, pilih metode POST -> 127.0.0.1/8000/api/download<nama_file>
	c. lalu copy urlnya (misal: 127.0.0.1:8000/api/download/gula.pdf) ke searchbar browser
	d. setelah itu akan muncul {"files": "http://127.0.0.1:9000/upload/gula.pdf"}, copy http://127.0.0.1:9000/upload/gula.pdf dan paste ke newtab
	e. setelah dicopy, maka akan keluar tampilan file yang sebelumnya diupload dan siap didownload