const CACHE = 'numero1-v10';
const FILES = [
  './',
  './index.html',
  './privacy.html',
  './manifest.webmanifest',
  './robots.txt',
  './sitemap.xml',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
  './apple-touch-icon.png',
  './favicon-64.png',
  './mappa.jpg',
  './mappa-480.jpg',
  './ill-pizza.svg',
  './ill-forno.svg',
  './ill-kebab.svg',
  './foto-capricciosa-400.jpg',
  './foto-capricciosa.jpg',
  './foto-diavola-400.jpg',
  './foto-diavola.jpg',
  './foto-margherita-400.jpg',
  './foto-margherita.jpg',
  './th-capricciosa.jpg',
  './th-contadina.jpg',
  './th-diavola.jpg',
  './th-margherita.jpg',
  './th-napoli.jpg',
  './th-prosciutto-e-funghi.jpg',
  './th-quattro-formaggi.jpg',
  './th-quattro-stagioni.jpg',
  './th-marinara.jpg',
  './th-rucola.jpg',
  './th-calzone-liscio.jpg',
  './th-prosciutto.jpg',
  './th-pugliese.jpg',
  './th-patatine.jpg',
  './th-romana.jpg',
  './th-salsiccia.jpg',
  './th-salame-dolce.jpg',
  './th-wurstel.jpg',
  './th-calabrese.jpg',
  './th-carciofi.jpg',
  './th-parmigiana.jpg',
  './th-campagnola.jpg',
  './th-carbonara.jpg',
  './th-calzone-farcito.jpg',
  './th-occhio-di-bue.jpg',
  './th-messicana.jpg',
  './th-taranto.jpg',
  './th-pepericcia.jpg',
  './th-rustica.jpg',
  './th-zucchine-e-zola.jpg'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  if (new URL(req.url).origin !== location.origin) return;

  e.respondWith(
    fetch(req)
      .then((res) => {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(req, copy));
        return res;
      })
      .catch(() => caches.match(req).then((hit) => hit || caches.match('./index.html')))
  );
});
