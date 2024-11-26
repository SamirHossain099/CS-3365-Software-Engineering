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
    const handlePurchase = () => {
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user) {
            alert('Please log in to purchase tickets');
            navigate('/login');
            return;
        }

        if (!selectedShowtime) {
            alert('Please select a showtime');
            return;
        }

        // Find the selected showtime object
        const showtime = showtimes.find(st => st.showtime_id === parseInt(selectedShowtime));
        if (!showtime) {
            alert('Invalid showtime');
            return;
        }

        if (ticketCount < 1) {
            alert('Please select at least one ticket');
            return;
        }

        // Navigate to checkout page with necessary information
        navigate('/checkout', {
            state: {
                showtimeId: parseInt(selectedShowtime),
                ticketPrice: Number(showtime.ticket_price),
                ticketCount: ticketCount,
                movieTitle: movie.title,
                showDate: showtime.show_date,
                showTime: showtime.show_time,
                theaterLocation: showtime.theater_location
            }
        });
    };

    const handleCreateReview = async () => {
        const user = JSON.parse(localStorage.getItem('user'));
        
        if (!user) {
            navigate('/');
            return;
        }

        const rating = prompt("Enter your rating (1-5):");
        const reviewText = prompt("Enter your review:");

        // Validate rating
        const ratingNum = parseInt(rating);
        if (isNaN(ratingNum) || ratingNum < 1 || ratingNum > 5) {
            alert('Please enter a valid rating between 1 and 5');
            return;
        }

        // Validate review text
        if (!reviewText || reviewText.trim() === '') {
            alert('Please enter a review text');
            return;
        }

        const requestData = {
            movie_id: parseInt(movieId),
            rating: ratingNum,
            review_text: reviewText.trim(),
            user_id: user.id
        };

        try {
            const response = await fetch(`${BACKEND_URL}/reviews/add/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to create review');
            }

            const data = await response.json();
            alert('Review created successfully!');
            
            // Refresh the reviews
            const reviewsResponse = await fetch(`${BACKEND_URL}/movies/details/${movieId}/`);
            const reviewsData = await reviewsResponse.json();
            setReviews(reviewsData.reviews || []);
        } catch (error) {
            console.error('Error:', error);
            alert(error.message || 'An error occurred while creating your review.');
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
                <button onClick={handleCreateReview}>Create Review</button>
            </div>
        </div>
    );
}

export default Movie;