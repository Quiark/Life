import Vue from "vue";
import { api, api_post, file_api, file_html, loginTool } from './common'
import * as config from './config.js'

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
            <div class="card" v-for="it in items">
                <div class="card-content">
                    <img width="480" v-bind:src="imgurl(it)" />
                </div>
            </div>
        </div>
    `,

    data: function() {
        return {
            items: []
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
                vm.items = it
            })
        },
        imgurl: function(name) {
            return config.STORAGE_PREFIX + config.UNPUBLISHED_GROUP + '/' + name;
        }
    }

})
