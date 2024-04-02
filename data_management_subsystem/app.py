from flask import Flask, render_template, request, redirect, session, json
from chat_data_module import ChatData as cd
from datetime import datetime as dt

import datetime


app = Flask(__name__)


@app.route('/post_chat/<user_id>', methods=['POST'])
def post_chat(user_id):
    if request.method == "POST":
        json_data = request.get_json(silent=True)
        print(request.get_json(silent=True))
        chat_handler = cd(int(user_id))
        timestamp: dt = dt.now()
        user_chat_id = cd.log_chat(chat_data, timestamp, False)
        
        return json.dumps({'success': True, 'user_chat_id': user_chat_id}), 201
    else:
        return json.dumps({'success': False}), 400

@app.route('/generate_response/<user_id>', methods=['POST'])
def generate_response(user_id):
    return json.dumps({'success': False, 'Exception data': "generate_response/<user_id> POST request not implemented."}), 501
    
    try:
        user_id = int(user_id)
        chat_handler = cd(user_id)
        # This code will be executed from the front-end server to communicate
        # with the backend server.
        
        json_data = request.get_json(silent=True)
        chat_input = json_data['chat_input']
        backend_json_data = requests.post('backend_ip/generate_response', {'input': chat_input})
        robot_chat_id = cd.log_chat(backend_json_data['output'], dt.now(), True)
        if 'citations' in backend_json_data.keys():
            cd.upload_citations(robot_chat_id, backend_json_data['citations'])
        robot_chat_data = cd.get_chat_by_cid(robot_chat_id)

        i = 0
        response_time = robot_chat_data[3].strftime("%m/%d/%Y, %I:%M:%S %p")
        content_json = {'time_in_edt': response_time, 'content': robot_chat_id[1], 'citations': backend_json_data['citations']}
        return json.dumps({'success': True, 'ai_output': content_json}), 201
    except Exception as e:
        return json.dumps({'success': False, 'Exception data': str(e)}), 500

    
    

@app.route('/get_chat/<user_id>', methods=['GET'])
def get_chat(user_id):
    
    if request.method == "GET":
        chat_data = cd(user_id)
        chat_logs = cd.return_chat_history()
        chat_logs.remove(None)
        i = 0
        for row in chat_logs:
            chat_logs[i] = list(chat_logs[i])
            chat_logs[i][3] = chat_logs[i][3].strftime("%m/%d/%Y, %I:%M:%S %p")
            i+=1

        content_json = []
        for row in chat_logs:
            row_json = {'time_in_edt': row[3], 'content': row[1], 'is_from_bot': row[2]}
            if len(row) == 5:
                row_json['citations'] = row[4]
            content_json.append(row_json)

        return json.dumps({'success': True, 'chat_history': content_json, 'user_id': int(user_id)}), 201
    else:
        return json.dumps({'success': False, 'content': "You didnt ask to get it!"}), 400

if __name__=="__main__":
    app.run()
