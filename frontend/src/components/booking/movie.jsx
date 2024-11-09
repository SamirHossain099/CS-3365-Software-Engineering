/**
 * This is the movie component which will be used to display the movies
 * and their showtimes on different days.
 * The movie componenent below gives Date, Time, Movie Description, Reviews, and Purchase Ticket button.
**/

import "./movie.css";
import { useNavigate } from "react-router-dom";

function Movie() {
    const navigate = useNavigate();
    const handlePurchase = async (movieId) => {
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user) {
            navigate('/');
            return;
        }

        try {
            const response = await fetch('/api/purchase/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    userId: user.id,
                    movieId,
                    date,
                    time,
                    theater,
                    ticketCount,
                    price,
                })
            });

            if (response.ok) {
                alert('Purchase successful');
            } else {
                const error = await response.json();
                alert(error.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing your purchase.');
        }
    };

    return (
        <div>
            <h1>Movie Name</h1>
            {/* Container/Hero page for the movie with the purchase option alongside movie information.*/}
            <div>
                <div>
                    <button>Purchase Ticket</button>
                    <button>Rate</button>
                </div>
                <div>
                    <p>Date and Length of Movie</p>
                    <p>Cast</p>
                    <p>Genre</p>
                </div>
                <div>
                    <p>Movie Age Rating</p>
                    <p>Movie Description</p>
                </div>
            </div>
            {/* Container for the reviews of the movie. Which will be below the container/hero page of the movie information.*/}
            <div>
                <h3>Reviews</h3>
                <div>
                    <p>User</p>
                    <p>Review</p>
                    <p>Rating</p>
                </div>
            </div>
        </div>
    )
}

export default Movie;