import * as _ from "lodash";
import Vue from "vue";
import 'whatwg-fetch';

import './styles/main.scss';
import { Post, Group, Comment, User } from './data'
import { api, api_post, file_api, file_html } from './common'
import './group-pagination'
import './post-full'


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
			<group-pagination v-bind:pages="groupObj.pages" v-model="currentPage" />

			<post-full 
				v-for="p in content"
				v-bind:key="p.postid"
				v-bind:obj="p">
			</post-full>

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
			vm.current = it.groups[0]
		})
	},

	watch: {
		current: function() {
			let vm = this
			this.getGroup(this.current).then(function(it) {
				// caveat: Vue converts the object into something that only supports the [] operation
				let head = _(it.pages).keys().maxBy((i) => parseInt(i))
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
			return api(`groups/${ group }/page/${ page }`)
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

