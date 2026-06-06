import urllib.request
import json
import time

def test_api():
    base_url = "http://127.0.0.1:8000"
    print("Starting API integration validation...")
    
    # 1. Health check
    try:
        req = urllib.request.urlopen(f"{base_url}/api/health")
        res = json.loads(req.read().decode())
        print(f"[OK] Health check passed: {res}")
    except Exception as e:
        print(f"[FAIL] Health check failed: {e}")
        return

    # 2. Get Templates
    try:
        req = urllib.request.urlopen(f"{base_url}/api/templates")
        res = json.loads(req.read().decode())
        print(f"[OK] Fetched templates list. Available count: {len(res)}")
        print(f"     Found: {[t['key'] for t in res]}")
    except Exception as e:
        print(f"[FAIL] Templates fetch failed: {e}")
        return

    # 3. Onboard fresh Consultation Session
    try:
        data = json.dumps({"industry": "Dental Clinic", "company_name": "Apex Dental"}).encode('utf-8')
        headers = {"Content-Type": "application/json"}
        request = urllib.request.Request(f"{base_url}/api/consultation/start", data=data, headers=headers)
        response = urllib.request.urlopen(request)
        session = json.loads(response.read().decode())
        session_id = session["id"]
        print(f"[OK] Initialized new consultation session: {session_id}")
    except Exception as e:
        print(f"[FAIL] Session start failed: {e}")
        return

    # 4. Exchange Message
    try:
        data = json.dumps({"content": "We are a dental clinic with 12 staff members."}).encode('utf-8')
        request = urllib.request.Request(f"{base_url}/api/consultation/{session_id}/message", data=data, headers=headers)
        response = urllib.request.urlopen(request)
        chat = json.loads(response.read().decode())
        print(f"[OK] Message exchange successful. Message count: {len(chat['messages'])}")
        print(f"     AI Question: {chat['messages'][-1]['content']}")
    except Exception as e:
        print(f"[FAIL] Message exchange failed: {e}")
        return

    # 5. Run analyze
    try:
        request = urllib.request.Request(f"{base_url}/api/consultation/{session_id}/analyze", data=b'', headers=headers)
        response = urllib.request.urlopen(request)
        analysis = json.loads(response.read().decode())
        print(f"[OK] Business Analysis reasoning completed.")
        print(f"     Readiness metrics: {analysis['readiness_scores']}")
        print(f"     First Recommendation: {analysis['recommendations'][0]['title']}")
    except Exception as e:
        print(f"[FAIL] Analysis Agent reasoning failed: {e}")
        return

    # 6. Fetch PDF Report
    try:
        req = urllib.request.urlopen(f"{base_url}/api/reports/{session_id}/pdf")
        pdf_bytes = req.read()
        print(f"[OK] Report PDF compiled and streamed successfully. Size: {len(pdf_bytes)} bytes")
    except Exception as e:
        print(f"[FAIL] PDF download failed: {e}")
        return

    print("\n[SUCCESS] All backend API integration tests passed successfully!")

if __name__ == "__main__":
    test_api()
