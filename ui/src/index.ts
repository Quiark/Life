import * as _ from "lodash";
import Vue from "vue";
import 'whatwg-fetch';

import './styles/main.scss';
import * as config from './config.js'
import './group-pagination'
import './post-full'

// TODO autogenerate
type Post = object
type Group = object
type Comment = object
type User = object

function api(path: string): Promise<any> {
	return fetch(config.API_BASE + path).then((it) => it.json())
}

function file_api(path: string): Promise<any> {
	return fetch(config.STORAGE_PREFIX + path).then((it) => it.json())
}

function file_html(path: string): Promise<string> {
	return fetch(config.STORAGE_PREFIX + path).then((it) => it.text())
}

// Tabbed container of groups
let v = new Vue({
	el: "#vue",
	template: `<div id="root" class="">
		<div class="groups-tabs tabs is-medium">
			<ul>
				<li	v-for="group in groups"
					v-bind:class="[{ 'is-active': current === group }]" >

					<a	v-bind:key="group" 
						v-on:click="current = group"
						href="#" >{{ group }}</a>
				</li>
			</ul>
		</div>
		<div class="group-content">
			<post-full 
				v-for="p in content"
				v-bind:key="p.postid"
				v-bind:obj="p">
			</post-full>

			{{ currentPage }}
			<group-pagination v-bind:pages="groupObj.pages" v-model="currentPage" />
		</div>
	</div>
	`,
	data: {
		groups: [] as string[],
		current: null as string,  // current group id
		currentPage: null as string, // page id
		groupObj: { // current
			pages: {}
		} as Group,
		content: [] as Post[],
		user: null as User
	},

	mounted: function() {
		let vm = this
		this.getUser().then(function(it) {
			vm.user = it
			vm.groups = it.groups
		})
		this.current = this.groups[0]
	},

	watch: {
		current: function() {
			let vm = this
			this.getGroup(this.current).then(function(it) {
				// caveat: Vue converts the object into something that only supports the [] operation
				let head = _(it.pages).keys().head()
				vm.groupObj = it
				vm.currentPage = head
			})
		},
		currentPage: function() {
			this.updateContent()
		}
	},

	methods: {
		getContent: function(group, page) {
			return api(`groups/${ group }/posts/${ page }`)
		},
		getGroup: function(gr) {
			return api(`groups/${ gr }`)
		},
		getUser: function() {
			return api(`user`)
		},
		updateContent: function() {
			let vm = this

			this.getContent(this.current, this.currentPage).then(function(it) {
				vm.content = it
			})
		}
	}
})

