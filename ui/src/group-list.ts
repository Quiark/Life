import * as _ from "lodash";
import Vue from "vue";
import { api, api_post, file_api, file_html, loginTool } from './common'

Vue.component('group-list', {
    template: `
<div class="field">
    <label class="label">Group</label>
    <div class="control">
    <div class="select">
        <select v-model="sel">
            <option 
                v-for="it in groups" 
                v-bind:value="it.groupid">
                {{ it.name }}
            </option>
        </select>
    </div> </div> </div>
    `,

    data: () => ({
        groups: [],
        sel: null
    }),

    watch: {
        sel: function(val) {
            this.$emit('input', val)
        }
    },

    mounted: function() {
        let vm = this
        api('groups').then((it) => {
            vm.groups = [{name: 'null', groupid: null}].concat(it)
        })
    }

})
