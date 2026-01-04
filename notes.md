## Keputusan Desain Utama

Saya memisahkan kode yang awalnya berada dalam satu file besar (`main.py`) menjadi beberapa folder dan file yang lebih kecil berdasarkan tugas masing-masing. Tujuannya adalah setiap bagian dapat dikembangkan dan diperbaiki secara terpisah tanpa memengaruhi bagian lain.

Dalam refactor ini, struktur project dibagi menjadi tiga folder utama:

- **`api/`**  
  Berisi `endpoints.py` yang bertanggung jawab untuk menerima HTTP request dari pengguna dan mengembalikan response.

- **`services/`**  
  Berisi logic inti aplikasi, seperti `embedding.py` untuk mengubah teks menjadi embedding dan `rag_system.py` untuk mengatur alur kerja retrieval document dan pembuatan jawaban.

- **`storage/`**  
  Berisi `document_store.py` yang menangani penyimpanan dan pencarian dokumen menggunakan Qdrant maupun fallback in-memory.

Selain itu, saya menambahkan file **`models.py`** untuk membuat struktur data (request dan response) menggunakan Pydantic. Hal ini memastikan validasi data yang konsisten dan membuat kontrak API lebih jelas.

Dengan pemisahan bagian-bagian ini, setiap bagian aplikasi memiliki peran yang jelas. Jika terjadi bug atau perubahan pada satu bagian (misalnya storage), perbaikan dapat dilakukan secara spesifik tanpa perlu memeriksa seluruh kode, sehingga meningkatkan maintainability dan keterbacaan aplikasi secara keseluruhan.


## Trade-off yang Dipertimbangkan
Saya mempertimbangkan untuk membuat lebih banyak folder, misalnya memisahkan config untuk konfigurasi, utils untuk helper functions, atau tests untuk unit tests. Folder config akan berisi pengaturan aplikasi seperti URL database, ukuran vector, nama collection, dan konfigurasi lain yang berbeda antar environment tanpa perlu mengubah kode. Folder utils akan berisi function-function yang dipakai berulang kali, misalnya function untuk format waktu, generate random ID, atau validasi input. Folder tests akan berisi file-file untuk testing otomatis yang memastikan setiap bagian aplikasi bekerja dengan benar, misalnya test apakah add_document benar-benar menyimpan data, atau apakah search_documents mengembalikan hasil yang tepat sehingga ketika ada perubahan kode, saya dan developer lain bisa langsung tahu apakah ada bug atau tidak. Namun saya putuskan untuk tidak melakukannya karena project masih kecil dan keterbatasan waktu. Menurut saya, struktur saat ini sudah cukup untuk project ini.

## Peningkatan dari Sisi Maintainability

### Kondisi Sebelum Refactoring
Sebelum dilakukan refactoring, seluruh kode berada dalam satu file `main.py` yang panjang. Aplikasi menggunakan variabel global yang dapat diakses dan diubah dari berbagai bagian kode, sehingga alur kerja data sulit dipahami ketika proses debugging. Function-function tidak tersusun dengan rapi dan saling bergantung satu sama lain. Untuk menemukan atau memahami bagian tertentu, developer harus membaca dan melakukan scroll pada satu file yang besar dan komplesk. Hal ini juga membuat proses testing menjadi sulit karena seluruh bagian sistem saling bergantung karena berada didalam 1 file dan tidak dapat diuji secara terpisah.

### Kondisi Setelah Refactoring
Setelah refactoring, kode dipisah ke dalam beberapa folder dan file python dengan tugas yang jelas dan berbeda-beda. Setiap bagian utama dipisahkan sesuai perannya, seperti API layer, business logic, dan data access. Variabel global dihilangkan dan digantikan dengan dependency injection (menyediakan komponen yang dibutuhkan) melalui constructor, sehingga komponen yang diperlukan menjadi jelas dan mudah dilacak. Struktur ini memudahkan proses testing karena setiap komponen dapat diuji secara terpisah dengan menggunakan data palsu/dummy. Developer baru dapat dengan cepat memahami arsitektur aplikasi dan mengetahui lokasi yang tepat untuk melakukan perubahan. Perubahan pada satu bagian tidak akan memengaruhi bagian lain selama format (Nama fungsi/method, parameter yang diterima, return value) tetap sama. Secara keseluruhan kode menjadi lebih mudah dibaca, dimodifikasi, dan di-maintain dalam jangka panjang.
