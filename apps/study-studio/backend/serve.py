"""Single-process hosted entrypoint, with explicit persistence and authored initial content."""
import os
import uvicorn
from .deployment import settings

if __name__=='__main__':
    config=settings()
    if config.hosted:
        from .pilot.demo_course import seed
        seed()
    uvicorn.run('backend.app:app',host='0.0.0.0' if config.hosted else '127.0.0.1',port=int(os.getenv('PORT','8765')),workers=1,proxy_headers=False)
