# helper functions to get data in and out of database using api
import requests
import json
import yaml

def get_all_parcels(project_id):
# this would make an api request using the project id and get back geo_json

    #api = 'http://api.tiles.mapbox.com/v3/examples.map-zr0njcqy/markers.geojson'
    api = 'http://54.69.121.180:3000/parcels'

    try:
        r = requests.get(api)
        data = r.text
    except requests.exceptions.ConnectionError:
        print '------------------------'
        print 'error'
        print '------------------------'
        data = None


    return data


def get_parcel_geom(project_id):
    example_geom = {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "name": "parcel5",
          "properties": {},
          "geometry": {
            "type": "Polygon",
            "coordinates": [
              [
                [
                  -77.03778505325317,
                  38.894356326330914
                ],
                [
                  -77.037034034729,
                  38.89489074395189
                ],
                [
                  -77.03662633895874,
                  38.89479054095427
                ],
                [
                  -77.0369267463684,
                  38.89343778664929
                ],
                [
                  -77.0384931564331,
                  38.89353799155547
                ],
                [
                  -77.03778505325317,
                  38.894356326330914
                ]
              ]
            ]
          }
        }
      ]
    }

    return example_geom


def get_all_surveys(id):
  survey_json = {
    "survey_id" : "12345",
    "data" : {
       "firstName": "John",
       "lastName": "Smith",
       "age": 25,
       "address":
       {
           "streetAddress": "21 2nd Street",
           "city": "New York",
           "state": "NY",
           "postalCode": "10021"
       },
       "phoneNumber":
       [
           {
             "type": "home",
             "number": "212 555-1234"
           },
           {
             "type": "fax",
             "number": "646 555-4567"
           }
       ]
    }
  }

  return survey_json


#For example sort="Id" or filter="lease"
def list_parcels(id,filter=None,sort=None):

      qs = ""

      if (filter is not None):
          print 'found filter parameter. ', filter
          qs = qs + 'tenure_type=' + filter

      elif (sort is not None):
          qs = qs + 'sort_by=' + sort

      else:
          print 'executing parcel lookup with no filter'

      api = 'http://54.69.121.180:3000/custom/get_parcels_list?' + qs

      r = requests.get(api)

      return r.json()



def list_relationships(id):

    # relationship_list = ['relationship1', 'relationship2', 'relationship3']

    relationship_list = {
       "features": [{
           "relationship_id": "1234",
           "relationship_type": "ownership",
           "relationship_person": {
             "firstname": "john",
             "id": "1234"
             }
           }, {
           "relationship_id": "4343",
           "relationship_type": "renting",
           "relationship_person": {
             "firstname": "sarah",
             "id": "4533"
             }
           }, {
           "relationship_id": "9090",
           "relationship_type": "renting",
           "relationship_person": {
             "firstname": "matt",
             "id": "6565"
             }
            }]
    }

    return relationship_list


def get_person_details(person_id):

    person_json = {
      "firstname": "sarah",
      "lastname": "b",
      "city": "seattle",
      "state": "wa",
      "zip": " ",
      "email": "spatialdev@forever.com",
      "marital_status": "single",
      "education_level": "high-school",
      "id": "12345"
    }
    return person_json


def get_parcel_details(parcel_id):

    parcel_json = {
      "parcel_type" : "individual",
      "landuse" : "residential",
      "parcel_id" : "1234"
    }
    return parcel_json


def get_relationship_details(relationship_id):

  relationship_json = {
    "parcel_id" : "1234",
    "person_id" : "234",
    "tenture_type" : "rent",
    "acquired_date" : "yesterday",
    "how_acquired" : "passed through generations ",
    "time_created" : "3:33"
  }
  return relationship_json


def get_cadasta_activity(project_id):

      api ='http://54.69.121.180:3000/activities'

      r = requests.get(api)

      try:
        data = r.json()
      except ValueError:
        data = None

      return data


