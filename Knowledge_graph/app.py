from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 预设JSON文件存放目录 - 您可以修改这个路径
PRESET_JSON_DIR = 'preset_jsons'
os.makedirs(PRESET_JSON_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/preset-files')
def get_preset_files():
    """获取预设的JSON文件列表"""
    try:
        files = []
        if os.path.exists(PRESET_JSON_DIR):
            for filename in os.listdir(PRESET_JSON_DIR):
                if filename.endswith('.json'):
                    files.append({
                        'name': filename,
                        'path': filename
                    })
        return jsonify({'success': True, 'files': files})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/load-preset/<filename>')
def load_preset_file(filename):
    """加载预设的JSON文件"""
    try:
        # 安全检查文件名
        filename = secure_filename(filename)
        filepath = os.path.join(PRESET_JSON_DIR, filename)
        
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'error': '文件不存在'})
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 验证数据格式
        if not validate_graph_data(data):
            return jsonify({'success': False, 'error': '无效的图数据格式'})
        
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """上传并解析JSON文件"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': '没有选择文件'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': '没有选择文件'})
        
        if file and file.filename.endswith('.json'):
            # 直接读取文件内容，不保存到磁盘
            content = file.read().decode('utf-8')
            data = json.loads(content)
            
            # 验证数据格式
            if not validate_graph_data(data):
                return jsonify({'success': False, 'error': '无效的图数据格式'})
            
            return jsonify({'success': True, 'data': data})
        else:
            return jsonify({'success': False, 'error': '请上传JSON文件'})
    
    except json.JSONDecodeError:
        return jsonify({'success': False, 'error': 'JSON格式错误'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def validate_graph_data(data):
    """验证图数据格式"""
    if not isinstance(data, dict):
        return False
    
    # 检查是否包含nodes和relationships字段
    if 'nodes' not in data or 'relationships' not in data:
        return False
    
    # 检查nodes格式
    if not isinstance(data['nodes'], list):
        return False
    
    node_ids = set()
    for node in data['nodes']:
        if not isinstance(node, dict) or 'id' not in node:
            return False
        node_ids.add(node['id'])
    
    # 检查relationships格式
    if not isinstance(data['relationships'], list):
        return False
    
    # 验证关系中的节点引用（允许有缺失的节点，但会在前端处理）
    for rel in data['relationships']:
        if not isinstance(rel, dict) or not all(key in rel for key in ['source', 'target', 'type']):
            return False
    
    return True

if __name__ == '__main__':
    app.run(debug=True, port=5000)