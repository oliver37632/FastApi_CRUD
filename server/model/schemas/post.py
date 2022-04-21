from pydantic import BaseModel, constr


class Posts(BaseModel):
    title: constr(min_length=1, max_length=10)
    content: constr(min_length=1, max_length=100)
