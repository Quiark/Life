import * as _ from "lodash";
import Vue from "vue";
import 'whatwg-fetch';

import * as config from './config.js'
import { api } from './common'

enum UploadStatus {
    OPENING = 'OPENING',
    UPLOADING = 'UPLOADING',
    ERROR = 'ERROR'
}

Vue.component('upload-box', {
    template: `
    <div class="card">
        <form class="dropzone card-content" 
              id="my-dropzone" 
              ref="form" role="form" 
              method="POST" enctype="multipart/form-data">

            <input type="hidden" v-for="(fval, fkey) in fields" :name="fkey" :value="fval" />
            <input type="hidden" name="acl" value="private" />
            <input type="hidden" name="key" v-bind:value="fullUploadKey" />

        <div id="uploadbox" class="fallback">
            <label for="file" class="h2">Upload picture</label>
            <input name="file" type="file" class="button" ref="file" @input="onFile" />
            <input type="button" class="button" value="Upload" @click="onSubmit" :disabled="uploadDisabled"/>
         </div>
      </form>

      <div id="status" v-if="status == 'OPENING'">
        Opening ...
      </div>
      <div id="status" v-if="status == 'ERROR'">
        Error ....
      </div>
      <div id="status" v-if="status == 'UPLOADING'">
        Uploading ....
      </div>
      <!--
      file:
      {{doneFile}}
      preview:
      {{donePreview}}
      -->

      <video width="30" controls="true" ref="video" @loadeddata="onVideoLoaded" class="bgprocess" >
      </video>
      <img width="30" ref="loaderImg" class="bgprocess" @load="onVideoLoaded" />
      <canvas ref="canvas" width="500">
      </canvas>
    </div>
    `,

    data: () => ({
        policy: null,
        signature: null,
        access_key: null,
        aws_s3_url: null,
        fields: [],
        // blob URLs to release
        toRelease: [] as string[],
        // to be able to use closure. Also used for image
        vidLoadHandler: null as ((evt) => void),
        status: null as UploadStatus,  // TODO can this be derived from other props?
        filename: null as string,
        ext: null as string,
        donePreview: false, // success upload of preview?
        doneFile: false
    }),


    // TODO need to inform when *both* thnigs are done uploading

    computed: {
        fullUploadKey: function() {
            return `${config.STORAGE_PREFIX}/${config.UNPUBLISHED_GROUP}/${this.filename}.${this.ext}`
        },
        uploadDisabled: function() {
            return (this.status == UploadStatus.OPENING) || (this.doneFile && this.donePreview)
        }
    },

    methods: {
        getTokens: function() {
            let vm = this
            return api('upload-details').then((it) => {
                vm.aws_s3_url = it.url
                vm.fields = it.fields
            })
        },

        onSubmit: function() {
            let vm = this
            this.getTokens().then((it) => {
                this.$nextTick(() => {
                    vm.status = UploadStatus.UPLOADING
                    if (!vm.donePreview) vm.uploadPreview()
                    if (!vm.doneFile) vm.uploadFile()
                })
            })
        },

        onFile: function() {
            let vm = this
            let vid = this.$refs.video
            let canvas = this.$refs.canvas
            let fileEl = this.$refs.file
            let imgEl = this.$refs.loaderImg

            let file = fileEl.files[0]

            let blobURL = URL.createObjectURL(file)
            this.toRelease.push(blobURL)
            this.status = UploadStatus.OPENING
            this.filename = Math.ceil(Math.random() * 1000000)
            this.ext = file.name.split('.')[1]
            this.doneFile = false
            this.donePreview = false

            if (file.type.startsWith('image/')) {
                this.vidLoadHandler = (event) => {
                    vm.previewOnCanvas(canvas, imgEl, imgEl.naturalWidth, imgEl.naturalHeight)
                }
                imgEl.src = blobURL

            } else if (file.type.startsWith('video/')) {
                this.vidLoadHandler = (event) => {
                    vm.previewOnCanvas(canvas, vid, vid.videoWidth, vid.videoHeight)

                }
                vid.src = blobURL
                vid.load()

            } else return
        },

        previewOnCanvas: function(canvas, data, w, h) {
            let ratio = h / w
            canvas.width = config.IMG_PREVIEW_SIZE
            canvas.height = config.IMG_PREVIEW_SIZE * ratio

            let ctx = canvas.getContext('2d');
            ctx.drawImage(data, 0, 0, canvas.width, canvas.height);
        },

        onVideoLoaded: function(evt) {
            let fn = this.vidLoadHandler
            this.vidLoadHandler = null
            this.status = null

            if (fn != null) fn(evt)
        },

        uploadPreview: function() {
            let vm = this
            let canvas = this.$refs.canvas
            let onPreviewBlob = (blob) => {
                vm.uploadBlob(blob, `p500-${this.filename}.jpg`).then((ok) => {
                    vm.donePreview = true
                }, (err) => {
                    vm.donePreview = false
                })
            }
            canvas.toBlob(onPreviewBlob, 'image/jpeg')
        },

        uploadFile: function() {
            let fileEl = this.$refs.file
            let file = fileEl.files[0]
            let vm = this
            this.uploadBlob(file, this.filename + '.' + this.ext).then((ok) => {
                vm.doneFile = true
            }, (err) => {
                console.log('request failed', err)
                vm.doneFile = false
            })

        },

        uploadBlob: function(blob, name) {
            let formData = new FormData()
            let vm = this

            let allFields = Object.assign({acl: 'private'}, this.fields)
            for (let it in allFields) {
                formData.append(it, allFields[it])
            }
            formData.append('file', blob, name)

            return fetch(this.aws_s3_url, {
                method: 'POST',
                mode: 'no-cors',
                body: formData
            })        
            // note: it rejects only on network error, not on receiving 404
        }
    },

    beforeDestroy: function() {
        this.toRelease.map((it) => URL.revokeObjectURL(it))
    }

})
