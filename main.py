from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

app.title = "FASTAPI Server"
app.version = "0.0.1"

movies = [
    {"id": 1, "title": "The Shawshank Redemption", "year": 1994, "rating": 9.3},
    {"id": 2, "title": "The Godfather", "year": 1972, "rating": 9.2},
    {"id": 3, "title": "The Godfather: Part II", "year": 1974, "rating": 9.0},
]


@app.get("/movies", tags=["Movies"])
async def get_movies():
    return movies


@app.get("/movies/{id}", tags=["Movies"])
async def get_movie_by_id(id: int):
    for movie in movies:
        if movie["id"] == id:
            return movie
    return {"error": "Movie not found", "status": 404}

# Query params
@app.get("/movies/", tags=["Movies"])
async def get_movies_by_query(year: int = None):
    """
    Retrieves a list of movies based on the specified year.

    Args:
        year (int, optional): The year to filter the movies by. Defaults to None.

    Returns:
        list: A list of movies that match the specified year, or all movies if no year is provided.
    """
    if year:
        return [movie for movie in movies if movie["year"] == year]
    return movies

@app.post("/movies", tags=["Movies"])
async def add_movie(movie: dict):
    ## How to verify that movie dict has the key values that i need ?
    required_keys = {'id','title', 'year', 'rating'}
    if movie.keys() >= required_keys:
        print("The movie dictionary contains all the required keys.")
        movies.append(movie)
        return {"status": "Movie added successfully", "movie": movie}
    else:
        print("The movie dictionary is missing some keys.")
        return {"error": "dictionary is missing some keys.", "status": 400}
    
@app.put("/movies/{id}", tags=["Movies"])
async def update_movie(id: int, movie: dict):

    updatable_keys = {'title', 'year', 'rating'}
    # Check if the movie dict contains at least one of the updatable keys
    if not updatable_keys.intersection(movie.keys()):
        return {"error": "No updatable information provided.", "status": 400}

    for i in range(len(movies)):
        if movies[i]["id"] == id:
            # Update only the keys that are present in the incoming movie dict
            for key in movie:
                if key in updatable_keys:
                    movies[i][key] = movie[key]
            return {"status": "Movie updated successfully", "movie": movie}
    return {"error": "Movie not found", "status": 404}

@app.delete("/movies/{id}", tags=["Movies"])
async def delete_movie(id: int):
    for i in range(len(movies)):
        if movies[i]["id"] == id:
            del movies[i]
            return {"status": "Movie deleted successfully"}
    return {"error": "Movie not found", "status": 404}


