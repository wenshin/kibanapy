__version__ = '0.1.1'
__release_date__ = '2015-06-09'


try:
    from .dashboard import Dashboard
    from .visualization import Visualization
except Exception:
    # setup.py import module 来获取__version__ 但是如果是纯净的环境，
    # requests包依赖是没有的，所以这里用异常包裹
    pass
