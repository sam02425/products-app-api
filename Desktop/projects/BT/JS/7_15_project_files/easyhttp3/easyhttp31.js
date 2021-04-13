/**
 * EasyHTTP Library
 * Library for making HTTP requests
 *
 * @version 3.0.0
 * @author  Brad Traversy
 * @license MIT
 *
 **/

class EasyHTTP {
    // Make an HTTP GET Request


    // get(url) {
    //     return new Promise((resolve, reject) => {
    //         fetch(url)
    //         .then(res => res.json())
    //         .then(data => resolve(data))
    //         .catch(err => reject(err));
    //     });
    // }


    async get(url){
        const response = await fetch(url);
        const resData = await response.json();
        return resData;
    }

    // Make an HTTP POST Request

    // post(url) {
    //     return new Promise((resolve, reject) => {
    //         fetch(url, {
    //               method: 'POST',
    //               headers: {
    //                   'Content-type': 'application/json'
    //               },
    //               body: JSON.stringify(data) 
    // })
    //         .then(res => res.json())
    //         .then(data => resolve(data))
    //         .catch(err => reject(err));
    //     });
    // }

    async post(url, data){
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const resData = await response.json();
        return resData;
    }

    // Make an HTTP PUT Request

    // put(url) {
    //     return new Promise((resolve, reject) => {
    //         fetch(url, {
    //               method: 'PUT',
    //               headers: {
    //                   'Content-type': 'application/json'
    //               },
    //               body: JSON.stringify(data) 
    // })
    //         .then(res => res.json())
    //         .then(data => resolve(data))
    //         .catch(err => reject(err));
    //     });
    // }

    async put(url, data) {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const resData = await response.json();
        return resData;
    }

    // Make an HTTP DELETE Request

    // delete(url) {
    //     return new Promise((resolve, reject) => {
    //         fetch(url, {
    //               method: 'DELETE',
    //               headers: {
    //                   'Content-type': 'application/json'
    //               },
    //               body: JSON.stringify(data) 
    // })
    //         .then(res => res.json())
    //         .then(data => resolve('Resource Deleted..'))
    //         .catch(err => reject(err));
    //     });
    // }

    async delete(url, data) {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const resData = await response.json();
        return resData;
    }

}