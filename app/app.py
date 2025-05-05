from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/movie", methods=["GET"])
def get_movie():
    movie_name = request.args.get("name")
    if not movie_name:
        return jsonify({"error": "Movie name is required"}), 400

    try:
        api_key = "0d1c38a77122f7212cc19086b9fbbdfa"
        tmdb_url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": api_key,
            "query": movie_name,
            "include_adult": False,
            "language": "en-US",
            "page": 1
        }

        response = requests.get(tmdb_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("results"):
            movies = []
            for movie in data["results"]:
                movies.append({
                    "id": movie.get("id"),
                    "title": movie.get("title"),
                    "release_date": movie.get("release_date", "N/A"),
                    "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else "/static/placeholder.jpg",
                    "overview": movie.get("overview", "No overview available."),
                    "rating": movie.get("vote_average", 0),
                    "genre_ids": movie.get("genre_ids", []),
                })
            return jsonify({"results": movies})

        return jsonify({"error": "No movies found"}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):
    try:
        api_key = "0d1c38a77122f7212cc19086b9fbbdfa"
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {
            "api_key": api_key,
            "language": "en-US",
            "append_to_response": "credits,videos,images"
        }

        response = requests.get(details_url, params=params)
        response.raise_for_status()
        movie = response.json()

        processed_data = {
            "id": movie.get("id"),
            "title": movie.get("title"),
            "release_date": movie.get("release_date"),
            "poster": f"https://image.tmdb.org/t/p/w780{movie['poster_path']}" if movie.get("poster_path") else "/static/placeholder.jpg",
            "backdrop": f"https://image.tmdb.org/t/p/w1280{movie['backdrop_path']}" if movie.get("backdrop_path") else "",
            "overview": movie.get("overview"),
            "rating": round(movie.get("vote_average", 0), 1),
            "genres": [g["name"] for g in movie.get("genres", [])],
            "runtime": movie.get("runtime"),
            "tagline": movie.get("tagline"),
            "cast": [{
                "name": member["name"],
                "character": member["character"],
                "photo": f"https://image.tmdb.org/t/p/w185{member['profile_path']}" if member.get("profile_path") else ""
            } for member in movie.get("credits", {}).get("cast", [])[:6]],
            "trailer": next((f"https://www.youtube.com/watch?v={v['key']}" 
                           for v in movie.get("videos", {}).get("results", []) 
                           if v['site'] == 'YouTube' and v['type'] == 'Trailer'), None)
        }

        return render_template("movie_details.html", movie=processed_data)

    except requests.exceptions.RequestException as e:
        return render_template("error.html", error=f"Error fetching data: {str(e)}")
    except Exception as e:
        return render_template("error.html", error=f"Unexpected error: {str(e)}")

@app.route("/search")
def search_results():
    query = request.args.get("query")
    return render_template("search_results.html", search_query=query)

@app.route("/trending")
def get_trending():
    try:
        api_key = "0d1c38a77122f7212cc19086b9fbbdfa"
        url = "https://api.themoviedb.org/3/trending/movie/week"
        params = {"api_key": api_key}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)