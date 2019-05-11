import Vue from "vue";

import * as config from './config.js'
import { imgurl } from './common'

Vue.component('avatar', {
    template: `
    <div class="avatar">
        <img :src="imgurl" width="64" />
    </div>
    `,

    props: ['userid'],
    computed: {
        imgurl: function() {
            return imgurl('avatars', this.userid + '.jpg')
        }
    }
})
