// URL base de la API
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'; // Ajusta esto a la URL de tu API

// Funciones de utilidad
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    document.cookie = `${name}=${value}; ${expires}; path=/`;
}

function getUrlParameter(name) {
    const url = window.location.search;
    const regex = new RegExp(`[?&]${name}(=([^&#]*)|&|#|$)`);
    const results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

// Verificación de autenticación
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    
    if (loginLink) {
        if (token) {
            loginLink.textContent = 'Cerrar Sesión';
            loginLink.addEventListener('click', (e) => {
                e.preventDefault();
                document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                window.location.href = 'index.html';
            });
        } else {
            loginLink.textContent = 'Iniciar Sesión';
            loginLink.href = 'login.html';
        }
    }
    
    return token;
}

// ====== MANEJO DE PÁGINA DE INICIO DE SESIÓN ======
function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorMessage = document.getElementById('login-error');
            
            try {
                const response = await fetch(`${API_BASE_URL}/users/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    setCookie('token', data.access_token, 7); // Guarda el token por 7 días
                    window.location.href = 'index.html';
                } else {
                    errorMessage.textContent = data.error || 'Error al iniciar sesión. Verifica tus credenciales.';
                }
            } catch (error) {
                errorMessage.textContent = 'Error de conexión. Por favor, intenta nuevamente.';
                console.error('Error:', error);
            }
        });
    }
}

// ====== MANEJO DE PÁGINA PRINCIPAL (INDEX) ======
async function fetchPlaces() {
    const token = getCookie('token');
    const placesContainer = document.getElementById('places-list');
    
    if (placesContainer) {
        try {
            // Configura los headers basados en la autenticación
            const headers = {
                'Content-Type': 'application/json'
            };
            
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            
            const response = await fetch(`${API_BASE_URL}/places`, {
                method: 'GET',
                headers: headers
            });
            
            if (response.ok) {
                const places = await response.json();
                displayPlaces(places);
                setupPriceFilter(places);
            } else {
                placesContainer.innerHTML = '<p class="error-message">Error al cargar los lugares. Por favor, intenta nuevamente.</p>';
            }
        } catch (error) {
            placesContainer.innerHTML = '<p class="error-message">Error de conexión. Por favor, intenta nuevamente.</p>';
            console.error('Error:', error);
        }
    }
}

function displayPlaces(places) {
    const placesContainer = document.getElementById('places-list');
    placesContainer.innerHTML = '';
    
    if (places.length === 0) {
        placesContainer.innerHTML = '<p>No hay lugares disponibles.</p>';
        return;
    }
    
    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.dataset.price = place.price_by_night;
        
        placeCard.innerHTML = `
            <h3>${place.name}</h3>
            <p>${place.description ? place.description.substring(0, 100) + '...' : 'Sin descripción'}</p>
            <div class="place-price">$${place.price_by_night} / noche</div>
            <a href="places.html?id=${place.id}" class="details-button">Ver Detalles</a>
        `;
        
        placesContainer.appendChild(placeCard);
    });
}

function setupPriceFilter(places) {
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', () => {
            const selectedPrice = priceFilter.value;
            const placeCards = document.querySelectorAll('.place-card');
            
            placeCards.forEach(card => {
                const price = parseFloat(card.dataset.price);
                
                if (selectedPrice === 'all' || price <= parseFloat(selectedPrice)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

// ====== MANEJO DE PÁGINA DE DETALLES DE LUGAR ======
async function fetchPlaceDetails() {
    const placeId = getUrlParameter('id');
    const token = getCookie('token');
    const placeDetailsContainer = document.getElementById('place-details');
    const reviewsContainer = document.getElementById('reviews-list');
    const addReviewSection = document.getElementById('add-review');
    
    if (placeDetailsContainer && placeId) {
        try {
            // Configura los headers basados en la autenticación
            const headers = {
                'Content-Type': 'application/json'
            };
            
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            
            const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
                method: 'GET',
                headers: headers
            });
            
            if (response.ok) {
                const place = await response.json();
                displayPlaceDetails(place);
                
                // Cargar reseñas
                if (reviewsContainer) {
                    fetchReviews(placeId, token);
                }
                
                // Configurar sección de añadir reseña
                if (addReviewSection) {
                    if (token) {
                        const addReviewBtn = document.getElementById('add-review-btn');
                        if (addReviewBtn) {
                            addReviewBtn.href = `add_review.html?place_id=${placeId}`;
                        }
                    } else {
                        addReviewSection.innerHTML = '<p>Inicia sesión para dejar una reseña.</p>';
                    }
                }
            } else {
                placeDetailsContainer.innerHTML = '<p class="error-message">Error al cargar los detalles del lugar. Por favor, intenta nuevamente.</p>';
            }
        } catch (error) {
            placeDetailsContainer.innerHTML = '<p class="error-message">Error de conexión. Por favor, intenta nuevamente.</p>';
            console.error('Error:', error);
        }
    }
}

function displayPlaceDetails(place) {
    const placeDetailsContainer = document.getElementById('place-details');
    
    // Construir lista de amenidades con iconos
    let amenitiesHTML = '<p>No hay amenidades listadas</p>';
    
    if (place.amenities && place.amenities.length > 0) {
        amenitiesHTML = '<ul class="amenities-list">';
        place.amenities.forEach(amenity => {
            // Usar iconos específicos para ciertas amenidades comunes
            let iconSrc = '';
            if (amenity.toLowerCase().includes('wifi')) {
                iconSrc = 'images/icon_wifi.png';
            } else if (amenity.toLowerCase().includes('baño') || amenity.toLowerCase().includes('bath')) {
                iconSrc = 'images/icon_bath.png';
            } else if (amenity.toLowerCase().includes('cama') || amenity.toLowerCase().includes('bed')) {
                iconSrc = 'images/icon_bed.png';
            }
            
            if (iconSrc) {
                amenitiesHTML += `<li><img src="${iconSrc}" alt="${amenity}" width="20"> ${amenity}</li>`;
            } else {
                amenitiesHTML += `<li>${amenity}</li>`;
            }
        });
        amenitiesHTML += '</ul>';
    }
    
    const placeHTML = `
        <div class="place-info">
            <h1>${place.name}</h1>
            <p><strong>Ubicación:</strong> ${place.city}, ${place.state || ''}</p>
            <p><strong>Precio:</strong> $${place.price_by_night} / noche</p>
            <p><strong>Descripción:</strong> ${place.description || 'Sin descripción'}</p>
            
            <div class="amenities">
                <h3>Amenidades</h3>
                ${amenitiesHTML}
            </div>
        </div>
    `;
    
    placeDetailsContainer.innerHTML = placeHTML;
}

async function fetchReviews(placeId, token) {
    const reviewsContainer = document.getElementById('reviews-list');
    
    try {
        // Configura los headers basados en la autenticación
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
            method: 'GET',
            headers: headers
        });
        
        if (response.ok) {
            const reviews = await response.json();
            displayReviews(reviews);
        } else {
            reviewsContainer.innerHTML = '<p class="error-message">Error al cargar las reseñas. Por favor, intenta nuevamente.</p>';
        }
    } catch (error) {
        reviewsContainer.innerHTML = '<p class="error-message">Error de conexión. Por favor, intenta nuevamente.</p>';
        console.error('Error:', error);
    }
}

function displayReviews(reviews) {
    const reviewsContainer = document.getElementById('reviews-list');
    
    if (!reviews || reviews.length === 0) {
        reviewsContainer.innerHTML = '<p>No hay reseñas para este lugar.</p>';
        return;
    }
    
    reviewsContainer.innerHTML = '';
    
    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        
        const reviewDate = new Date(review.created_at).toLocaleDateString();
        
        reviewCard.innerHTML = `
            <div class="review-user">${review.user_name || 'Usuario anónimo'}</div>
            <div class="review-date">${reviewDate}</div>
            <p>${review.text}</p>
        `;
        
        reviewsContainer.appendChild(reviewCard);
    });
}

// ====== MANEJO DE PÁGINA DE AÑADIR RESEÑA ======
function setupAddReviewPage() {
    const token = getCookie('token');
    const placeId = getUrlParameter('place_id');
    
    // Redirige al index si no hay token o ID de lugar
    if (!token || !placeId) {
        window.location.href = 'index.html';
        return;
    }
    
    // Obtiene el nombre del lugar para mostrarlo en el título
    fetchPlaceName(placeId, token);
    
    // Configura el formulario para enviar reseñas
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const reviewText = document.getElementById('review-text').value;
            const errorMessage = document.getElementById('review-error');
            
            try {
                const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ text: reviewText })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    alert('¡Reseña enviada con éxito!');
                    window.location.href = `places.html?id=${placeId}`;
                } else {
                    errorMessage.textContent = data.error || 'Error al enviar la reseña. Por favor, intenta nuevamente.';
                }
            } catch (error) {
                errorMessage.textContent = 'Error de conexión. Por favor, intenta nuevamente.';
                console.error('Error:', error);
            }
        });
    }
}

async function fetchPlaceName(placeId, token) {
    const placeTitle = document.getElementById('place-title');
    
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const place = await response.json();
            placeTitle.textContent = `Añadir Reseña para: ${place.name}`;
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Función principal que se ejecuta al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    // Verificar la autenticación en todas las páginas
    const token = checkAuthentication();
    
    // Determinar en qué página estamos y ejecutar el código correspondiente
    const currentPath = window.location.pathname;
    
    if (currentPath.includes('login.html')) {
        setupLoginForm();
    } 
    else if (currentPath.includes('places.html')) {
        fetchPlaceDetails();
    } 
    else if (currentPath.includes('add_review.html')) {
        setupAddReviewPage();
    } 
    else {
        // Página index.html o cualquier otra
        fetchPlaces();
    }
});