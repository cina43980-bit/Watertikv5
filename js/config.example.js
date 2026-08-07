// File ini cuma contoh, API key diisi otomatis oleh GitHub Actions
const CONFIG = {
    firebase: {
        apiKey: "ISI_API_KEY",
        authDomain: "ISI_AUTH_DOMAIN",
        projectId: "ISI_PROJECT_ID",
        storageBucket: "ISI_STORAGE_BUCKET",
        messagingSenderId: "ISI_SENDER_ID",
        appId: "ISI_APP_ID"
    },
    cerebras: {
        apiKey: "ISI_API_KEY",
        apiUrl: "ISI_API_URL",
        model: "ISI_MODEL"
    },
    tiktok: {
        apiUrl: "ISI_TIKTOK_API_URL"
    }
};
window.__CONFIG = CONFIG;
