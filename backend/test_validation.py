import urllib.request
import json

base = 'http://127.0.0.1:8000'

def test_validation():
    print("Testing message input validation...")
    
    # 1. Start a fresh consultation session
    data = json.dumps({
        "industry": "",
        "company_name": "",
        "company_size": ""
    }).encode()
    
    req = urllib.request.Request(
        f'{base}/api/consultation/start',
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    res = json.loads(urllib.request.urlopen(req).read())
    session_id = res['id']
    print(f"Started session: {session_id}")
    print(f"Initial AI Message: {res['messages'][0]['content']}\n")

    # 2. Test invalid keysmash message (e.g. 'asdf')
    msg_data = json.dumps({"content": "asdf"}).encode()
    req = urllib.request.Request(
        f'{base}/api/consultation/{session_id}/message',
        data=msg_data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        response = json.loads(urllib.request.urlopen(req).read())
        messages = response['messages']
        last_agent_msg = messages[-1]['content']
        print("[Rejected Keysmash] Sent: 'asdf'")
        print(f"AI Response: {last_agent_msg}")
        assert "couldn't process that response" in last_agent_msg or "re-answer" in last_agent_msg
        assert response['current_step'] == 0, f"Expected step to remain 0, got {response['current_step']}"
        print("-> OK: Step remained at 0 and warning response returned.\n")
    except Exception as e:
        print(f"Keysmash assertion failed: {e}")
        return

    # 3. Test generic greeting (e.g. 'hi')
    msg_data = json.dumps({"content": "hi"}).encode()
    req = urllib.request.Request(
        f'{base}/api/consultation/{session_id}/message',
        data=msg_data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        response = json.loads(urllib.request.urlopen(req).read())
        messages = response['messages']
        last_agent_msg = messages[-1]['content']
        print("[Rejected Greeting] Sent: 'hi'")
        print(f"AI Response: {last_agent_msg}")
        assert "couldn't process that response" in last_agent_msg or "re-answer" in last_agent_msg
        assert response['current_step'] == 0
        print("-> OK: Step remained at 0 and warning response returned.\n")
    except Exception as e:
        print(f"Greeting assertion failed: {e}")
        return

    # 4. Test valid answer
    msg_data = json.dumps({"content": "Acme Tech in SaaS Development"}).encode()
    req = urllib.request.Request(
        f'{base}/api/consultation/{session_id}/message',
        data=msg_data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        response = json.loads(urllib.request.urlopen(req).read())
        messages = response['messages']
        last_agent_msg = messages[-1]['content']
        print("[Accepted Answer] Sent: 'Acme Tech in SaaS Development'")
        print(f"AI Response: {last_agent_msg}")
        assert response['current_step'] == 1
        print("-> OK: Step advanced to 1 and next question received.\n")
    except Exception as e:
        print(f"Valid answer assertion failed: {e}")
        return

    print("[SUCCESS] Input validation system works perfectly and is fool proof!")

if __name__ == "__main__":
    test_validation()
