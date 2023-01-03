from flask import make_response, jsonify


def customResponse(success: bool, message: str, errorCode: int = 400, **extraHeaders):
    # return json dictionary as response with standard format
    new_response = make_response(jsonify({
        'success' : success, 
        'message' : message,
        **extraHeaders
    }))

    new_response.status_code = 200 if success else errorCode
    return new_response