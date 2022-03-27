from flask import make_response, jsonify


def custom_response(success: bool, message: str, errorCode: int = 400, **others):
    new_response = make_response(jsonify({
        'success' : success, 
        'message' : message,
        **others
    }))

    new_response.status_code = 200 if success else errorCode
    return new_response