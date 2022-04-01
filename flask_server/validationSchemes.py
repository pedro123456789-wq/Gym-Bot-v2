'''JSON validation schemes for API endpoints'''


'''/api/sign-up'''

signUpSchema = {
    'type' : 'object', 
    'properties' : {
        'username' : {
                        'type' : 'string', 
                        'minLength' : 1, 
                        'maxLength' : 20
                    }, 
        'password' : {
                        'type' : 'string', 
                        'minLength' : 7, 
                        'maxLength' : 40, 
                    }, 
        'email' : {
                    'type' : 'string', 
                    'minLength' : 1, 
                    'maxLength' : 40
        }
    }, 
    'required' : ['username', 'email', 'password']
}



confirmEmailSchema = {
    'type' : 'object', 
    'properties' : {
        'username' : {
            'type' : 'string', 
            'minLength' : 1, 
            'maxLength' : 40
        }, 
        'confirmationCode' : {
            'type' : 'string',
            'length' : 5
        }
    }, 
    'required' : ['username', 'confirmationCode']
}