import os
import subprocess
import sys

# Conda 环境名称
conda_env = "py3918"

# 项目目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
project_a_dir = os.path.join(BASE_DIR, "tavily-company-research")
project_a_ui_dir = os.path.join(project_a_dir, "ui")  # 前端目录
project_b_dir = os.path.join(BASE_DIR, "Q-MacroAgent")  # Streamlit 项目

def check_dir(path, name):
    if not os.path.exists(path):
        print(f"❌ {name} 目录不存在: {path}")
        sys.exit(1)

def check_package_json(path):
    pkg_path = os.path.join(path, "package.json")
    if not os.path.exists(pkg_path):
        print(f"❌ package.json 不存在: {pkg_path}")
        sys.exit(1)

def run_cmd(cmd, cwd=None):
    try:
        process = subprocess.Popen(cmd, cwd=cwd, shell=True)
        return process
    except FileNotFoundError as e:
        print(f"❌ 命令启动失败: {cmd}\n错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 检查 conda 环境
    if os.environ.get("CONDA_DEFAULT_ENV") != conda_env:
        print(f"⚠ 请先在终端手动运行: conda activate {conda_env}")
        sys.exit(1)

    # 检查目录和 package.json
    check_dir(project_a_dir, "Project A (后端)")
    check_dir(project_a_ui_dir, "Project A UI (前端)")
    check_dir(project_b_dir, "Project B (Streamlit)")
    check_package_json(project_a_ui_dir)

    # 启动前端
    print("启动 Project A 前端 (npm run dev)...")
    run_cmd("npm run dev", cwd=project_a_ui_dir)

    # 启动后端
    print("启动 Project A 后端 (python -m application)...")
    run_cmd("python -m application", cwd=project_a_dir)

    # 启动 Streamlit
    print("启动 Project B (Streamlit)...")
    run_cmd("streamlit run web_app.py", cwd=project_b_dir)

    print("✅ 所有服务已启动，请在浏览器访问相应端口")
