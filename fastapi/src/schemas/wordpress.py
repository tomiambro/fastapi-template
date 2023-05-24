from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator

from .jwt import JWT


class WPAPI(BaseModel):
    key: str = Field(None, alias="site_api_key")
    password: str = Field(None, alias="site_api_password")

    def __str__(self):
        return f"WPAPI(key={self.key}, password={self.password})"


class WPBase(BaseModel):
    blog_url: str
    blog_name: str
    blog_description: str
    db_version: Optional[str] = Field(None, alias="wordpress_db_version")
    site_version: Optional[str] = Field(None, alias="wordpress_site_version")
    user_email: Optional[str] = Field(None, alias="wordpress_user_email")
    api_credentials: Optional[WPAPI] = Field(None, alias="wordpress_api_credentials")
    active: bool = False
    token: Optional[JWT]

    def __str__(self):
        return (
            f"WPBase(blog_url={self.blog_url}, blog_name={self.blog_name}, "
            f"blog_description={self.blog_description}, db_version={self.db_version}, "
            f"site_version={self.site_version}, user_email={self.user_email}, "
            f"api_credentials={str(self.api_credentials)}, token={self.token} "
            f"active={self.active})"
        )


class WordpressCreate(WPBase):
    wordpress_api_credentials: Optional[WPAPI] = Field(
        None, alias="wordpress_api_credentials"
    )

    @validator("wordpress_api_credentials", pre=True)
    def set_api_credentials(cls, value, values):
        if value:
            values["api_credentials"] = value
        return value

    def __str__(self):
        return (
            f"WordpressCreate(blog_url={self.blog_url}, blog_name={self.blog_name}, "
            f"blog_description={self.blog_description}, db_version={self.db_version}, "
            f"site_version={self.site_version}, user_email={self.user_email}, "
            f"wordpress_api_credentials={str(self.wordpress_api_credentials)}, "
            f"active={self.active})"
        )


class WordpressUpdate(BaseModel):
    id: Optional[int]
    blog_url: Optional[str]
    blog_name: Optional[str]
    blog_description: Optional[str]
    db_version: Optional[str] = Field(None, alias="wordpress_db_version")
    site_version: Optional[str] = Field(None, alias="wordpress_site_version")
    user_email: Optional[str] = Field(None, alias="wordpress_user_email")
    wordpress_api_credentials: Optional[WPAPI] = Field(
        None, alias="wordpress_api_credentials"
    )
    active: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    token: Optional[JWT]

    @validator("wordpress_api_credentials", pre=True)
    def set_api_credentials(cls, value, values):
        if value:
            values["api_credentials"] = value
        return value


class Wordpress(WPBase):
    id: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        orm_mode = True

    def __str__(self):
        return (
            f"WordpressUpdate(id={self.id}, blog_url={self.blog_url}, "
            f"blog_name={self.blog_name}, blog_description={self.blog_description}, "
            f"db_version={self.db_version}, site_version={self.site_version}, "
            f"user_email={self.user_email}, "
            f"wordpress_api_credentials={str(self.wordpress_api_credentials)}, "
            f"active={self.active}, token={self.token} "
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )
