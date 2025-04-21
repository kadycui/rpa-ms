from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from conf.config import settings


def register_static_file(app: FastAPI):
    """
    静态文件交互开发模式, 生产使用 nginx 静态资源服务

    :param app:
    :return:
    """
    if settings.STATIC_FILE:
        import os
        from fastapi.staticfiles import StaticFiles
        # if not os.path.exists("./static"):
        #     os.mkdir("./static")
        app.mount("/static", StaticFiles(directory=settings.STATIC_PATH), name="static")




# 注册Doc文档
def register_docs(app: FastAPI):
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} - Swagger UI",
            swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui/swagger-ui.css",
            swagger_favicon_url="/static/swagger-ui/favicon-32x32.png"
        )