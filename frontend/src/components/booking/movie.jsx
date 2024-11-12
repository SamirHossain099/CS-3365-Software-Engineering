/**
 * This is the movie component which will be used to display the movies
 * and their showtimes on different days.
 * The movie componenent below gives Date, Time, Movie Description, Reviews, and Purchase Ticket button.
**/

import "./movie.css";
import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import FallbackImage from '../../moviefallback.jpg';

const BACKEND_URL = 'http://localhost:8000';

function Movie() {
    const navigate = useNavigate();
    const { movieId } = useParams();
    const [movie, setMovie] = useState(null);
    const [reviews, setReviews] = useState([]);
    const [showtimes, setShowtimes] = useState([]);
    const [selectedShowtime, setSelectedShowtime] = useState(null);
    const [ticketCount, setTicketCount] = useState(1);

    useEffect(() => {
        const fetchMovieDetails = async () => {
            try {
                const response = await fetch(`${BACKEND_URL}/movies/details/${movieId}/`);
                if (!response.ok) {
                    throw new Error('Failed to fetch movie details');
                }
                const data = await response.json();
                console.log('Movie details:', data);
                console.log('Image URL:', data.movie.image);
                setMovie(data.movie);
                setReviews(data.reviews || []);
            } catch (error) {
                console.error('Error fetching movie details:', error);
            }
        };

        const fetchShowtimes = async () => {
            try {
                const response = await fetch(`${BACKEND_URL}/showtimes/movie/${movieId}/`);
                if (!response.ok) {
                    throw new Error('Failed to fetch showtimes');
                }
                const data = await response.json();
                setShowtimes(data.showtimes);
            } catch (error) {
                console.error('Error fetching showtimes:', error);
            }
        };

        if (movieId) {
            fetchMovieDetails();
            fetchShowtimes();
        }
    }, [movieId]);

    const handlePurchase = async () => {
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user) {
            navigate('/');
            return;
        }

        if (!selectedShowtime) {
            alert('Please select a showtime');
            return;
        }

        try {
            const response = await fetch(`${BACKEND_URL}/booking/create/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: user.id,
                    showtime_id: selectedShowtime,
                    ticket_count: ticketCount,
                })
            });

            if (response.ok) {
                alert('Purchase successful!');
                navigate('/profile');
            } else {
                const error = await response.json();
                alert(error.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing your purchase.');
        }
    };

    if (!movie) {
        return <div className="loading">Loading...</div>;
    }

    return (
        <div className="movie-details-container">
            <div className="movie-hero">
                <img 
                    src={movie.image ? `${BACKEND_URL}/media/${movie.image.split('/').pop()}` : FallbackImage}
                    alt={movie.title}
                    className="movie-poster"
                    onError={(e) => {
                        console.log('Image load error for:', movie.title);
                        e.target.onerror = null;
                        e.target.src = FallbackImage;
                    }}
                />
                <div className="movie-info">
                    <h1>{movie.title}</h1>
                    <div className="movie-metadata">
                        <p>Rating: {movie.rating}/5</p>
                        <p>Duration: {movie.duration} minutes</p>
                        <p>Genre: {movie.genre}</p>
                        <p>Director: {movie.director || 'Not available'}</p>
                        <p>Release Date: {new Date(movie.release_date).toLocaleDateString()}</p>
                        <p>Location: {movie.location}</p>
                    </div>
                    <p className="movie-description">{movie.description}</p>
                </div>
            </div>

            <div className="booking-section">
                <h2>Book Tickets</h2>
                <select 
                    value={selectedShowtime || ''} 
                    onChange={(e) => setSelectedShowtime(e.target.value)}
                >
                    <option value="">Select a showtime</option>
                    {showtimes.map(showtime => (
                        <option key={showtime.showtime_id} value={showtime.showtime_id}>
                            {new Date(showtime.show_date).toLocaleDateString()} at {showtime.show_time} 
                            - {showtime.theater_location} (${showtime.ticket_price})
                        </option>
                    ))}
                </select>
                
                <div className="ticket-count">
                    <label>Number of tickets:</label>
                    <input
                        type="number"
                        min="1"
                        max="10"
                        value={ticketCount}
                        onChange={(e) => setTicketCount(parseInt(e.target.value))}
                    />
                </div>

                <button onClick={handlePurchase} className="purchase-button">
                    Purchase Tickets
                </button>
            </div>

            <div className="reviews-section">
                <h2>Reviews</h2>
                {reviews && reviews.length > 0 ? (
                    reviews.map(review => (
                        <div key={review.review_id} className="review-card">
                            <p className="review-user">{review.user}</p>
                            <p className="review-rating">Rating: {review.rating}/5</p>
                            <p className="review-text">{review.review_text}</p>
                            <p className="review-date">
                                {new Date(review.created_at).toLocaleDateString()}
                            </p>
                        </div>
                    ))
                ) : (
                    <p>No reviews yet.</p>
                )}
            </div>
        </div>
    );
}

export default Movie;