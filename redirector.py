from flask import Flask, render_template, request, redirect, abort
import json, logging

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# 从文件导入规则
def load_redirect_rules():
    try:
        with open('config.json', 'r') as file:
            rules = json.load(file)
            return rules
    except FileNotFoundError:
        return {}

# 导出规则到文件
def save_redirect_rules(rules):
    with open('config.json', 'w') as file:
        json.dump(rules, file)

# 初始化规则
redirect_rules = load_redirect_rules()

# 添加规则
def add_rule(domain, destination):
    redirect_rules[domain] = destination
    save_redirect_rules(redirect_rules)

# 移除规则
def remove_rule(domain):
    if domain in redirect_rules:
        del redirect_rules[domain]
        save_redirect_rules(redirect_rules)


def try_do_redirect():
    domain = request.host
    if domain in redirect_rules:
        destination = redirect_rules[domain]
        print(f"* Redir {domain} ==> {destination}")
        return redirect(destination, code=302)  # You can use 301 for permanent redirects


@app.route('/')
def index():
    return try_do_redirect() or render_template('index.html', redirect_rules=redirect_rules)

@app.route('/add_rule', methods=['POST'])
def add():
    domain = request.form.get('domain')
    destination = request.form.get('destination')
    add_rule(domain, destination)
    return redirect('/')

@app.route('/remove_rule/<domain>', methods=['GET'])
def remove(domain):
    remove_rule(domain)
    return redirect('/')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
