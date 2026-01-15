import os
import site
import sys

fixed_content = r"""
import asyncio
import datetime
import os
import random
import re
import shutil
import socket
import subprocess
import time
import uuid
from multiprocessing import Process
from importlib.resources import files

import httpx
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from a2a.client.card_resolver import A2ACardResolver
from a2a.types import AgentCard
from agentbeats.settings import ControllerSettings

settings = ControllerSettings()
app = FastAPI()

def robust_rename(src, dst):
    for i in range(15):
        try:
            if os.path.exists(dst):
                shutil.rmtree(dst)
            os.rename(src, dst)
            return
        except PermissionError:
            if i == 14: raise
            time.sleep(1.0)

def robust_rmtree(path):
    if not os.path.exists(path): return
    for i in range(15):
        try:
            shutil.rmtree(path)
            return
        except (PermissionError, FileNotFoundError):
            if i == 14: raise
            time.sleep(1.0)

@app.get("/status")
def get_status():
    run_file = "run.bat" if os.name == "nt" and os.path.exists("run.bat") else "run.sh"
    with open(run_file, "r", encoding="utf-8") as f:
        starting_command = f.read().strip()
    agents_folder = os.path.join(".ab", "agents")
    maintained = 0
    running = 0
    if os.path.exists(agents_folder):
        for agent_id in os.listdir(agents_folder):
            if agent_id.startswith("archived"): continue
            maintained += 1
            agent_folder = os.path.join(agents_folder, agent_id)
            state_file = os.path.join(agent_folder, "state")
            if os.path.exists(state_file):
                state = open(state_file, "r", encoding="utf-8").read().strip()
                if state == "running":
                    running += 1
    return {
        "maintained_agents": maintained,
        "running_agents": running,
        "starting_command": starting_command,
    }

@app.get("/agents")
def list_agents():
    agents_folder = os.path.join(".ab", "agents")
    agents = {}
    if os.path.exists(agents_folder):
        for agent_id in os.listdir(agents_folder):
            if agent_id.startswith("archived"): continue
            agent_folder = os.path.join(agents_folder, agent_id)
            if not os.path.isdir(agent_folder): continue
            state_file = os.path.join(agent_folder, "state")
            if not os.path.exists(state_file): continue
            state = open(state_file, "r", encoding="utf-8").read().strip()
            port_file = os.path.join(agent_folder, "port")
            port = int(open(port_file, "r", encoding="utf-8").read().strip()) if os.path.exists(port_file) else None
            
            protocol = "https" if settings.https_enabled else "http"
            _host = settings.host if settings.cloudrun_host is None else settings.cloudrun_host
            _port_s = ":" + str(settings.port) if settings.cloudrun_host is None else ""
            url = f"{protocol}://{_host}{_port_s}/to_agent/{agent_id}"
            
            agents[agent_id] = {
                "url": url,
                "internal_port": port,
                "state": state,
            }
    return agents

@app.get("/agents/{agent_id}")
def get_agent_info(agent_id: str):
    agent_folder = os.path.join(".ab", "agents", agent_id)
    if not os.path.exists(agent_folder):
        return Response(content="Agent not found", status_code=404)
        
    with open(os.path.join(agent_folder, "state"), "r", encoding="utf-8") as f:
        state = f.read().strip()
        
    def read_file_safe(path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        return "Not found."

    return {
        "state": state,
        "stdout_log": read_file_safe(os.path.join(agent_folder, "stdout.log")),
        "stderr_log": read_file_safe(os.path.join(agent_folder, "stderr.log")),
        "agent_card": read_file_safe(os.path.join(agent_folder, "agent_card")),
    }

@app.post("/agents/{agent_id}/reset")
def reset_agent(agent_id: str):
    agent_folder = os.path.join(".ab", "agents", agent_id)
    if not os.path.exists(agent_folder):
        return Response(content="Agent not found", status_code=404)
    with open(os.path.join(agent_folder, "state"), "w", encoding="utf-8") as f:
        f.write("reset_requested")
    return {"message": f"Agent {agent_id} reset."}

@app.get("/info", response_class=HTMLResponse)
def get_info_page():
    return files("agentbeats.frontend").joinpath("ctrl_info.html").read_text(encoding="utf-8")

@app.api_route("/to_agent/{agent_id}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_to_agent_root(agent_id: str, request: Request):
    return await proxy_to_agent(agent_id, "", request)

@app.api_route("/to_agent/{agent_id}/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_to_agent(agent_id: str, full_path: str, request: Request):
    agent_folder = os.path.join(".ab", "agents", agent_id)
    port_file = os.path.join(agent_folder, "port")
    if not os.path.exists(port_file): return Response(content="Agent not found", status_code=404)
    port = int(open(port_file, "r", encoding="utf-8").read().strip())
    agent_url = f"http://localhost:{port}/{full_path}"
    async with httpx.AsyncClient(follow_redirects=True, timeout=1800.0) as client:
        response = await client.request(
            method=request.method, url=agent_url, content=await request.body(),
            headers=request.headers, params=request.query_params,
        )
        return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))

@app.get("/")
async def root(): return RedirectResponse(url="/info")

def find_unoccupied_port():
    while True:
        port = random.randint(20000, 60000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError: continue

async def get_agent_card(agent_port: int):
    async with httpx.AsyncClient() as client:
        resolver = A2ACardResolver(httpx_client=client, base_url=f"http://localhost:{agent_port}")
        try:
            return await resolver.get_agent_card()
        except: return None

def maintain_agent_process(agent_id: str, role="green"):
    agent_folder = os.path.join(".ab/agents", agent_id)
    agent_p = None
    agent_port = None
    while True:
        try:
            with open(os.path.join(agent_folder, "state"), "r", encoding="utf-8") as f:
                state = f.read().strip()
        except: state = "unknown"

        if state == "pending":
            agent_port = find_unoccupied_port()
            with open(os.path.join(agent_folder, "port"), "w", encoding="utf-8") as f: f.write(str(agent_port))
            env = os.environ.copy()
            env["AGENT_PORT"] = str(agent_port)
            env["ROLE"] = role
            _protocol = "https" if settings.https_enabled else "http"
            _host = settings.host if settings.cloudrun_host is None else settings.cloudrun_host
            _port_s = ":" + str(settings.port) if settings.cloudrun_host is None else ""
            env["AGENT_URL"] = f"{_protocol}://{_host}{_port_s}/to_agent/{agent_id}"
            
            with open(os.path.join(agent_folder, "stdout.log"), "w", encoding="utf-8") as fout, \
                 open(os.path.join(agent_folder, "stderr.log"), "w", encoding="utf-8") as ferr:
                cmd = ["run.bat"] if os.name == "nt" and os.path.exists("run.bat") else ["./run.sh"]
                agent_p = subprocess.Popen(cmd, cwd=os.getcwd(), shell=True, stdout=fout, stderr=ferr, env=env)
            with open(os.path.join(agent_folder, "state"), "w", encoding="utf-8") as f: f.write("starting")
        elif state == "starting":
            card = asyncio.run(get_agent_card(agent_port))
            if card is not None:
                with open(os.path.join(agent_folder, "agent_card"), "w", encoding="utf-8") as f: f.write(card.model_dump_json(indent=2))
                with open(os.path.join(agent_folder, "state"), "w", encoding="utf-8") as f: f.write("running")
        elif state == "running":
            if agent_p.poll() is not None:
                with open(os.path.join(agent_folder, "state"), "w", encoding="utf-8") as f: f.write(f"finished({agent_p.poll()})")
        elif state == "reset_requested":
            if os.name == "nt": subprocess.run(["taskkill", "/F", "/T", "/PID", str(agent_p.pid)], capture_output=True)
            else: agent_p.terminate()
            try: agent_p.wait(timeout=5)
            except: pass
            archive_parent = os.path.join(".ab", "archive")
            os.makedirs(archive_parent, exist_ok=True)
            robust_rename(agent_folder, os.path.join(archive_parent, f"archived_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{agent_id}"))
            os.makedirs(agent_folder, exist_ok=True)
            with open(os.path.join(agent_folder, "state"), "w", encoding="utf-8") as f: f.write("pending")
        time.sleep(1.0)

def main():
    os.makedirs(".ab", exist_ok=True)
    robust_rmtree(".ab/agents")
    os.makedirs(".ab/agents", exist_ok=True)
    for role in ["green", "white"]:
        agent_id = f"{role}_{uuid.uuid4().hex[:8]}"
        agent_folder = os.path.join(".ab/agents", agent_id)
        os.makedirs(agent_folder, exist_ok=True)
        with open(os.path.join(agent_folder, "state"), "w", encoding="utf-8") as f: f.write("pending")
        p = Process(target=maintain_agent_process, args=(agent_id, role))
        p.start()
    uvicorn.run(app, host=settings.host, port=settings.port)
"""

def find_controller_path():
    for p in site.getsitepackages():
        target = os.path.join(p, "agentbeats", "controller.py")
        if os.path.exists(target): return target
    for p in sys.path:
        target = os.path.join(p, "agentbeats", "controller.py")
        if os.path.exists(target): return target
    return None

target = find_controller_path()
if target:
    with open(target, "w", encoding="utf-8") as f:
        f.write(fixed_content.strip() + "\n")
    print(f"Patched: {target}")
else:
    print("Could not find agentbeats/controller.py")
