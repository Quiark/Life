import * as _ from "lodash";
import Vue from "vue";

import { rainbow_class } from './common'

let MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

Vue.component('group-pagination', {
    template: `
        <nav id="group-pagination" class="pagination" role="navigation" aria-label="pagination">
            <!-- <a class="pagination-previous">Previous</a>
            <a class="pagination-next">Next page</a> -->
            <a v-bind:class="['button', { 'rotating' : loading }]" 
                v-on:click="$emit('reload')"><i class="fas fa-sync">&nbsp;</i></a>
            <ul class="pagination-list" v-for="page in pagenames">
                <li><router-link
                        v-bind:class="[{ 'is-current': value === page[2]}, 'button', 'pagination-link', 'has-text-centered', display_class(page)]"
                        v-bind:key="page[2]"
                        v-bind:to="'/ui/group/' + groupid + '/page/' + page[2]"
                        disabled-v-on-click="$emit('input', page[2])"
                        >
                    <span class="is-size-5">{{ page[0] }}</span>&nbsp;{{ page[1] }}
                </router-link></li>
            </ul>
        </nav>
    `,
    props: ['pages', 'value', 'groupid', 'loading'],
    computed: {
        pagenames: function() {
            let res = _.keys(this.pages).sort().map((it) => [
                MONTHS[parseInt(it.slice(4, 6)) - 1],
                it.slice(0, 4),
                it
            ])
            return res
        }
    },
    methods: {

        display_class: function(page) {
            return rainbow_class(page[2])
        }

    }
})
