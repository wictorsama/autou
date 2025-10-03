const CACHE_NAME = 'autou-v1.0.0';
const urlsToCache = [
  '/',
  '/static/styles.css',
  '/static/app.js',
  '/static/manifest.json',
  'https://cdn.tailwindcss.com',
  'https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js'
];

// Instalar Service Worker
self.addEventListener('install', event => {
  console.log('Service Worker: Instalando...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Service Worker: Cache aberto');
        return cache.addAll(urlsToCache);
      })
      .catch(err => console.log('Service Worker: Erro ao cachear', err))
  );
});

// Ativar Service Worker
self.addEventListener('activate', event => {
  console.log('Service Worker: Ativando...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: Removendo cache antigo', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Interceptar requisições
self.addEventListener('fetch', event => {
  // Estratégia: Cache First para recursos estáticos
  if (event.request.url.includes('/static/') || 
      event.request.url.includes('cdn.tailwindcss.com') ||
      event.request.url.includes('unpkg.com')) {
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          if (response) {
            return response;
          }
          return fetch(event.request)
            .then(response => {
              if (!response || response.status !== 200 || response.type !== 'basic') {
                return response;
              }
              const responseToCache = response.clone();
              caches.open(CACHE_NAME)
                .then(cache => {
                  cache.put(event.request, responseToCache);
                });
              return response;
            });
        })
    );
  }
  // Estratégia: Network First para API calls
  else if (event.request.url.includes('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          // Se a resposta for bem-sucedida, cache ela
          if (response.status === 200) {
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });
          }
          return response;
        })
        .catch(() => {
          // Se falhar, tenta buscar no cache
          return caches.match(event.request)
            .then(response => {
              if (response) {
                return response;
              }
              // Retorna uma resposta offline personalizada
              return new Response(
                JSON.stringify({
                  error: 'Sem conexão com a internet',
                  offline: true,
                  message: 'Esta funcionalidade requer conexão com a internet'
                }),
                {
                  status: 503,
                  statusText: 'Service Unavailable',
                  headers: {
                    'Content-Type': 'application/json'
                  }
                }
              );
            });
        })
    );
  }
  // Para outras requisições, usa a estratégia padrão
  else {
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          return response || fetch(event.request);
        })
    );
  }
});

// Notificações push (para futuras implementações)
self.addEventListener('push', event => {
  console.log('Service Worker: Push recebido', event);
  
  const options = {
    body: event.data ? event.data.text() : 'Nova notificação do AutoU',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Abrir AutoU',
        icon: '/static/icons/icon-96x96.png'
      },
      {
        action: 'close',
        title: 'Fechar',
        icon: '/static/icons/icon-96x96.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('AutoU', options)
  );
});

// Clique em notificações
self.addEventListener('notificationclick', event => {
  console.log('Service Worker: Notificação clicada', event);
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Sincronização em background (para futuras implementações)
self.addEventListener('sync', event => {
  console.log('Service Worker: Sync event', event);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(
      // Implementar lógica de sincronização
      console.log('Executando sincronização em background')
    );
  }
});

// Mensagens do cliente
self.addEventListener('message', event => {
  console.log('Service Worker: Mensagem recebida', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME });
  }
});

// Atualização do Service Worker
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'UPDATE_FOUND') {
    console.log('Service Worker: Nova versão disponível');
    // Notificar o cliente sobre a atualização
    self.clients.matchAll().then(clients => {
      clients.forEach(client => {
        client.postMessage({
          type: 'UPDATE_AVAILABLE',
          message: 'Nova versão disponível. Recarregue a página para atualizar.'
        });
      });
    });
  }
});