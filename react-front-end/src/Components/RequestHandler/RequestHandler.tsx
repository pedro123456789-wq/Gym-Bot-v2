import {apiUrl} from '../GlobalVariables';


class RequestHandler{
    static async Post(url : string, payload: {[header: string] : any}): Promise<any>{
       let response = await fetch(`${apiUrl}${url}`, {
           method: 'POST', 
           body: JSON.stringify(payload), 
           headers: {'Content-Type' : 'application/json'}, 
           credentials: 'include'
       })

       return await response.json()
    }
}


export default RequestHandler;
