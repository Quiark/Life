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
              ref="form" role="form" >

            <div id="uploadbox" class="fallback">
                <label for="file" class="h2">Upload picture</label>
                <input name="file" type="file" class="button" ref="file" @input="onFile" />
                <input type="button" class="button" value="Upload" @click="onSubmit" :disabled="uploadDisabled"/>
                <input type="button" class="button" value="preview" @click="onVideoLoaded" />
             </div>
      </form>


      <div id="status" v-if="status == 'OPENING'">
        Opening ...
      </div>
      <div id="status" v-if="status == 'ERROR'">
        Error ....
      </div>
      <div id="status" v-if="(status == 'UPLOADING') && !uploadDisabled">
        Uploading ....
      </div>
      <!--
      file:
      {{doneFile}}
      preview:
      {{donePreview}}
      exception:
      {{ exception }}
      -->

      <video width="30" controls="true" ref="video" @loadeddata="onVideoLoaded" class="bgprocess" style="" >
      </video>
      <img width="30" ref="loaderImg" class="bgprocess" @load="onVideoLoaded" style=""/>
      <canvas ref="canvas" width="500" style="">
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
        doneFile: false,
        exception: ""
    }),

    computed: {
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
            let parts = file.name.split('.')
            this.ext = parts[parts.length - 1]
            this.doneFile = false
            this.donePreview = false

            if (file.type.startsWith('image/')) {
                this.vidLoadHandler = (event) => {
                    vm.previewOnCanvas(canvas, imgEl, imgEl.naturalWidth, imgEl.naturalHeight)
                }
                imgEl.src = blobURL

            } else if (file.type.startsWith('video/')) {
                this.vidLoadHandler = (event) => {
                    setTimeout(() => {
                        vm.previewOnCanvas(canvas, vid, vid.videoWidth, vid.videoHeight)
                        vm.exception += "previewOnCanvas\n"
                    }, 500)

                }
                vid.src = blobURL
                vid.load()

            } else return
        },

        previewOnCanvas: function(canvas, data, w, h) {
            let ratio = h / w
            canvas.width = config.IMG_PREVIEW_SIZE
            canvas.height = config.IMG_PREVIEW_SIZE * ratio

            let ctx = canvas.getContext('2d')
            ctx.imageSmoothingEnabled = true
            try {
                ctx.drawImage(data, 0, 0, canvas.width, canvas.height)
            } catch (ex) {
                this.exception += this.stringify(ex)
            }
        },


        stringify: function(obj) {
            var result = ''
            for (let k in obj) {

                result += k
                result += '='
                result += obj[k]
                result += '; '
            }
            return result

        },

        // TODO so I think the problem is this gets called too early
        onVideoLoaded: function(evt) {
            this.exception += "onVideoLoaded\n"
            let fn = this.vidLoadHandler
            // this.vidLoadHandler = null
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
