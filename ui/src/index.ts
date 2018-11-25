import * as _ from "lodash";
import Vue from "vue";
import 'whatwg-fetch';

import './styles/main.scss';
import * as config from './config.js'


let page = '201811'
let groups = [config.FIRST_GROUP, 'kungfu', 'matrix.org']

function api(path: string): Promise<any> {
	return fetch(config.API_BASE + path).then((it) => it.json())
}

function file_api(path: string): Promise<any> {
	return fetch(config.STORAGE_PREFIX + path).then((it) => it.json())
}

function file_html(path: string): Promise<string> {
	return fetch(config.STORAGE_PREFIX + path).then((it) => it.text())
}

function get_page_contents(group:string, page: string): Promise<string[]> {
	return file_api(`${ group }/${ page }.json`).then((it: string[]) => {
		return Promise.all(
				it.map((p) => file_html(`${ group }/${ p }.html`)))
	})
}

let v = new Vue({
	el: "#vue",
	template: `<div id="root">
		<div class="groups-tabs">
			<span	v-for="group in groups"
					v-bind:class="['tab-button', { active: current === group }]" >

				<a	v-bind:key="group" 
					v-on:click="current = group"
					href="#" >{{ group }}</a>
			</span>
		</div>
		<div class="group-content" >
			<div class="post" v-for="p in content">
				<div v-html="p" />
			</div>
		</div>
	</div>
	`,
	data: {
		groups: groups,
		current: groups[1],
		content: []
	},
	mounted: function() {
		this.current = this.groups[0]
	},
	watch: {
		current: function() {
			let vm = this
			this.getContent(this.current).then(function(it) {
				vm.content = it
			})
		}
	},
	methods: {
		getContent: function(gr) {
			return get_page_contents(gr, page)
		}
	}
})

