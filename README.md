# Movie Search Backend

The API for the semantic movie search project. 

## Getting Started

To start up the API locally, run 

`docker-compose up --build`

## Making a Request

The API accepts `json` requests. The only required field is `searchText`, and you can optionally specify 'numToReturn', the desired number of movies to return. For example:
```
{ 
  'searchText': 'An exciting sci-fi thriller with stunning visuals in outer space.', 
  'numToReturn': 10
}
```
