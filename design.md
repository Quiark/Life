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
