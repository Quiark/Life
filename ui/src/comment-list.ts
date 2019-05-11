import * as _ from "lodash";
import Vue from "vue";

import * as config from './config.js'
import './avatar'



Vue.component('comment-list', {
    template: `
        <div>
            <article class="life-comment message media is-small is-primary" v-for="c in comments">
                <avatar :userid="c.author" class="media-left" />
                <div class="message-body media-content">
                    <p v-for="line in splitlines(c.text)">
                        {{ line }}
                    </p>
                    <div class="comment-meta">
                        <span>{{ c.author }}</span>
                        <span>{{ c.time }}</span>
                    </div>
                </div>
            </article>
        </div>
    `,
    props: ['comments'],

    methods: {
        splitlines: function(arg) {
            return arg.split(/\n/g)
        }
    }
})
