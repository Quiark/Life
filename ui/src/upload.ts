import * as _ from "lodash";
import Vue from "vue";

import * as config from './config.js'
import { api } from './common'

Vue.component('upload-box', {
    template: `
    <div class="card">
        <form class="dropzone card-content" id="my-dropzone" role="form" v-bind:action="aws_s3_url" method="POST" enctype="multipart/form-data">

            <input type="hidden" v-for="(fval, fkey) in fields" :name="fkey" :value="fval">
            <input type="hidden" name="acl" value="private">

        <div id="uploadbox" class="fallback">
            <label for="file" class="h2">Upload picture</label>
            <input name="file" type="file" class="button" />
            <input type="submit" class="button" value="Upload" />
         </div>
      </form>

    </div>
    `,

    data: () => ({
        policy: null,
        signature: null,
        access_key: null,
        aws_s3_url: null,
        fields: [],
        //aws_s3_url: `https://${config.UPLOAD_BUCKET}.s3.${config.UPLOAD_ENDPOINT}.amazonaws.com/`,
        //aws_s3_url: `https://${config.UPLOAD_BUCKET}.s3.amazonaws.com/`,
        filename: 'tst.jpg'
    }),

    methods: {
        getTokens: function() {
            let vm = this
            api('upload-details').then((it) => {
                vm.aws_s3_url = it.url
                vm.fields = it.fields
            })
        }
    },

    mounted: function() { this.getTokens() }
})
