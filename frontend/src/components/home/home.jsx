/**
 * This is the home component which displays each Theater and the movies
 * playing at the given theater.
 * The home component also has a search bar to search for a specific theater/movie.
 * The home component also has the users profile logo on the left side next to the search bar.
**/

import { useState } from "react";
import DefaultProfile from "../../profile-default-icon-2048x2045-u3j7s5nj.png"

function Home() {
    return (
        <div>
            {/* Container for the profile logo and search bar which will be on the left side of the screen like a navbar*/}
            <div>
                <img src={DefaultProfile} alt="Profile Logo" />
                <input type="search" placeholder="Search for a movie" />
            </div>
            {/* Container for each theater and movies, where it will be replaced with object mapping.*/}
            <div>
                <div>
                    <h2>Theater 1</h2>
                    <div>
                        <img src={DefaultProfile} alt="Profile Logo" className="profile-logo"></img>
                        <p>Movie Name</p>
                    </div>
                </div>
                <div>
                    <h2>Theater 2</h2>
                </div>
                <div>
                    <h2>Theater 3</h2>
                </div>
                <div>
                    <h2>Theater 4</h2>
                </div>
                <div>
                    <h2>Theater 5</h2>
                </div>
                <div>
                    <h2>Theater 6</h2>
                </div>
            </div>
        </div>
    )
}

export default Home;
