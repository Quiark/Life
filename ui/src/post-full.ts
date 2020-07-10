import * as _ from "lodash"
import Vue from "vue"

import { api, api_post, file_api, file_html, rainbow_class, imgurlForPost, loginTool } from './common'
import { Post, Group, Comment, User } from './data'
import * as config from './config.js'
import './comment-list'

Vue.component('post-full', {
    template: `
        <div class="post card" v-bind:class="display_class">
            <div class="card-content">
                <div class="content">
                    <p v-for="line in text_lines">
                        {{ line }}
                    </p>
                </div>
                <img 
                    v-bind:width="previewSize" 
                    v-lazy="imgurlPreview"
                    @click="on_img_click"
                    />

                <span class="sidebar">
                <div class="button" >
                    <a :href="imgurlFull" download><i class="fas fa-download"></i></a>
                </div>
                </span>
				<comment-list v-bind:comments="obj.comments"/>
				<div class="comment-writing">
                    <div class="comment-textarea">
                        <textarea class="textarea" 
                            placeholder="your comment" 
                            v-model="commentInput"
                            rows="1" />
                    </div>
                    <div>
                        <button v-on:click="submit()" class="button is-primary"><i class="fas fa-check"></i></button>
                    </div>
				</div>
            </div>
            <footer class="card-footer">
				<router-link v-bind:to="posturl">
					{{ obj.time }}
				</router-link>
            </footer>
        </div>
    `,
    props: ['obj'],
	data: function() {
        return {
            commentInput: null,
            previewSize: config.IMG_PREVIEW_SIZE
        }
	},

    computed: {
        imgurlPreview: function() {
            return imgurlForPost(this.obj, true)
		},
        imgurlFull: function() {
            return imgurlForPost(this.obj, false)
		},
		posturl: function() {
            // having the optional params on router makes the trailing / required
            return `/ui/group/${ this.obj.groupid }/post/${ this.obj.postid }`
        },
        display_class: function() {
            return rainbow_class(this.obj.postid)
        },
        text_lines: function() {
            return this.obj.text.split(/\n/g)
        },
        isVideo: function() {
            this.obj.format != 'jpg'
        }
	},

	methods: {
		submit: function() {
			let vm = this
			api_post(`groups/${ this.obj.groupid }/posts/${ this.obj.postid }/comments`,
				{'text': vm.commentInput}).then(function() {
					// TODO
                    vm.obj.comments.push({
                        text: vm.commentInput,
                        author: loginTool.userid()
                    })
					vm.commentInput = null
			})
        },
        on_img_click: function() {
            this.$emit('post-enlarge', this.obj)
        }
	}
})
