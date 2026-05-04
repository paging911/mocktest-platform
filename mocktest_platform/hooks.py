app_name = "mocktest_platform"
app_title = "Mock Test Platform"
app_publisher = "Custom"
app_description = "Mock test engine for Frappe LMS and ERPNext"
app_email = "admin@example.com"
app_license = "MIT"

doctype_js = {
    "MT Exam": "public/js/mt_exam.js",
}

website_route_rules = [
    {"from_route": "/mock-tests", "to_route": "mock_tests"},
    {"from_route": "/mock-test/<exam>", "to_route": "mock_test"},
    {"from_route": "/mock-test-attempt/<attempt>", "to_route": "mock_test_attempt"},
    {"from_route": "/mock-test-result/<attempt>", "to_route": "mock_test_result"},
]
