from __future__ import annotations
from typing import Set, Dict, Any, Optional


class Node():
    def __init__(self, parent: Optional[Node], actor: Actor, movie: str):
        # self.state = state
        self.parent = parent # parent is a node also
        self.actor = actor
        # each node has its own actor movie pair - its like an x y coord so of course there are repeats.
        self.movie = movie 


class Actor():

    def __init__(self, _id: str, people:Dict[str, Dict[str, Any]]):
        # self.name = name # string of actor's name
        self._id = _id
        self.movies = self.__get_movies(people)


    # get list of all actor's movies
    def __get_movies(self, people: Dict[str, Dict[str, Any]]) -> Set[str]:
        # get list of movies from an actor's id
        movies = people[self._id]["movies"]
        return movies