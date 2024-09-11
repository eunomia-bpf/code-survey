# The first mail is  Wed, 13 Feb 2019 16:56:04 -0500
git rev-list --all --objects | grep 'm$' | awk '{print $1}' | wc -l
