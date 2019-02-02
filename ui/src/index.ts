import * as _ from "lodash";
import Vue from "vue";
import 'whatwg-fetch';

import './styles/main.scss';
import { Post, Group, Comment, User } from './data'
import { api, api_post, file_api, file_html, loginTool } from './common'
import * as config from './config.js'
import './group-pagination'
import './post-full'
import './unpublished'

// Tabbed container of groups
let MainVue = Vue.component('main-vue', {
	template: `<div id="root" class="">
		<div class="groups-tabs tabs is-medium">
			<ul>
				<li	v-for="group in groups"
					v-bind:class="[{ 'is-active': current === group.groupid }]" >

					<a	v-bind:key="group.groupid" 
						v-on:click="current = group.groupid"
						href="#" >{{ group.name }}</a>
				</li>
			</ul>
		</div>
		<div class="group-content">
            <template v-if="isNotUnpublished">
                <group-pagination v-bind:pages="groupObj.pages" v-model="currentPage" />

                <post-full 
                    v-for="p in content"
                    v-bind:key="p.postid"
                    v-bind:obj="p">
                </post-full>
            </template>
            <unpublished v-else>
            </unpublished>
		</div>
	</div>
	`,
    data: function() {
        return {
            groups: [] as string[],
            current: null as string,  // current group id
            currentPage: null as string, // page id
            groupObj: { // current
                pages: {}
            } as Group,
            content: [] as Post[],
            user: null as User
        }
	},

    computed: {
        isNotUnpublished: function() {
            return this.current != config.UNPUBLISHED_GROUP
        }
    },

	mounted: function() {
		let vm = this
		this.getUser().then(function(it) {
			vm.user = it
        })
        this.getGroups().then(function(it) {
			vm.groups = it
			vm.current = it[0].groupid
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
        getGroups: function() {
            return api('groups')
        },
		getUser: function() {
			return api(`user`)
		},
		updateContent: function() {
			let vm = this

			this.getContent(this.current, this.currentPage).then(function(it) {
                vm.content = it // TODO reverse order, probably on backend
			})
		}
	}
})

let UnauthComponent = { template: `
    <section class="hero is-warning is-bold">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            Missing login
          </h1>
          <h2 class="subtitle">
            Please use the link provided by Roman to log back in. Or ask for a new link.
          </h2>
        </div>
      </div>
    </section>
    ` }

let v = new Vue({
    el: "#vue",
    computed: {
        ViewComponent () {
            if (loginTool.userid() == null) return UnauthComponent
            else return MainVue
        }
    },
    render (h) { return h(this.ViewComponent) }
})
