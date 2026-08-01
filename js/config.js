const CONFIG = {
  firebase: {
    apiKey: 'AIzaSyCQZ-ce5I9-5UvD19cPK6qKj8kIXaMhOek',
    authDomain: ' watertik-466a0.firebaseapp.com',
    projectId: 'watertik-466a0',
    storageBucket: 'watertik-466a0.firebasestorage.app',
    messagingSenderId: '477111819819',
    appId: '1:477111819819:web:09626fc68a93f6b372146e'
  },
  cerebras: {
    apiKey: 'csk-xvn333y8eyfyvc93kv44xdrxpxwf65h6tyn3de34vxf9nfy9',
    apiUrl: 'https://api.cerebras.ai/v1/chat/completions',
    model: ' zai-glm-4.7'
  },
  tiktok: {
    apiUrl: 'https://www.tikwm.com/api/'
  }
};
window.__CONFIG = CONFIG;
console.log('Config loaded');
