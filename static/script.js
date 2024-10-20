document.getElementById('restaurantForm').addEventListener('submit', function (e) {
    e.preventDefault();
    
    const city = document.getElementById('city').value;
    const state = document.getElementById('state').value;
    const cuisine = document.getElementById('cuisine').value;


    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ city: city, state: state, cuisine: cuisine }),
    })
    .then(response => response.json())
    .then(data => {
        const recommendationsList = document.getElementById('recommendations');
        recommendationsList.innerHTML = '';

        if (data.message) {
            recommendationsList.innerHTML = `<li>${data.message}</li>`;
        } else {
            data.forEach(restaurant => {
                recommendationsList.innerHTML += `
                    <li>
                        <strong>${restaurant.name}</strong> - ${restaurant.cuisine}<br>
                        ${restaurant.address}, ${restaurant.city}, ${restaurant.state} ${restaurant.zipcode}<br>
                        Rating: ${restaurant.rating}
                    </li>
                `;
            });
        }
    });
});

