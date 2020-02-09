import * as _ from "lodash";
import Vue from "vue";
import * as config from './config.js'

Vue.component('videobox', {
    template: `
    <div v-if="value">
        <p>
        Pozor, videa jsou objemná, hrajte je jen s použitím Wifi.

        Careful, videos use a lot of data.
        </p>

        <div class="button" v-on:click="close">
            Close
        </div>

        <video  controls v-bind:src="value">
        </video>
    </div>
    `,

    props: ['value'],

    methods: {
        close: function() {
            this.$emit('input', null)
        }
    }
})
