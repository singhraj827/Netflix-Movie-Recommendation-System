from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load the saved data
try:
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movie_list = movies['title'].tolist()  # Convert to list for better lookup
except Exception as e:
    print("Error loading data:", e)
    movies = None
    similarity = None
    movie_list = []

def recommend(movie):
    if movie not in movie_list:
        return ["Movie not found! Please try another movie."]
    
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        recommended_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommendations = [movies.iloc[i[0]]['title'] for i in recommended_indices]
        return recommendations
    except Exception as e:
        print("Error in recommendation function:", e)
        return ["Error generating recommendations."]

@app.route('/')
def home():
    return render_template('index.html', movies=movie_list)

@app.route('/recommend', methods=['POST'])
def recommend_movies():
    try:
        data = request.json
        movie_name = data.get('movie', '').strip()
        if not movie_name:
            return jsonify(["Please enter a movie name."])
        
        recommended_movies = recommend(movie_name)
        return jsonify(recommended_movies)
    except Exception as e:
        print("Error in /recommend:", e)
        return jsonify(["Error processing request."])

if __name__ == '__main__':
    app.run(debug=True)
