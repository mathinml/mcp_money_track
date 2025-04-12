from setuptools import setup, find_packages

setup(
    name="mcp_money_track",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mcp"
    ],
    author="Your Name",
    author_email="mathinml@example.com",
    description="个人记账 MCP 服务",
    keywords="money, track, mcp",
    python_requires=">=3.10",
)
