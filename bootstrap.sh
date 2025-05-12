#!/usr/bin/env bash
set -e

# —— 1. 进入项目根 —— #
cd "$(dirname "$0")"

# —— 2. 创建 venv（已存在就跳过） —— #
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate

# —— 3. 配置国内 PyPI 源（只写一次） —— #
mkdir -p ~/.pip
cat > ~/.pip/pip.conf <<'EOF'
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
timeout = 100
EOF

# —— 4. 安装 / 升级依赖 —— #
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Dev environment ready. Run 'source venv/bin/activate' next time."
