import { apiUrl } from '../GlobalVariables';

// class to make sending requests to the server easier

class RequestHandler {
    static async POST(url: string, payload: { [header: string]: any }): Promise<any> {
        let response = await fetch(`${apiUrl}${url}`, {
            method: 'POST',
            body: JSON.stringify(payload),
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include'
        })

        return await response.json()
    }

    static async PUT(url: string, payload: { [header: string]: any }): Promise<any> {
        let response = await fetch(`${apiUrl}${url}`, {
            method: 'PUT',
            body: JSON.stringify(payload),
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include'
        });

        return await response.json();
    }

    static async GET(url: string, headers: { [header: string]: any }): Promise<any> {
        let response = await fetch(`${apiUrl}${url}`, {
            method: 'GET',
            headers: headers,
            credentials: 'include'
        });

        return await response.json();
    }
}


export default RequestHandler;
