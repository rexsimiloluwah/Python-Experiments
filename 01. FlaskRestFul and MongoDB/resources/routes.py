from .users import Auth, Register, Login
from .projects import Projects, ProjectsDetail

def init_routes(api):
    api.add_resource(Auth, '/api/auth/users')
    api.add_resource(Register, '/api/auth/register')
    api.add_resource(Login, '/api/auth/login')
    api.add_resource(Projects, '/api/projects')
    api.add_resource(ProjectsDetail, '/api/projects/<id>')