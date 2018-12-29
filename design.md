# Entities

User - a specific person with their token / login

Group - the minimal unit of post sharing, consists of users


# Access Control

## Initial simple phase

Serve pics from unguessable folders in S3, per Group.

life-rplasil.s3.aws.amazon.com/hc849bxC42hx94ci7-baby/pic001.jpg

-> probably useless as I need cloudfront anyway to have a custom domain rather than s3.aws

HTML fragments similarly using the same strategy.

## Actual secure phase

Use signed cookies with CloudFront

# Architecture

Static files served from S3, including post HTML fragments and opening page.

API served from now.sh

# API calls

display main page
  - get list of groups from current user
  - (later) each group should have display name and color or icon

display group
  - get list of pages (months) 
	- in group metadata, at least year-wise
  - get list of posts in month

create post
  - take picture
  - resize
  - add to page index
  - allow editing text
  - add to database

append comment
  - some kind of ID for post
  - update item in database

# DynamoDB tables design

## Posts ##

operations
* add post: increment in-page ix
* get,update post by groupid + postid
* get posts by groupid + page 

Access pattern: pretty much only the last page (month).

# Uploading pics

Upload pics to `UPLOAD_BUCKET`, they will be resized and placed into 
`$UNPUBLISHED_GROUP` as both `$UUID.jpg` and `$IMG_PREVIEW_PREFIX-$UUID.jpg`

todo:
 + generating random name
 - setting permissions


checklist:
 * deploy/resizer/config.json needs to be updated to match config.py values, dont have / before 'storage'
