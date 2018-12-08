import * as _ from "lodash";
import Vue from "vue";

import * as config from './config.js'

Vue.component('comment-list', {
    template: `
        <div>
            <article class="life-comment message is-small is-primary" v-for="c in comments">
                <div class="message-body">
                    {{ c.text }}
                    <div class="comment-meta">
                        <span>{{ c.author }}</span>
                        <span>{{ c.time }}</span>
                    </div>
                </div>
            </article>
        </div>
    `,
    props: ['comments']
})
