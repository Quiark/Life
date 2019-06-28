import * as _ from "lodash"
import Vue from "vue";
import { api, api_post, file_api, file_html, loginTool, rainbow_class, toastTool, imgurl } from './common'
import * as config from './config.js'
import { Group, PostPayload } from './data'
import './group-list'
import './upload'

class Item {
    id: string
    filename: string
    message: string

    constructor(u: string, f: string, m: string) {
        this.id = u
        this.filename = f
        this.message = m
    }
}

Vue.component('unpublished-item', {
    template: `
            <div class="card" v-bind:class="display_class">
                <div class="card-content">
                    <img width="300" v-bind:src="imgurl(it.filename)" />
                    <div class="field">
                        <label class="label">Your message</label>
                        <div class="control">
                            <textarea class="textarea" 
                                    placeholder="Write post message" 
                                    v-model="it.message"
                                    rows="3" />
                        </div>
                        <group-list v-model="sel_group" no_unpub="true" :groups="grouplist" />
                    </div>
                    <button v-on:click="submit(it)" class="button is-primary"><i class="fas fa-check"></i>&nbsp;Publish</button>
                </div>
            </div>
    `,

    props: ['it', 'grouplist'],

    data: () => ({
        sel_group: null as string
    }),

    computed: {
        display_class: function() {
            return rainbow_class(this.it.id)
        }
    },

    methods: {
        imgurl: function(name: string) {
            return imgurl(config.UNPUBLISHED_GROUP, name)
        },
        submit: function(item: Item) {
            let vm = this
            let post = {
                groupid: this.sel_group,
                text: item.message
            } as PostPayload
            api_post(`groups/unpublished/publish/${item.id}`, post).then((resp) => {
                if (resp.ok) {
                    vm.$emit('published')
                } else {
                    toastTool.handle_err('Cannot publish this post for now, something went wrong', resp)
                }
            })
        }
    }
})


Vue.component('unpublished', {
    // TODO: unify image component (with preview support and click to expand)
    //      with some kind of vue lightbox component
    template: `
        <div>
            <a class="button" v-on:click="refresh()">
                <span class="icon is-small">
                  <i class="fas fa-sync"></i>
                </span>
                <span>Refresh</span>
            </a>
            <upload-box />
            <unpublished-item v-for="it in items" :key="it.id" :it="it" :grouplist="grouplist" v-on:published="onItemPublished(it)" />
        </div>
    `,

    data: function() {
        return {
            items: [] as Item[],
            grouplist: [] as Group[]
        }
    },

    mounted: function() {
        this.refresh()
    },

    methods: {
        getItems: function() {
            return api('groups/unpublished/images')
        },

        getGroups: function() {
            let vm = this
            return api('groups').then((groups) => {
                groups = _.filter(groups, (it) => it.groupid !== config.UNPUBLISHED_GROUP)
                vm.grouplist = [{name: '--', groupid: null}].concat(groups)
            })
        },

        refresh: function() {
            let vm = this
            this.getGroups()
                .then(this.getItems)
                .then((it) => {
                vm.items = _.map(it, (x) => new Item(x.id, x.filename, null))
            })
        },

        onItemPublished: function(evt: Item) {
            console.log('got published event', evt)
            this.items = _.filter(this.items, (it) => it.id !== evt.id)
        }
    }

})
