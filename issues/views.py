import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from django.conf import settings
from issues.models import PRIORITY_STATUS, ISSUE_STATUS, CriticalIssue, Issue, LowPriorityIssue, Reporter
from rest_framework.views import APIView
from rest_framework.response import Response

ISSUE_FILE = settings.ENV_KEYS['ISSUE_FILE']
REPORTER_FILE = settings.ENV_KEYS['REPORTER_FILE']

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

def get_issue_handler(request: Request, issues: list) -> Response:

    priority = request.query_params.get('priority')
    status = request.query_params.get('status')
    id = request.query_params.get('id')

    filtered_issues = issues

    # Validate unknown params
    allowed_params = {"id", "status", "priority"}
    for key in request.query_params.keys():
        if key not in allowed_params:
            return Response(
                {"error": f"Invalid query param '{key}'"},
                status=400
            )

    # case where priority as query param.
    if priority:
        if priority not in PRIORITY_STATUS:
            return Response({"error": "Invalid priority value provided."}, status=400)
        
        filtered_issues = [issue for issue in filtered_issues if issue['priority'] == priority]

        if len(filtered_issues) == 0:
            return Response({"message": "No issues found with the specified priority."}, status=404)
        
    # case where status as query param.
    if status:
        if status not in ISSUE_STATUS:
            return Response({"error": "Invalid status value provided."}, status=400)

        filtered_issues = [issue for issue in filtered_issues if issue['status'] == status]

        if len(filtered_issues) == 0:
            return Response({"message": "No issues found with the specified status."}, status=404)
    
    # case where id as query param.
    if id:
        if not id.isdigit():
            return Response({"error": "ID must be a valid integer."}, status=400)

        int_id = int(id)
        filtered_issues = [issue for issue in filtered_issues if issue['id'] == int_id]

        if len(filtered_issues) == 0:
            return Response({"message": "No issues found with the specified id."}, status=404)

    # default case of returning all issues.
    return Response(filtered_issues)

class IssuesView(APIView):

    def get(self, request: Request) -> Response:
        

        #load issues from json file
        with open(ISSUE_FILE, "r") as file:
            issues = json.load(file)
        
        return get_issue_handler(request, issues)

    def post(self, request: Request) -> Response:

        try:
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

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
    
        return JsonResponse(response_data, status=201)



def  get_reporter_handler(request: Request, reporters: list) -> Response:

    id = request.query_params.get('id')

    filtered_reporters = reporters

    # Validate unknown params
    allowed_params = {"id"}
    for key in request.query_params.keys():
        if key not in allowed_params:
            return Response(
                {"error": f"Invalid query param '{key}'"},
                status=400
            )

    # case where id as query param.
    if id:
        if not id.isdigit():
            return Response({"error": "ID must be a valid integer."}, status=400)

        int_id = int(id)
        filtered_reporters = [reporter for reporter in filtered_reporters if reporter['id'] == int_id]

        if len(filtered_reporters) == 0:
            return Response({"message": "No reporters found with the specified id."}, status=404)

    # default case of returning all reporters.
    return Response(filtered_reporters)


def validate_reporter(data: dict) ->Reporter:
    reporter = Reporter(**data)
    reporter.validate()
    return reporter

class ReportersView(APIView):

    def get(self, request:Request) -> Response:
        
        with open(REPORTER_FILE, "r") as file:
            reporters = json.load(file)

        return get_reporter_handler(request, reporters)

    def post(self, request:Request) -> Response:

        try:
        
            with open(REPORTER_FILE, "r") as file:
                reporters = json.load(file)

            new_reporter = request.data

            reporter = validate_reporter(new_reporter) 
            response_data = reporter.to_dict()
            
            reporters.append(response_data)

            with open(REPORTER_FILE, "w") as file:
                json.dump(reporters, file, indent=4)

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

        return JsonResponse(response_data, status=201)

