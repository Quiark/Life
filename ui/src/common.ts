import * as config from './config.js'


var currentUser = {
    id: null,
    token: null
}

// either from localSession or from url
// where should this be called?
export function read_login() {
    let parts = window.location.hash.split('/')
    if (parts[0] === '#login') {
        currentUser = {
            id: parts[1],
            token: parts[2]
        }
        localStorage.setItem('currentUser', JSON.stringify(currentUser))

    } else {
        let stored = JSON.parse(localStorage.getItem('currentUser'))
        if (stored != null) currentUser = stored
    }
}

function api_headers() {
    return {
        'Authorization': `${currentUser.id} ${currentUser.token}`
    }
}

export function api(path: string): Promise<any> {
    return fetch(config.API_BASE + path, { headers: api_headers() }).then((it) => it.json())
}

export function api_post(path: string, payload: any): Promise<any> {
	return fetch(config.API_BASE + path, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(payload)
	})
}

export function file_api(path: string): Promise<any> {
	return fetch(config.STORAGE_PREFIX + path).then((it) => it.json())
}

export function file_html(path: string): Promise<string> {
	return fetch(config.STORAGE_PREFIX + path).then((it) => it.text())
}
