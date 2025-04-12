

#### 安装

```bash
git clone https://github.com/mathinml/mcp_money_track.git
cd mcp_money_track
pip install mcp
pip install .
```
#### 配置信息

```bash
{
  "mcpServers": {
    "money-track-mcp": {
      "command": "path-to-your-python",
      "args": [
        "-m",
        "mcp_money_track"
      ],
      "env": {
        "ACCOUNTING_WORKING_DIR": "/Users/xyz/account"
      }
    }
  }
} 
```