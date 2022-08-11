from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
from Movie import Movie


mydb = mysql.connector.connect(host="localhost",user="root",password="",database="python")

mycursor = mydb.cursor()

app = FastAPI()

					#0					1
# movies = [{"title":"","year":0},
# 		  {"title":"Batman","year":2021},
# 		  {"title":"Joker","year":2022},
# 		  {"title":"Lion King","year":1999},
# 		  {"title":"Snow white","year":1998},
# 		  {"title":"Ice age","year":2012}]



@app.get("/")
async def root():
	return {"message":"welcome"}

#get all movies
@app.get("/movies")
def get_movies():
	sql = "SELECT * FROM movies"
	mycursor.execute(sql)
	movies = mycursor.fetchall()
	return movies

#get single movie by id
@app.get("/movie/{movie_id}")
def get_movie(movie_id:int):
	sql = "SELECT * FROM movies WHERE id = %s"
	val = (movie_id,)
	mycursor.execute(sql,val)
	movie = mycursor.fetchall() #[[]]
	return movie[0]

#get single movie by title
@app.get("/movie_by_title/{movie_title}")
def get_movie_by_title(movie_title:str):
	sql = "SELECT * FROM movies WHERE title = %s"
	val = (movie_title,)
	mycursor.execute(sql,val)
	movie = mycursor.fetchall() # [[]]
	if len(movie) == 0:
		raise HTTPException(status_code=500,detail="Movie not found")
	return movie[0]



@app.delete("/movie/{movie_id}")
def delete_movie(movie_id:int):
	sql = "DELETE FROM movies WHERE id = %s"
	val = (movie_id,)
	mycursor.execute(sql,val)
	mydb.commit()
	return {"message":"movie has been deleted successfully"}	



#create movie
@app.post("/create_movie")
def create_movie(movie:Movie):
	sql = "INSERT INTO movies (title,year,storyline) VALUES (%s,%s,%s)"
	val = (movie.title, movie.year,movie.storyline)
	mycursor.execute(sql,val)
	mydb.commit()
	return movie


#update movie
@app.post("/update_movie")
def update_movie(movie:Movie,movie_id:int):
	sql = "UPDATE movies SET title = %s , year = %s , storyline = %s WHERE id = %s"
	val = (movie.title,movie.year, movie.storyline, movie_id)
	mycursor.execute(sql,val)
	mydb.commit()
	return movie










# uvicorn main:app --reload