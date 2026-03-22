import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from django.conf import settings
from issues.models import CriticalIssue, Issue, LowPriorityIssue
from rest_framework.views import APIView
from rest_framework.response import Response

ISSUE_FILE = settings.ENV_KEYS['ISSUE_FILE']

def validate_issue(data: dict) -> Issue:

    issue: Issue = None

    if data['priority'] == 'critical':
        issue = CriticalIssue(**data)
    elif data['priority'] == 'low':
        issue = LowPriorityIssue(**data)
    else:
        issue = Issue(**data)

    issue.validate()
    return issue

class IssuesView(APIView):

    def get(self, request: Request) -> Response:
        
        #load issues from json file
        with open(ISSUE_FILE, "r") as file:
            issues = json.load(file)
        
        return Response(issues)

    def post(self, request: Request) -> Response:

        #load issues from json file
        with open(ISSUE_FILE, "r") as file:
            issues = json.load(file)

        #create new issue
        new_issue = request.data

        # validate new issue and create response msg.
        issue = validate_issue(new_issue)
        response_data = issue.to_dict()
        response_data['message'] = issue.describe()

        # add new issue to list and save to json file
        issues.append(issue.to_dict())

        with open(ISSUE_FILE, "w") as file:
            json.dump(issues, file, indent=4)
    
        return JsonResponse(response_data, status=201)

