import * as _ from "lodash";
import Vue from "vue";

import * as config from './config.js'

Vue.component('comment-list', {
    template: `
        <div>
            <article class="message is-small is-primary" v-for="c in comments">
                <div class="message-header">
                    <span>{{ c.author }}</span>
                    <span>{{ c.time }}</span>
                </div>
                <div class="message-body">{{ c.text }}</div>
            </article>
        </div>
    `,
    props: ['comments']
})
