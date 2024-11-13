/**
 * This is the movie component which displays detailed information about a specific movie,
 * including its description, showtimes, and user reviews.
 * Users can also book tickets for available showtimes.
 */

import "./movie.css";
import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import FallbackImage from '../../moviefallback.jpg';  // Default image if movie poster fails to load

// Backend URL for API calls
const BACKEND_URL = 'http://localhost:8000';

function Movie() {
    // React Router hooks for navigation and getting movie ID from URL
    const navigate = useNavigate();
    const { movieId } = useParams();

    // State management for component data
    const [movie, setMovie] = useState(null);                        // Stores movie details
    const [reviews, setReviews] = useState([]);                      // Stores movie reviews
    const [showtimes, setShowtimes] = useState([]);                  // Stores available showtimes
    const [selectedShowtime, setSelectedShowtime] = useState(null);  // Selected showtime for booking
    const [ticketCount, setTicketCount] = useState(1);               // Number of tickets to purchase

    // useEffect hook to fetch movie details and showtimes when component mounts or movieId changes
    useEffect(() => {
        // Function to fetch movie details and reviews
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

        // Function to fetch available showtimes for the movie
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

        // Call both fetch functions if movieId is available
        if (movieId) {
            fetchMovieDetails();
            fetchShowtimes();
        }
    }, [movieId]);  // Dependency array - effect runs when movieId changes

    // Handler for ticket purchase
    const handlePurchase = async () => {
        // Check if user is logged in
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user) {
            navigate('/');  // Redirect to login if not logged in
            return;
        }

        // Validate showtime selection
        if (!selectedShowtime) {
            alert('Please select a showtime');
            return;
        }

        // Attempt to create booking
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
                navigate('/profile');  // Redirect to profile page after successful purchase
            } else {
                const error = await response.json();
                alert(error.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing your purchase.');
        }
    };

    // Show loading state while movie data is being fetched
    if (!movie) {
        return <div className="loading">Loading...</div>;
    }

    // Render movie details, booking section, and reviews
    return (
        <div className="movie-details-container">
            {/* Movie hero section with poster and basic info */}
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

            {/* Booking section with showtime selection and ticket count */}
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

            {/* Reviews section */}
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