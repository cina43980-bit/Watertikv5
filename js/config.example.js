// 🔒 API key diisi dari GitHub Secrets
// Jangan edit file ini, nanti diisi otomatis oleh GitHub Actions

const CONFIG = {
    firebase: {
        apiKey: "ISI_DARI_SECRETS",
        authDomain: "ISI_DARI_SECRETS",
        projectId: "ISI_DARI_SECRETS",
        storageBucket: "ISI_DARI_SECRETS",
        messagingSenderId: "ISI_DARI_SECRETS",
        appId: "ISI_DARI_SECRETS"
    },
    cerebras: {
        apiKey: "ISI_DARI_SECRETS",
        apiUrl: "ISI_DARI_SECRETS",
        model: "ISI_DARI_SECRETS"
    },
    tiktok: {
        apiUrl: "ISI_DARI_SECRETS"
    }
};

// JANGAN UBAH KODE DI BAWAH INI!
window.__CONFIG = CONFIG;
console.log('⏳ Menunggu config dari GitHub Secrets...');
