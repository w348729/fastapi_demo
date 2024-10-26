from fastapi import BackgroundTasks
from fastapi import APIRouter
from fastapi import Body
from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from app.routers.authentication import UserAuth
from app.routers.authentication import get_current_active_user
from app.db.db_utils import db_demo
from app.models.story import Story, StoryUpdate


story_collections = db_demo['story']

story_router = APIRouter(
    prefix='/story'
)


def response_model(data):
    return {
        'data': [data],
        'code': 200,
        'message': 'done'
    }


def ErrorResponseModel(error, code, message):
    return {
        'error': error, 
        'code': code, 
        'message': message
    }


def story_serilizer(story):
    return {
        'title': story.get('title'),
        'content': story.get('content'),
        'author': story.get('author'),
        'country': story.get('country')
    }


# get all story
async def get_all_story():
    stroy_list = []
    for entry in story_collections.find():
        stroy_list.append(story_serilizer(entry))
    return stroy_list


# get 1 story with title
async def get_one_story(title: str) -> dict:
    story = story_collections.find_one({'title': title})
    if story:
        return story_serilizer(story)


# add new story
async def add_story(story_data: dict) -> dict:
    story = story_collections.insert_one(story_data)
    new_story = story_collections.find_one({'_id': story.inserted_id})
    return story_serilizer(new_story)


# update stroy with given data
async def update_story(title: str, data: dict):
    # Return false if an empty request body
    if len(data) < 1:
        return False
    story = story_collections.find_one({'title': title})
    if not story:
        return False
    if story:
        updated_story = story_collections.update_one(
            {'title': title}, {'$set': data}
        )
        if updated_story:
            return True
        return False


# delete a story 
async def delete_story(title: str):
    story = story_collections.find_one({'title': title})
    if not story:
        return False
    print(title)
    story_collections.delete_one({'title': title})
    return True


# add new story
@story_router.post('/')
async def add_story_data(story: Story = Body(...), current_user: UserAuth = Depends(get_current_active_user)):
    story = jsonable_encoder(story)
    new_story = await add_story(story)
    return response_model(new_story)


# get all story
@story_router.get('/')
async def get_story(current_user: UserAuth = Depends(get_current_active_user)):
    story = await get_all_story()
    if story:
        return response_model(story)
    return response_model(story)


# update story
@story_router.put('/{title}')
async def update_story_data(title: str, new_data: StoryUpdate = Body(...), current_user: UserAuth = Depends(get_current_active_user)):
    new_data = {k: v for k, v in new_data.model_dump().items() if v is not None}
    updated_story = await update_story(title, new_data)
    if updated_story:
        return response_model(f'story with title: {title} updated',)
    return ErrorResponseModel('got error', 404, 'an error in updating')


# delete a stroy
@story_router.delete('/{title}')
async def delete_story_data(title: str, current_user: UserAuth = Depends(get_current_active_user)):
    deleted_story = await delete_story(title)
    if deleted_story:
        return response_model(f'story with title: {title} removed')
    return ErrorResponseModel('got error occurred', 404, 'story not exist')


def batch_update_tasks():
    # update stroy which county in none or unexist
    for entry in story_collections.find():
        if not entry.get('country'):
            story_collections.update_one({'title': entry.get('title')}, {'$set': {'country': 'cn'}})
    return True


# backend tasks of batch update story without country
@story_router.post('/batch_update')
async def batch_update(background_tasks: BackgroundTasks):
    background_tasks.add_task(batch_update_tasks)
    return response_model('batch updated in backend')