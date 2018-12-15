import * as config from './config.js'


export function api(path: string): Promise<any> {
	return fetch(config.API_BASE + path).then((it) => it.json())
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
