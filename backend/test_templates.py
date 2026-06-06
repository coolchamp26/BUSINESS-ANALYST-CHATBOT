import urllib.request, json

base = 'http://127.0.0.1:8000'
templates = ['dental_clinic', 'ecommerce_store', 'real_estate', 'saas_startup', 'restaurant', 'hospital', 'coaching_institute', 'marketing_agency']

print("Validating all 8 industry demo templates...\n")
all_ok = True

for tmpl in templates:
    try:
        data = json.dumps({'template_key': tmpl}).encode()
        req = urllib.request.Request(
            f'{base}/api/consultation/start',
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        res = json.loads(urllib.request.urlopen(req).read())
        session_id = res['id']
        status = res['status']

        # Fetch pre-populated analysis
        analysis = json.loads(urllib.request.urlopen(
            f'{base}/api/consultation/{session_id}/analysis'
        ).read())

        recs = len(analysis.get('recommendations', []))
        stacks = len(analysis.get('tech_stack', []))
        roi = analysis.get('roi_prediction', {})
        savings = roi.get('monthly_cost_savings', 0)
        nodes = len(analysis.get('workflow_diagram', {}).get('nodes', []))

        print(f"  [OK] {tmpl}")
        print(f"       Company : {analysis['company_name']}")
        print(f"       Status  : {status}")
        print(f"       Recs    : {recs} | Stack tools: {stacks} | Workflow nodes: {nodes}")
        print(f"       Savings : INR {savings}/mo\n")

    except Exception as e:
        print(f"  [FAIL] {tmpl}: {e}\n")
        all_ok = False

if all_ok:
    print("All 8 demo templates validated successfully!")
else:
    print("Some templates had issues — review above.")
