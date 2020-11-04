#/usr/bin/python3

import csv
import sys

from typing import List, Set, Tuple, Union, Optional
from util import Node, Actor

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

test = 0 # for debugging

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Target Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        # path = [(target, target)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source: str, target: str) -> List[Tuple[str, str]]:
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    proper_path = []

    origin = Actor(source, people)
    destination = Actor(target, people)
    # movies which have had the actor's names extracted
    explored_movies: Set[str] = set()

    # net of connections between actors
    # initalised with all connections to destination
    net = create_nodes(None, destination, explored_movies)

    for node in net:
        # print(movies[node.movie]["title"])
        if matches(node, origin.movies):
            proper_path = create_path(node)
            # print(proper_path)       
            return proper_path
        # keep adding to the end addtional nodes to end of list
        else:
            new_nodes = get_neighbours(node, explored_movies)
            for new_node in new_nodes: 
                net.append(new_node)
    # will be empty - satisfies mypy req
    return proper_path


def create_nodes(parent: Optional[Node], actor: Actor, explored_movies: Set[str]) -> List[Node]:
    nodes = []
    for movie in actor.movies:
        if movie not in explored_movies:
            explored_movies.add(movie)
            node = Node(parent, actor, movie)
            nodes.append(node)
    return nodes


def matches(node: Node, destination_movies: Set[str]) -> bool:
    if node.movie in destination_movies:
        return True
    else:
        return False


def create_path(node: Node, path: List[Tuple[str, str]]=[]) -> List[Tuple[str, str]]: 
    path.append((node.movie, node.actor._id))
    if node.parent is not None:
        return create_path(node.parent, path)
    else:
        return path


def get_neighbours(parent: Node, explored_movies: Set[str]) -> List[Node]:
    # the node in the paramater becomes the parent of the neighbours/children
    # global test # debugging
    neighbours = []
    movie_id = parent.movie
    m_data = movies[movie_id]
    # iterate through all actors in this node's movie
    for actor_id in m_data["stars"]:
        if parent.actor._id != actor_id:
            actor = Actor(actor_id, people)
            # make a node for each of this actor's movies
            # so there will be many nodes for this actor, each of a different movie
            neighbours += create_nodes(parent, actor, explored_movies)
            #for movie in actor.movies:
                # if movie is already in explored movies, then it is already in the list to be explored because i have all the actors already
                # You don't want the same movie twice, even with a different actor. Because when I get a movie, I get all the actors from it
                # and then check their movies against the target.
                # neighbours = create_nodes(parent, actor, explored_movies)
                # if movie not in explored_movies:
                #     explored_movies.add(movie)
                #     new_node = Node(parent, actor, movie)
                #     neighbours.append(new_node)
        # else:
        #     print(test)
        #     test += 1
    return neighbours


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
