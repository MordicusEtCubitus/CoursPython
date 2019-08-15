"""
GraphMe class is a context manager allowing to generate the call graph of functions
It is a very basic implementation used to demonstrate Python/inspection potential

    ```python
    from graphme import GraphMe

    def fibo(n):
        return n if n <= 1 else fibo(n-1) + fibo(n-2)

    with GraphMe() as gfx:
        fibo(7)

    gfx.show()
    ```
"""

import sys
import traceback
from graphviz import Digraph
import inspect

class GraphMe:
    """
    GrapĥMe context manager

    When writing:

    with MyObject() as var:
        actions()

    Python executes something like:

    try:
        var = MyObject().__enter__()
        actions()
    finally:
        var.__exit__()

    This is called context Manager, see PEP343 for more details
    https://www.python.org/dev/peps/pep-0343/
    """

    def __init__(self, filename='graphme', format='svg'):
        self.old_profile = None  # Keep trace of previous profiler if any
        self.graph = None  # graphviz object
        self.call_number = 0  # number of functions called
        self.frame_ids = {}  # keep trace of functions ids to manage unique identifiers and parent link
        self.filename = filename
        self.format = format

    def __enter__(self):

        self.old_profile = sys.getprofile()  # Keep profiler to restore it, if any already set

        # Build the graph
        self.graph = Digraph(filename=self.filename, format=self.format)

        # Reset values
        self.call_number = 0
        self.frame_ids = {}

        # Set caller function used to build graph call
        sys.setprofile(self.caller)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.setprofile(self.old_profile)


    def caller(self, frame, event, arg):

        # Only worry about creating graph call for functions
        if event != 'call':
            return

        # The call number is used to help identifying functions
        self.call_number += 1

        # We cannot use frame ids to identify uniquely functions calls
        # Because when a function terminates, its frame id may be reused for new functions
        # generating wrong graph reference, so we use a custom id

        # If id already exists, this is a reused one, we can overwrite it
        key = id(frame)
        self.frame_ids[key] = str(self.call_number)

        # Build frame id and parent frame id
        frame_id = self.frame_ids[key]
        parent_frame = frame.f_back
        p_key = id(parent_frame)

        # If not found, it has not been called inside the with statement, it is the __enter__ statement
        if p_key not in self.frame_ids:
            self.frame_ids[p_key] = None

        parent_frame_id = self.frame_ids[p_key]

        # Parent and current traceback frame information: they contain the functions names
        tb_parent_frame, tb_frame = traceback.extract_stack(frame, limit=2)

        attrs = ", ".join([ "%s=%s" % (k, v if type(v) in (int, float, str, bool) else '...') for k, v in frame.f_locals.items()])

        # Do not graph __exit__
        if self not in frame.f_locals.values():
            self.graph.node(frame_id, "%s(%s)" % (tb_frame.name, attrs))

        # Do not add link to parent if not created in the with statement
        if parent_frame_id is not None:
            self.graph.edge(parent_frame_id, frame_id)


    def show(self):
        self.graph.view()


if __name__ == '__main__':
    def fibo(n):
        return n if n <= 1 else fibo(n - 1) + fibo(n - 2)

    def square(x):
        return x ** 2

    with GraphMe(filename="fibo43square3") as gfx:
        fibo(4)
        fibo(2)
        square(3)

    gfx.show()

