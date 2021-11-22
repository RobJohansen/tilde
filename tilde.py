'''Flask Shell'''

from app import app, db
from app.models import User, Node, NodeTerm

@app.shell_context_processor
def make_shell_context():
    '''Context for interactive shell, i.e. `flask shell`'''

    return {
        'db': db,
        'User': User,
        'Node': Node,
        'NodeTerm': NodeTerm
    }
