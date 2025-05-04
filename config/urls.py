"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/auth/',include('apps.authentication.routes.auth_routes')),

    path('api/admin/create-agent/',include("apps.admin.create_agent.routes.create_agent_routes")),

    # path('api/client/chat-with-agent/',include("apps.chat.routes.agent_chat_route")),

    path('api/admin/train/', include("apps.admin.train_agent.routes.training_route")),

    path('api/user/tempchat/', include("apps.user.temp_chat.routes.temp_chat_route")),
    
    path('api/user/chat/', include("apps.user.chat.routes.chat_route")),
]