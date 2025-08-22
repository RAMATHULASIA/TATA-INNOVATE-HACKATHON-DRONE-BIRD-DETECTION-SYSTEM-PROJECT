// TATA AI Co-pilot Service Worker
const CACHE_NAME = 'tata-ai-copilot-v1.0.0';
const OFFLINE_URL = '/offline.html';

// Resources to cache for offline functionality
const STATIC_CACHE_URLS = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json',
  '/favicon.ico',
  OFFLINE_URL
];

// API endpoints that can work offline
const API_CACHE_URLS = [
  '/api/platforms',
  '/api/templates',
  '/api/status'
];

// Install event - cache static resources
self.addEventListener('install', (event) => {
  console.log('TATA AI Co-pilot Service Worker installing...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Caching static resources');
        return cache.addAll(STATIC_CACHE_URLS);
      })
      .then(() => {
        // Skip waiting to activate immediately
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('Failed to cache static resources:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('TATA AI Co-pilot Service Worker activating...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME) {
              console.log('Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        // Take control of all clients immediately
        return self.clients.claim();
      })
  );
});

// Fetch event - serve cached content when offline
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Handle navigation requests
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // If online, return the response and cache it
          const responseClone = response.clone();
          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(request, responseClone);
            });
          return response;
        })
        .catch(() => {
          // If offline, try to serve from cache
          return caches.match(request)
            .then((cachedResponse) => {
              if (cachedResponse) {
                return cachedResponse;
              }
              // Fallback to offline page
              return caches.match(OFFLINE_URL);
            });
        })
    );
    return;
  }

  // Handle API requests
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Cache successful API responses
          if (response.ok && API_CACHE_URLS.some(apiUrl => url.pathname.startsWith(apiUrl))) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(request, responseClone);
              });
          }
          return response;
        })
        .catch(() => {
          // Try to serve from cache when offline
          return caches.match(request)
            .then((cachedResponse) => {
              if (cachedResponse) {
                return cachedResponse;
              }
              // Return offline response for API calls
              return new Response(
                JSON.stringify({
                  error: 'Offline',
                  message: 'This feature requires an internet connection'
                }),
                {
                  status: 503,
                  statusText: 'Service Unavailable',
                  headers: { 'Content-Type': 'application/json' }
                }
              );
            });
        })
    );
    return;
  }

  // Handle static resources
  event.respondWith(
    caches.match(request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }
        
        return fetch(request)
          .then((response) => {
            // Cache successful responses
            if (response.ok) {
              const responseClone = response.clone();
              caches.open(CACHE_NAME)
                .then((cache) => {
                  cache.put(request, responseClone);
                });
            }
            return response;
          });
      })
  );
});

// Background sync for offline actions
self.addEventListener('sync', (event) => {
  console.log('Background sync triggered:', event.tag);
  
  if (event.tag === 'background-sync-code-generation') {
    event.waitUntil(syncCodeGeneration());
  } else if (event.tag === 'background-sync-code-analysis') {
    event.waitUntil(syncCodeAnalysis());
  }
});

// Push notification handling
self.addEventListener('push', (event) => {
  console.log('Push notification received:', event);
  
  const options = {
    body: 'Your code analysis is complete!',
    icon: '/favicon.ico',
    badge: '/favicon.ico',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'View Results',
        icon: '/favicon.ico'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/favicon.ico'
      }
    ]
  };

  if (event.data) {
    const data = event.data.json();
    options.body = data.body || options.body;
    options.data = { ...options.data, ...data };
  }

  event.waitUntil(
    self.registration.showNotification('TATA AI Co-pilot', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
  console.log('Notification clicked:', event);
  
  event.notification.close();

  if (event.action === 'explore') {
    // Open the app and navigate to results
    event.waitUntil(
      clients.openWindow('/?notification=results')
    );
  } else if (event.action === 'close') {
    // Just close the notification
    return;
  } else {
    // Default action - open the app
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Background sync functions
async function syncCodeGeneration() {
  try {
    // Get pending code generation requests from IndexedDB
    const pendingRequests = await getPendingRequests('code-generation');
    
    for (const request of pendingRequests) {
      try {
        const response = await fetch('/api/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(request.data)
        });
        
        if (response.ok) {
          // Remove from pending requests
          await removePendingRequest('code-generation', request.id);
          
          // Show success notification
          await self.registration.showNotification('TATA AI Co-pilot', {
            body: 'Code generation completed successfully!',
            icon: '/favicon.ico',
            tag: 'code-generation-success'
          });
        }
      } catch (error) {
        console.error('Failed to sync code generation:', error);
      }
    }
  } catch (error) {
    console.error('Background sync failed:', error);
  }
}

async function syncCodeAnalysis() {
  try {
    // Similar implementation for code analysis
    const pendingRequests = await getPendingRequests('code-analysis');
    
    for (const request of pendingRequests) {
      try {
        const response = await fetch('/api/analyze', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(request.data)
        });
        
        if (response.ok) {
          await removePendingRequest('code-analysis', request.id);
          
          await self.registration.showNotification('TATA AI Co-pilot', {
            body: 'Code analysis completed successfully!',
            icon: '/favicon.ico',
            tag: 'code-analysis-success'
          });
        }
      } catch (error) {
        console.error('Failed to sync code analysis:', error);
      }
    }
  } catch (error) {
    console.error('Background sync failed:', error);
  }
}

// IndexedDB helpers for offline storage
async function getPendingRequests(type) {
  // Simplified implementation - in real app, use IndexedDB
  return [];
}

async function removePendingRequest(type, id) {
  // Simplified implementation - in real app, use IndexedDB
  return true;
}

// Message handling from main thread
self.addEventListener('message', (event) => {
  console.log('Service Worker received message:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

console.log('TATA AI Co-pilot Service Worker loaded successfully');
