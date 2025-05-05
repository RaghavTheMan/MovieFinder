function handleEnter(event) {
    if (event.key === "Enter") {
        searchMovie();
    }
}

function searchMovie() {
    const query = document.getElementById("movieName").value.trim();
    if (!query) {
        alert("Please enter a movie name!");
        return;
    }
    window.location.href = `/search?query=${encodeURIComponent(query)}`;
}

function initSwiper() {
    new Swiper('.swiper-container', {
        slidesPerView: 'auto',
        spaceBetween: 15,
        centeredSlides: false,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            640: {
                slidesPerView: 2,
            },
            768: {
                slidesPerView: 3,
            },
            1024: {
                slidesPerView: 4,
            },
        }
    });
}

window.onload = function() {
    fetch('/trending')
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('trendingMovies');
            container.innerHTML = data.results.slice(0,10).map(movie => `
                <div class="swiper-slide">
                    <div class="trending-card">
                        <img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" 
                             alt="${movie.title}" 
                             class="trending-poster">
                        <div class="trending-info">
                            <h3>${movie.title}</h3>
                            <p>★ ${movie.vote_average.toFixed(1)}</p>
                        </div>
                    </div>
                </div>
            `).join('');
            initSwiper();
        });
};

document.addEventListener('click', function(e) {
    const movieCard = e.target.closest('.movie-card');
    if (movieCard) {
        const movieId = movieCard.dataset.movieId;
        if (movieId) {
            window.location.href = `/movie/${movieId}`;
        }
    }
});