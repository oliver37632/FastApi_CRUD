from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from server.controller import post, auth, comment


app = FastAPI()

app.add_middleware(
    CORSMiddleware,          # CORS 설정
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.app)     # 라우터 세팅
app.include_router(auth.app)
app.include_router(comment.app)

if __name__ == '__main__':
    uvicorn.run("server.main:app", host="0.0.0.0", port=5000, reload=True)  # reload = 디버깅


    '''
    
import uvicorn




if __name__ == "__main__":



uvicorn.run(

 "app.main:app",

 host="localhost",

 port=8000,

 reload=True,

 reload_excludes=["app/files/"],

 )
    '''