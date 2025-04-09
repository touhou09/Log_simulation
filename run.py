import asyncio
from main import app
from fastapi import FastAPI
import uvicorn
from output_plugins import get_output_plugin
from generator import start_log_generator

async def main():
    output_plugin = get_output_plugin()
    asyncio.create_task(start_log_generator(output_plugin))
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    asyncio.run(main())