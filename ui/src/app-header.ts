import Vue from "vue";
import { api, api_post, file_api, file_html, loginTool, toastTool } from './common'
import * as config from './config.js'

export let AppHeader = Vue.component('app-header', {
    template: `<div>
        <!-- <div>
        </div> -->
        <nav class="navbar navbar-main" role="navigation" aria-label="main navigation">
            <div class="navbar-elem">
                <!-- <img src="favicon.png" width="32" height="32" /> -->
                <router-link to="/">
                    <h4 class="title is-4">Roman's family</h4>
                </router-link>
            </div>
            <div class="navbar-elem">
                <router-link to="/ui/user" class="button">
                    <i class="fas fa-address-card"></i>&nbsp;
                    {{ userid }}
                </router-link>
            </div>
            <div class="navbar-elem" v-if="canPublish">
                <router-link class="button" v-bind:to="uploadLink">
                    <i class="fas fa-caret-square-up"></i>&nbsp;
                    Upload
                </router-link>
            </div>
        </nav>
        <router-view />
    </div>`,

    computed: {
        userid: function() {
            return loginTool.userid()
        },
        canPublish: function() {
            // TODO well get it from user
            return false
        },
        uploadLink: function() {
            return '/ui/group/' + config.UNPUBLISHED_GROUP
        }
    }
})
