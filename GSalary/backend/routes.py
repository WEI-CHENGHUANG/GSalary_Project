# import sys


# sys.path.append("..")
# print(sys.path)

from model.api_posts import postsContent, allPostsContent
from model.api_members import userIdentification, memberInfo
from model.api_homepage import salary, languages, jobposts
from model.api_each_state import getstateInfo

from model.api_google import logInByGoogle


def routes(api):
    api.add_resource(salary, "/api/salary")
    api.add_resource(languages, "/api/languages")
    api.add_resource(jobposts, "/api/jobposts")
    api.add_resource(userIdentification, "/api/user")
    api.add_resource(memberInfo, "/api/member")
    api.add_resource(postsContent, "/api/post")
    api.add_resource(allPostsContent, "/api/posts")
    api.add_resource(getstateInfo, "/api/stateInfo")
    api.add_resource(logInByGoogle, "/api/google")
