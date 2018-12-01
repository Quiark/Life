import * as _ from "lodash";
import Vue from "vue";

import * as config from './config.js'

Vue.component('post-full', {
    template: `
        <div class="post card">
            <div class="card-content">
                <div class="content">
                    {{ obj.text }}
                </div>
                <img width="480" height="230" v-bind:src="imgurl" />
            </div>
            <footer class="card-footer">
                {{ obj.time }}
            </footer>
        </div>
    `,
    props: ['obj'],

    computed: {
        imgurl: function() {
            return config.STORAGE_PREFIX + this.obj.groupid + '/' + this.obj.postid + '.jpg'
        }
    }
})
