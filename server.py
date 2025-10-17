# server.py
import os
from flask import Flask, render_template, request, jsonify
import subprocess
import time

# Initialize Flask application
app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'test.py')

        if not os.path.exists(script_path):
            return jsonify({'error': 'Script file does not exist'}), 404

        start_time = time.time()
        process = subprocess.Popen(
            ['python', script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        return jsonify({
            'output': stdout if stdout else stderr,
            'exitCode': process.returncode,
            'executionTime': round((time.time() - start_time) * 1000, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)