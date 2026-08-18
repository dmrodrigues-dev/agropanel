let API_URL;

if (["localhost", "127.0.0.1"].includes(window.location.hostname)) {
  API_URL = "http://localhost:5000";
} else {
  API_URL = "https://agropanel.onrender.com";
}

window.API_URL = API_URL;
