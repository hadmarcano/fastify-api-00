from fastapi import FastAPI, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token

app = FastAPI()

app.title = "FASTAPI Server"
app.version = "0.0.1"

movies = [
    {"id": 1, "title": "The Shawshank Redemption", "year": 1994, "rating": 9.3},
    {"id": 2, "title": "The Godfather", "year": 1972, "rating": 9.2},
    {"id": 3, "title": "The Godfather: Part II", "year": 1974, "rating": 9.0},
]

class User(BaseModel):
    email:str
    password:str


class Movie(BaseModel):
    # id: int | None = None
    id: Optional[int] = None
    title: str = Field(min_length=2, max_length=15)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "The Shawshank Redemption",
                "year": 1994,
                "rating": 9.3,
            }
        }

@app.post("/login", tags=["Auth"])
async def login(user: User):
    user = user.dict()
    print("User", user)
    return create_token(user)


@app.get("/movies", tags=["Movies"], response_model=List[Movie], status_code=200)
async def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)


@app.get("/movies/{id}", tags=["Movies"], response_model=Movie, status_code=200)
async def get_movie_by_id(id: int = Path(ge=1, le=2000)) -> Movie:
    for movie in movies:
        if movie["id"] == id:
            return JSONResponse(status_code=200, content=movie)
    return JSONResponse(
        status_code=404, content={"error": "Movie not found", "status": 404}
    )


# Query params
@app.get("/movies/", tags=["Movies"], response_model=List[Movie], status_code=200)
async def get_movies_by_query(year: int = None) -> List[Movie]:
    """
    Retrieves a list of movies based on the specified year.

    Args:
        year (int, optional): The year to filter the movies by. Defaults to None.

    Returns:
        list: A list of movies that match the specified year, or all movies if no year is provided.
    """
    if year:
        data = [movie for movie in movies if movie["year"] == year]
        return JSONResponse(status_code=200, content=data)
    return JSONResponse(status_code=200, content=movies)


@app.post("/movies", tags=["Movies"], response_model=List[Movie], status_code=201)
async def add_movie(movie: Movie):

    movie = movie.dict()
    # Check if the movie dict contains all the required keys
    required_keys = {"id", "title", "year", "rating"}
    if movie.keys() >= required_keys:
        print("The movie dictionary contains all the required keys.")
        movies.append(movie)
        return JSONResponse(
            status_code=201,
            content={"status": "Movie added successfully", "movie": movie},
        )
    else:
        print("The movie dictionary is missing some keys.")
        return JSONResponse(
            status_code=400,
            content={"error": "dictionary is missing some keys.", "status": 400},
        )


@app.put("/movies/{id}", tags=["Movies"], response_model=dict, status_code=200)
async def update_movie(id: int, movie: dict) -> dict:

    updatable_keys = {"title", "year", "rating"}
    # Check if the movie dict contains at least one of the updatable keys
    if not updatable_keys.intersection(movie.keys()):
        return JSONResponse(
            status_code=400,
            content={"error": "No updatable information provided.", "status": 400},
        )

    for i in range(len(movies)):
        if movies[i]["id"] == id:
            # Update only the keys that are present in the incoming movie dict
            for key in movie:
                if key in updatable_keys:
                    movies[i][key] = movie[key]
            return JSONResponse(
                status_code=200,
                content={"status": "Movie updated successfully", "movie": movie},
            )
    return JSONResponse(
        status_code=404, content={"error": "Movie not found", "status": 404}
    )


@app.delete("/movies/{id}", tags=["Movies"], response_model=dict, status_code=200)
async def delete_movie(id: int) -> dict:
    for i in range(len(movies)):
        if movies[i]["id"] == id:
            del movies[i]
            return JSONResponse(
                status_code=200, content={"status": "Movie deleted successfully"}
            )
    return JSONResponse(
        status_code=404, content={"error": "Movie not found", "status": 404}
    )
