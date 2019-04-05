import * as _ from "lodash";
import Vue from "vue";
import 'whatwg-fetch';
import SureToast from 'vue-sure-toast';
import VueRouter from 'vue-router';

import './styles/main.scss';
import { Post, Group, Comment, User } from './data'
import { api, api_post, file_api, file_html, loginTool, toastTool } from './common'
import * as config from './config.js'
import './group-pagination'
import './post-full'
import './unpublished'

Vue.use(SureToast, {
  position: 'top-center',
  theme: 'warning'
})

Vue.use(VueRouter)

// TODO: create image view container (otherwise no way to go back to previous state)
//      it should also have feature to go to next item
//      ideally without redownloading it


let UserProfile = Vue.component('user-profile', {
    template: `<div> user profile </div>`
})

// Tabbed container of groups
let GroupsDisplay = Vue.component('groups-display', {
	template: `<div id="root" class="">
    {{ current }}
		<div class="groups-tabs tabs is-medium">
			<ul>
				<li	v-for="group in groups"
					v-bind:class="[{ 'is-active': current === group.groupid }]" >

                    <router-link
                        v-bind:key="group.groupid" 
                        v-bind:to="'/ui/group/' + group.groupid"
                        >{{ group.name }}</router-link>
				</li>
			</ul>
		</div>
		<div class="group-content">
            <template v-if="isNotUnpublished">
                <group-pagination v-bind:pages="groupObj.pages" v-bind:groupid="current" />

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
            // current: null as string,  // current group id
            // currentPage: null as string, // page id
            groupObj: { // current
                pages: {}
            } as Group,
            content: [] as Post[],
            user: null as User
        }
	},

    computed: {
        isNotUnpublished: function(): boolean {
            return this.current != config.UNPUBLISHED_GROUP
        },
        current: function(): string {
            // could use props support in vue-router
            return this.$route.params.groupid
        },
        currentPage: function(): string {
            // TODO on page load
            //  - runs computed - current, currentPage
            //  - doesn't run watch
            let head = _(this.groupObj.pages).keys().maxBy((i) => parseInt(i))
            return this.$route.params.pageid || head
        }
    },

	mounted: function() {
		let vm = this

		this.getUser().then(function(it) {
			vm.user = it
        })
        this.getGroups().then(function(it) {
			vm.groups = it
            if (!vm.current) vm.go(it[0].groupid)
		})
        // so basically in here I could already have groupid and pageid even
        // and watch will not be called for them
        this.updateGroup()
	},

	watch: {
		current: function() {
            this.updateGroup()
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
        updateGroup: function() {
            if (!this.current) return
			let vm = this
			this.getGroup(this.current).then(function(it) {
				// caveat: Vue converts the object into something that only supports the [] operation
				vm.groupObj = it
                vm.updateContent()
			})
        },
		updateContent: function() {
            if (!this.currentPage) return
			let vm = this

			this.getContent(this.current, this.currentPage).then(function(it) {
                vm.content = it
			})
        },
        go: function(groupid, pageid) {
            var path = '/ui/group/' + groupid
            if (pageid) path += '/' + pageid
            this.$router.push(path)
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

let router = new VueRouter({
    mode: 'hash',
    base: './',
    routes: [
        { path: '/', component: GroupsDisplay },
        { path: '/ui/user/:userid', component: UserProfile },
        { path: '/ui/group/:groupid', component: GroupsDisplay },
        { path: '/ui/group/:groupid/page/:pageid', component: GroupsDisplay },
        // this would be a different component
        { path: '/ui/group/:groupid/post/:postid', component: GroupsDisplay },
        // this is used after successful login
        { path: '/login/:a/:b', component: GroupsDisplay }
    ]
})


let AppHeader = Vue.component('app-header', {
    template: `<div>
        <nav class="level">
            <div class="level-left">
                <div class="level-item">a regrettable agreement!</div>
            </div>
            <div class="level-right">
                <div class="level-item">{ user.name }</div>
            </div>
        </nav>
        <router-view />
    </div>`,
    router
})

let v = new Vue({
    el: "#vue",
    computed: {
        ViewComponent () {
            if (loginTool.userid() == null) return UnauthComponent
            else return AppHeader
        }
    },

    render (h) { return h(this.ViewComponent) }
})

toastTool.vue = v
