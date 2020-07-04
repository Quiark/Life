import * as _ from "lodash";
import Vue from "vue";
import 'whatwg-fetch';

import * as config from './config.js'
import { api } from './common'

Vue.component('upload-box', {
    template: `
    <div class="card">
        <form class="dropzone card-content" 
              id="my-dropzone" 
              ref="form" role="form" 
              method="POST" enctype="multipart/form-data">

            <input type="hidden" v-for="(fval, fkey) in fields" :name="fkey" :value="fval">
            <input type="hidden" name="acl" value="private">

        <div id="uploadbox" class="fallback">
            <label for="file" class="h2">Upload picture</label>
            <input name="file" type="file" class="button" ref="file" @input="onFile" />
            <input type="button" class="button" value="Upload" @click="onSubmit" />
         </div>
      </form>

      <div id="status" ref="status" v-if="statusLoading">
        Opening ...
      </div>

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
        statusLoading: false
    }),

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
                    vm.$refs.form.submit()
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
            this.statusLoading = true

            if (file.type.startsWith('image/')) {
                this.vidLoadHandler = (event) => {
                    vm.previewOnCanvas(canvas, imgEl, imgEl.naturalWidth, imgEl.naturalHeight)
                }
                imgEl.src = blobURL

            } else if (file.type.startsWith('video/')) {
                this.vidLoadHandler = (event) => {
                    vm.previewOnCanvas(canvas, vid, vid.videoWidth, vid.videoHeight)

                    // canvas.toBlob(onPreviewBlob, 'image/jpeg')
                }
                vid.src = blobURL
                vid.load()

            } else return

            // I don't know how to use promises so the callbacks are in reverse order
            let onPreviewBlob = (blob) => {
                // vm.$refs.gen.value = blob
                vm.uploadBlob(blob)
            }
        },

        previewOnCanvas: function(canvas, data, w, h) {
            let ratio = h / w
            canvas.width = config.IMG_PREVIEW_SIZE
            canvas.height = config.IMG_PREVIEW_SIZE * ratio

            let ctx = canvas.getContext('2d');
            ctx.drawImage(data, 0, 0, canvas.width, canvas.height);
        },

        onVideoLoaded: function(evt) {
            console.log('loaded', evt)
            let fn = this.vidLoadHandler
            this.vidLoadHandler = null
            console.log('cleared')
            this.statusLoading = false

            if (fn != null) fn(evt)
        },

        uploadBlob: function(blob) {
            let name = Math.ceil(Math.random() * 1000000)

            let formData = new FormData()

            let allFields = Object.assign({acl: 'private'}, this.fields)
            for (let it in allFields) {
                formData.append(it, allFields[it])
            }
            formData.append(`${name}.jpg`, blob)

            fetch(this.aws_s3_url, {
                method: 'POST',
                body: formData
            })

        },

        uploadBase64: function(payload) {
            let boundary = '----htdoesuibsntiskmjatiuhasind'
            let prefix = 'data:image/jpeg;base64,'
            let dataAscii = payload.substr(prefix.length)
            let arr = [String.fromCharCode(127), String.fromCharCode(128), String.fromCharCode(129)]
            // for (let i = 0; i < 1024; i++) arr[i] = String.fromCharCode(i % 255)
            dataAscii = btoa(arr.join(''))
            // let dataAscii = 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
            // dataAscii += 'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc'
            // dataAscii += 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            let name = Math.ceil(Math.random() * 100000)
            let body = [
                '--' + boundary,
                `Content-Disposition: form-data; name="file"; filename="${name}.jpg"`,
                'Content-Type: image/jpeg',
                '',
                atob(dataAscii),
                '--' + boundary + '--',
                ''
            ]
            let keysBody = []
            let allFields = Object.assign({acl: 'private'}, this.fields)
            for (let it in allFields) {
                keysBody.push('--' + boundary)
                keysBody.push(`Content-Disposition: form-data; name="${it}"`)
                keysBody.push('')
                keysBody.push(allFields[it])
            }


            fetch(/*this.aws_s3_url*/ 'http://localhost:7004/api/filetest', {
                method: 'POST',
                body: ''
                /*
                headers: {
                    'Content-Type': 'multipart/form-data; boundary=' + boundary
                },
                body: keysBody.concat(body).join('\r\n')
                */
            })
        }
    },

    beforeDestroy: function() {
        this.toRelease.map((it) => URL.revokeObjectURL(it))
    }

})
