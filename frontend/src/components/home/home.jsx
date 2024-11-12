/**
 * This is the home component which displays each Theater and the movies
 * playing at the given theater.
 * The home component also has a search bar to search for a specific theater/movie.
 * The home component also has the users profile logo on the left side next to the search bar.
**/

// Import necessary dependencies and assets
import "./home.css";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import DefaultProfile from "../../profile-default-icon-2048x2045-u3j7s5nj.png"
import HomeIcon from "../../home.png"
import SearchIcon from "../../search-icon.png"
import FallbackImage from '../../moviefallback.jpg';  // Fallback image for when movie posters fail to load

// Define the backend URL for media files
const BACKEND_URL = 'http://localhost:8000/media';

function Home() {
    // State management for movies in each theater
    const [theater1Movies, setTheater1Movies] = useState([]);
    const [theater2Movies, setTheater2Movies] = useState([]);
    const [theater3Movies, setTheater3Movies] = useState([]);
    const [theater4Movies, setTheater4Movies] = useState([]);
    const [theater5Movies, setTheater5Movies] = useState([]);
    const [theater6Movies, setTheater6Movies] = useState([]);
    
    // State for controlling search bar visibility
    const [showSearch, setShowSearch] = useState(false);
    
    // Hook for programmatic navigation
    const navigate = useNavigate();

    // Fetch movies when component mounts
    useEffect(() => {
        fetchMovies();
    }, []);

    // Function to fetch movies from backend and sort them by theater location
    const fetchMovies = async () => {
        try {
            const response = await fetch('/movies/viewmovies/');
            if (!response.ok) {
                throw new Error('Failed to fetch movies');
            }
            const data = await response.json();
            console.log('First movie data:', data.movies[0]);
            
            // Filter movies by their respective theater locations
            setTheater1Movies(data.movies.filter(movie => movie.location === 'Lubbock, TX'));
            setTheater2Movies(data.movies.filter(movie => movie.location === 'Amarillo'));
            setTheater3Movies(data.movies.filter(movie => movie.location === 'Levelland, TX'));
            setTheater4Movies(data.movies.filter(movie => movie.location === 'Plainview, TX'));
            setTheater5Movies(data.movies.filter(movie => movie.location === 'Snyder, TX'));
            setTheater6Movies(data.movies.filter(movie => movie.location === 'Abilene, TX'));
        } catch (error) {
            console.error('Error fetching movies:', error);
        }
    };

    // Handler for profile icon click - navigates to profile page
    const handleProfileClick = () => {
        navigate("/profile");
    }

    return (
        <div>
            {/* Navigation bar container */}
            <div className="navbar-container">
                {/* Profile icon with click handler */}
                <img 
                    src={DefaultProfile} 
                    alt="Profile Logo" 
                    className="profile-logo" 
                    onClick={handleProfileClick} 
                    style={{cursor: "pointer"}}
                />
                {/* Home icon */}
                <img 
                    src={HomeIcon} 
                    alt="Home Icon" 
                    className="home-icon" 
                    style={{cursor: "pointer"}} 
                />
                {/* Search container with toggle functionality */}
                <div className="search-container">
                    <input 
                        type="search" 
                        placeholder="Search for a movie" 
                        className={`search-bar ${showSearch ? 'show' : 'hide'}`} 
                    />
                    <img 
                        src={SearchIcon} 
                        alt="Search Icon" 
                        className="search-icon"
                        onClick={() => setShowSearch(!showSearch)}
                    />
                </div>
            </div>
            
            {/* Main content container for theaters and movies */}
            <div className="main-content">
                {/* Each theater section follows the same pattern:
                    1. Theater heading
                    2. Container for movies
                    3. Map through movies array to create movie cards
                    4. Each movie card contains:
                       - Movie poster image with error handling
                       - Movie title
                */}
                {/* Theater 1 section */}
                <div className="theater-section">
                    <h2>Theater 1</h2>
                    <div className="movies-container">
                        {theater1Movies.map(movie => (
                            <div key={movie.movie_id} className="movie-card">
                                <img 
                                    src={movie.image || FallbackImage} 
                                    alt={movie.title} 
                                    onError={(e) => {
                                        e.target.onerror = null;
                                        e.target.src = FallbackImage;
                                    }}
                                />
                                <p>{movie.title}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Theater 2 section */}
                <div className="theater-section">
                    <h2>Theater 2</h2>
                    <div className="movies-container">
                        {theater2Movies.map(movie => (
                            <div key={movie.movie_id} className="movie-card">
                                <img 
                                    src={movie.image || FallbackImage} 
                                    alt={movie.title}
                                    onError={(e) => {
                                        e.target.onerror = null;
                                        e.target.src = FallbackImage;
                                    }}
                                />
                                <p>{movie.title}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Theater 3 section */}
                <div className="theater-section">
                    <h2>Theater 3</h2>
                    <div className="movies-container">
                        {theater3Movies.map(movie => (
                            <div key={movie.movie_id} className="movie-card">
                                <img 
                                    src={movie.image || FallbackImage} 
                                    alt={movie.title}
                                    onError={(e) => {
                                        e.target.onerror = null;
                                        e.target.src = FallbackImage;
                                    }}
                                />
                                <p>{movie.title}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Theater 4 section */}
                <div className="theater-section">
                    <h2>Theater 4</h2>
                    <div className="movies-container">
                        {theater4Movies.map(movie => (
                            <div key={movie.movie_id} className="movie-card">
                                <img 
                                    src={movie.image || FallbackImage} 
                                    alt={movie.title}
                                    onError={(e) => {
                                        e.target.onerror = null;
                                        e.target.src = FallbackImage;
                                    }}
                                />
                                <p>{movie.title}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Theater 5 section */}
                <div className="theater-section">
                    <h2>Theater 5</h2>
                    <div className="movies-container">
                        {theater5Movies.map(movie => (
                            <div key={movie.movie_id} className="movie-card">
                                <img 
                                    src={movie.image || FallbackImage} 
                                    alt={movie.title}
                                    onError={(e) => {
                                        e.target.onerror = null;
                                        e.target.src = FallbackImage;
                                    }}
                                />
                                <p>{movie.title}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Theater 6 section */}
                <div className="theater-section">
                    <h2>Theater 6</h2>
                    <div className="movies-container">
                        {theater6Movies.map(movie => (
                            <div key={movie.movie_id} className="movie-card">
                                <img 
                                    src={movie.image || FallbackImage} 
                                    alt={movie.title}
                                    onError={(e) => {
                                        e.target.onerror = null;
                                        e.target.src = FallbackImage;
                                    }}
                                />
                                <p>{movie.title}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Home;
