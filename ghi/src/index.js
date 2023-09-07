import React, {useEffect} from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import 'dotenv/config';


const SEARCH_API_KEY = process.env.REACT_APP_SEARCH_API_KEY;


function runGoogleMapsScript() {
((g) => {
var h,
a,
k,
p = "The Google Maps JavaScript API",
c = "google",
l = "importLibrary",
q = "__ib__",
m = document,
b = window;
b = b[c] || (b[c] = {});
var d = b.maps || (b.maps = {}),
r = new Set(),
e = new URLSearchParams(),
u = () =>
h ||
(h = new Promise(async (f, n) => {
await (a = m.createElement("script"));
e.set("libraries", [...r] + "");
for (k in g)
e.set(
k.replace(/[A-Z]/g, (t) => "_" + t[0].toLowerCase()),
g[k]
);
e.set("callback", c + ".maps." + q);
a.src = `https://maps.${c}apis.com/maps/api/js?` + e;
d[q] = f;
a.onerror = () => (h = n(Error(p + " could not load.")));
a.nonce = m.querySelector("script[nonce]")?.nonce || "";
m.head.append(a);
}));
d[l]
? console.warn(p + " only loads once. Ignoring:", g)
: (d[l] = (f, ...n) => r.add(f) && u().then(() => d[l](f, ...n)));
})({
key: SEARCH_API_KEY,
v: "weekly",
});

}


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
  
);

useEffect(() => {
  runGoogleMapsScript();
}, []);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
