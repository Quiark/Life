import * as _ from "lodash"
import Vue from "vue"

import { api, api_post, file_api, file_html, rainbow_class, imgurl } from './common'
import { Post, Group, Comment, User } from './data'
import * as config from './config.js'
import './comment-list'

Vue.component('post-full', {
    template: `
        <div class="post card" v-bind:class="display_class">
            <div class="card-content">
                <div class="content">
                    {{ obj.text }}
                </div>
                <img  v-bind:width="previewSize" v-bind:src="imgurl" />

				<comment-list v-bind:comments="obj.comments"/>
				<div class="columns is-gapless">
					<div class="column is-four-fifths">
						<textarea class="textarea" 
							placeholder="your comment" 
							v-model="commentInput"
							rows="1" />
					</div>
					<div class="column">
						<button v-on:click="submit()" class="button is-primary"><i class="fas fa-check"></i></button>
					</div>
				</div>
            </div>
            <footer class="card-footer">
				<a v-bind:href="posturl">
					{{ obj.time }}
				</a>
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
        imgurl: function() {
            return imgurl(this.obj.groupid, config.IMG_PREVIEW_PREFIX + this.obj.postid + '.jpg')
		},
		posturl: function() {
			return `/ui/groups/${ this.obj.groupid }/posts/${ this.obj.postid }`
        },
        display_class: function() {
            return rainbow_class(this.obj.postid)
        }
	},

	methods: {
		submit: function() {
			let vm = this
			api_post(`groups/${ this.obj.groupid }/posts/${ this.obj.postid }/comments`,
				{'text': vm.commentInput}).then(function() {
					// TODO
					vm.obj.comments.push({text: vm.commentInput})
					vm.commentInput = null
			})
		}
	}
})
