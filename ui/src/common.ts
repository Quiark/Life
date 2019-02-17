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

class ToastTool {

    vue: any;

    public handle_err(msg: string, debug_obj) {
        console.error(msg, debug_obj)

        this.vue.$sureToast.show(msg);
    }

}

export let loginTool = new LoginTool()
export let toastTool = new ToastTool();

function api_headers() {
    return {
        'Authorization': `${loginTool.userid()} ${currentUser.token}`
    }
}

function api_error_handler(resp) {
    if (resp.ok)
        return resp
    else {
        toastTool.handle_err('Something went wrong', [resp])
    }

}

// note that this one handles response automatically and returns json
export function api(path: string): Promise<any> {
    return fetch(config.API_BASE + path, { headers: api_headers() })
            .then(api_error_handler)
            .then((resp) => resp.json())
}

export function api_post(path: string, payload: any): Promise<any> {
	return fetch(config.API_BASE + path, {
		method: 'POST',
		headers: _.assign(api_headers(), {
			'Content-Type': 'application/json'
		}),
		body: JSON.stringify(payload)
    }).then(api_error_handler)
}

export function file_api(path: string): Promise<any> {
    return fetch(config.STORAGE_PREFIX + path, { headers: api_headers() }).then((it) => it.json())
}

export function file_html(path: string): Promise<string> {
	return fetch(config.STORAGE_PREFIX + path).then((it) => it.text())
}

export function imgurl(groupid: string, name: string): string {
    let start = ''
    if (config.LOCAL && config.STORAGE_IMPL == 's3')
        start = config.BUCKET_URL

    /*
https://s3.ap-northeast-2.amazonaws.com/life.rplasil.name/storage/keCxhEChibx-unpublished/p300-217bb62ab8be5f8c1d519d22cf8182cd.jpg
http://life.rplasil.name.s3-website.ap-northeast-2.amazonaws.com/storage/keCxhEChibx-unpublished/p300-02d0fc3a4243387758aec3b96e201548.jpg
     */

    return start + config.STORAGE_PREFIX + groupid + '/' + name;
    
}

export function rainbow_class(id: string): string {
    return 'rainbow-edge' + (parseInt(id) % 6)
}
