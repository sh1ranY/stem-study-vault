"""Learner workspace: continuation suggestions and drafts, separate from assessed evidence."""
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import Field, BaseModel, ConfigDict
from . import store, learning_path

class Draft(BaseModel):
    model_config=ConfigDict(extra="forbid")
    revision:int=Field(ge=0)
    answers:dict[str,str]
    working:str=Field(default='',max_length=12000)
    photo_id:Optional[str]=None
    prior_seen:bool=False

def create_router(user, required, fail, lock):
    router=APIRouter()
    @router.get('/learning/overview')
    def overview(u=Depends(user)):
        owner=u['id']
        return learning_path.overview(store.listing('task',owner),store.listing('attempt',owner),store.listing('guided-session',owner),store.listing('answer-draft',owner))

    @router.put('/drafts/{task_id}')
    def save_draft(task_id:str,body:Draft,u=Depends(user)):
        with lock,store.engine.begin() as conn:
            t=required('task',u['id'],task_id,conn)
            if not set(body.answers).issubset({f['id'] for f in t['fields']}) or any(len(v)>200 for v in body.answers.values()):
                fail(422,'草稿字段无效。 / Invalid draft fields.')
            if body.photo_id and required('photo',u['id'],body.photo_id,conn)['task_id']!=task_id:
                fail(422,'照片属于另一道题。 / Photo belongs to another task.')
            previous=store.fetch('answer-draft',u['id'],task_id,conn)
            revision=previous['revision'] if previous else 0
            value=body.model_dump(exclude={'revision'})
            # Replaying a successful save after an interrupted response is safe.
            if previous and all(previous.get(k)==v for k,v in value.items()): return previous
            if body.revision!=revision: fail(409,'另一页面更新了这份草稿，请载入已保存版本。 / This draft changed in another tab. Load the saved version.')
            return store.save('answer-draft',u['id'],{'id':task_id,'revision':revision+1,'at':store.now(),**value},conn)

    @router.get('/drafts/{task_id}')
    def draft(task_id:str,u=Depends(user)):
        required('task',u['id'],task_id)
        return store.fetch('answer-draft',u['id'],task_id)
    return router
