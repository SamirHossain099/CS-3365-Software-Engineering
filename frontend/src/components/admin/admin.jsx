/** 
 * This is the admin component which will be used to manage the website.
 * Only users with admin privilages will be able to access this component.
 * The component will allow the admin to manage the movies, dates, and showtimes.
**/

import "./admin.css";

function Admin() {
    return (
        <div>
            <h2>Dashboard</h2>
            {/* Section for the theaters.*/}
            <div>
                <h3>Theaters</h3>
                <form>
                    <label htmlFor="TheaterName">Theater Name</label>
                    <input type="text" id="TheaterName" name="TheaterName" required />
                    <label htmlFor="TheaterLocation">Theater Location</label>
                    <input type="text" id="TheaterLocation" name="TheaterLocation" required />
                    <button type="submit">Add Theater</button>
                </form>
                <button>Delete Theater</button>
            </div>
            {/* Section for the movies.*/}
            <div>
                <h3>Movies</h3>
                <form>
                    <label htmlFor="MovieName">Movie Name</label>
                    <input type="text" id="MovieName" name="MovieName" required />
                    <label htmlFor="MovieDescription">Movie Description</label>
                    <input type="text" id="MovieDescription" name="MovieDescription" required />
                    <label htmlFor="MovieCast">Movie Cast</label>
                    <input type="text" id="MovieCast" name="MovieCast" required />
                    <label htmlFor="MovieGenre">Movie Genre</label>
                    <input type="text" id="MovieGenre" name="MovieGenre" required />
                    <button type="submit">Add Movie</button>
                </form>
                <button>Delete Movie</button>
            </div>
            {/* Section for the total users.*/}
            <div>
                <h3>Total Users</h3>
                <p>{/* Total number of users.*/}</p>
            </div>
        </div>
    )
}

export default Admin;
