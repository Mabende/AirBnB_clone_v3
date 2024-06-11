#!/usr/bin/python3
"""
Handles RESTful API actions for Place objects
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    new_place = Place(city_id=city_id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """Searches for Place objects based on JSON body content"""
    try:
        request_data = request.get_json()
        if request_data is None:
            raise ValueError("Not a JSON")
    except ValueError as e:
        abort(400, str(e))

    states_ids = request_data.get('states', [])
    cities_ids = request_data.get('cities', [])
    amenities_ids = request_data.get('amenities', [])

    if not states_ids and not cities_ids and not amenities_ids:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    # Filter by states
    filtered_places = []
    for state_id in states_ids:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                filtered_places.extend(city.places)

    # Filter by cities
    for city_id in cities_ids:
        city = storage.get(City, city_id)
        if city and city not in filtered_places:
            filtered_places.extend(city.places)

    # Filter by amenities
    amenities = [storage.get(Amenity, amenity_id)
                 for amenity_id in amenities_ids]
    amenities = list(filter(None, amenities))

    if amenities:
        filtered_places = [place for place in filtered_places
                           if all(amenity in place.amenities
                                  for amenity in amenities)]

    return jsonify([place.to_dict() for place in filtered_places])
