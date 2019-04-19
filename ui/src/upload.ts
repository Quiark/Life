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

        <div class="fallback">
            <div for="file">Upload picture</div>
            <input name="file" type="file" class="button" />
            <input type="submit" class="button" />
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

    mounted: function() {
        let vm = this
        api('upload-details').then((it) => {
            vm.aws_s3_url = it.url
            vm.fields = it.fields
        })
    }
})
