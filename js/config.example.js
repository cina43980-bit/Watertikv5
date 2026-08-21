// 🔒 Konfigurasi WaterTik API
// Arahkan ke backend Python yang sedang jalan di HP (http://127.0.0.1:8000)

const BACKEND_URL = "http://127.0.0.1:8000";

const CONFIG = {
    // Backend API yang kamu buat di Main.py
    api: {
        tiktok: `${BACKEND_URL}/api/tiktok`,
        ai: `${BACKEND_URL}/api/ask-ai`
    },
    
    // Tetap simpan jika ada fitur lain yang masih butuh
    firebase: {
        apiKey: "GANTI_DENGAN_KEY_FIREBASE_KAMU",
        authDomain: "water-tik.firebaseapp.com",
        // ... (sisanya sesuai kebutuhanmu)
    }
};

// JANGAN UBAH KODE DI BAWAH INI!
window.__CONFIG = CONFIG;
console.log('✅ Konfigurasi dimuat, tersambung ke:', BACKEND_URL);
