# Pagination

Sending massive amounts of data at once is not recommended because it slows down the client since it has to wait for the server to retrieve all that data. The best approach to this problem is to paginate data using request arguments and only send the user the information they need — i.e. batches of information.

We will first start by retrieving all the expenses in our database and then paginating and displaying only a few entries.

**The below code shows a simple route that fetches all the movies in the database and displays them in JSON format**

```python
@app.route('/movies')
def movies():
 movies = Moviee.query.all()
 print(movies)
 results = [movie.format() for movie in movies]
 return jsonify({
   'success':True,
   'results':results,
   'count':len(results)
 })
```
- Suppose we had more than a thousand movies in our database — in that case, retrieving all the data would slow down the server, resulting in a poor user experience.
> Solution:  Flask comes with the paginate() query method that we will use to retrieve limited movies.

The syntax for the paginate query is as follows:

```python
paginate(page=None, per_page=None, error_out=True, max_per_page=None)
```

# Filtering

Filtering allows users to get only the information they require by passing certain query parameters.

Let's assume we want to get all the horror movies in the database. Let's implement this:

**In the code below, we use the attribute ilike to ensure that the query is case insensitive, i.e both “HORROR” and “horror” will give you the correct results.**
```python
@app.route('/horror')
def horror():
  horror_movies= Moviee.query.filter(Moviee.genre.ilike("horror"))
  results = [movie.format() for movie in horror_movies]
  return jsonify({
    'success':True,
    'results':results,
    'count':len(results)
  })
```

# SORTING

Sorting is the process of arranging the query data into specific so that you can analyze it more effectively. You can sort data in:

- Alphabetical order
- Numerical order
- Categories such as year and so on

Let's sort our movies based on the highly-rated movies. The following code shows a list of the five top-rated movies:

```python
@app.route('/rating')
def rating():
  
  rate_movies = Moviee.query.order_by(Moviee.rating.desc()).limit(5).all()

  results = [movie.format() for movie in rate_movies]
  return jsonify({
    'success':True,
    'results':results,
    'count':len(results)
  })
```