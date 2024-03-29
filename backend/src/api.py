import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from urllib.request import urlopen
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
from flasgger import Swagger

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    !! Running this funciton will add one
'''

db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
         or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])

def getDrinks():
    drinks = Drink.query.all()
    allDrinks = [drink.short() for drink in drinks]
    return jsonify({
        "success": True,
        "drinks": allDrinks
    }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')

def drinksDetail(payload):
    try:
        drinks = Drink.query.all()

        allDrinks = [drink.long() for drink in drinks]
        return jsonify({
            "success": True,
            "drinks": allDrinks
        }), 200
    except:
        abort(422)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')

def postDrinks(payload):
    body = request.get_json()

    requestedTitle = body.get('title', None)
    requestedRecipe = body.get('recipe', None)
     # Get the response data
    newDrink = Drink(
        title=requestedTitle,
        recipe=json.dumps(requestedRecipe)) #dumps - Converts a Python Object into a JSON String
    try:
        newDrink.insert()

        return jsonify({
            "success": True,
            "drinks": [newDrink.long()]
        }), 200
        
    except:
        abort(422)



'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patchDrinks(jwt, drink_id):
    body = request.get_json()

    #requestedId = body.get('id')
    requestedTitle = body.get('title', None)
    requestedRecipe = body.get('recipe', None)

    try:
        drinks = Drink.query.filter_by(id=drink_id).one_or_none()
        if drinks is None:
            abort(404)
        if (requestedTitle or requestedRecipe) is None:
            abort(400)

        drinks.update()
        print('yesss')
        
        updatedDrink = Drink.query.filter_by(id=drink_id).first()

        return jsonify({
            'success': True,
            'drinks': [updatedDrink.long()]
        }), 200
        print('y!!!!!')


    except Exception as e:
        print(e)
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def deleteDrinks(jwt, drink_id):
    requestedId = request.form.get('id')
    requestedTitle = request.form.get('title')
    requestedRecipe = request.form.get('recipe')
    try:
        Drink(id=requestedId, 
            title=requestedTitle,
            recipe=json.dumps(requestedRecipe)).insert()
        print('iAmWorking')

        drinks = Drink.query.filter(Drink.id == drink_id).one_or_none()
        print('iAmRunning')
        if drinks is None:
            abort(404)
        
        drinks.delete()

        return jsonify({
            'success': True,
            'delete': drink_id
        }), 200

    except:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422



@app.errorhandler(400)
def badRequest(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401
    

@app.errorhandler(405)
def notAllowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Not Allowed error"
    }), 405


@app.errorhandler(500)
def internalServer(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server error"
    }), 500
'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def resourceNotFound(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def authError(ex):
    response = jsonify(ex.error),
    response.status_code = ex.status_code,
    return jsonify({
        "success": False,
        "error": response.status_code,
        "message": "response.status_code"
    })