import * as _ from "lodash";
import * as config from './config.js'


var currentUser = {
    id: null,
    token: null
}

class LoginTool {
    
    // either from localSession or from url
    // where should this be called?
    public read_login() {
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

    public userid() {
        if (currentUser.id == null) this.read_login()
        return currentUser.id
    }

}

export let loginTool = new LoginTool()

function api_headers() {
    return {
        'Authorization': `${loginTool.userid()} ${currentUser.token}`
    }
}

export function api(path: string): Promise<any> {
    return fetch(config.API_BASE + path, { headers: api_headers() }).then((it) => it.json())
}

export function api_post(path: string, payload: any): Promise<any> {
	return fetch(config.API_BASE + path, {
		method: 'POST',
		headers: _.assign(api_headers(), {
			'Content-Type': 'application/json'
		}),
		body: JSON.stringify(payload)
	})
}

export function file_api(path: string): Promise<any> {
    return fetch(config.STORAGE_PREFIX + path, { headers: api_headers() }).then((it) => it.json())
}

export function file_html(path: string): Promise<string> {
	return fetch(config.STORAGE_PREFIX + path).then((it) => it.text())
}
