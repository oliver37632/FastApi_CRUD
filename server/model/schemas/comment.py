from pydantic import BaseModel, constr


class Comments(BaseModel):

    content: constr(min_length=1, max_length=255)
