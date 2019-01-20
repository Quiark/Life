import * as _ from "lodash"
import Vue from "vue";
import { api, api_post, file_api, file_html, loginTool } from './common'
import * as config from './config.js'
import './group-list'

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
            <div class="card">
                <div class="card-content">
                    <img width="300" v-bind:src="imgurl(it.filename)" />
                    <div class="field">
                        <label class="label">Your message</label>
                        <div class="control">
                            <textarea class="textarea" 
                                    placeholder="Write post message" 
                                    v-model="it.message"
                                    rows="1" />
                        </div>
                        <group-list v-model="gr" />
                        {{ gr }}
                    </div>
                    <button v-on:click="submit(it)" class="button is-primary"><i class="fas fa-check"></i>Publish</button>
                </div>
            </div>
    `,

    props: ['it'],

    data: () => ({
        gr: null
    }),

    methods: {
        imgurl: function(name) {
            return config.STORAGE_PREFIX + config.UNPUBLISHED_GROUP + '/' + name;
        },
        submit: function(item: Item) {
            console.log(item.message)
            api(`groups/unpublished/publish/${item.id}`)
        }
    }
})


Vue.component('unpublished', {
    // TODO: unify image component (with preview support and click to expand)
    template: `
        <div>
            <a class="button" v-on:click="refresh()">
                <span class="icon is-small">
                  <i class="fas fa-sync"></i>
                </span>
                <span>Refresh</span>
            </a>
            <unpublished-item v-for="it in items" :key="it.id" :it="it" />
        </div>
    `,

    data: function() {
        return {
            items: [] as Item[]
        }
    },

    mounted: function() {
        this.refresh()
    },

    methods: {
        getItems: function() {
            return api('groups/unpublished/images')
        },
        refresh: function() {
            let vm = this
            this.getItems().then((it) => {
                vm.items = _.map(it, (x) => new Item(x.id, x.filename, null))
            })
        }
    }

})
