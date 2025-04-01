
isColdRetain = lambda child: child.idx_prop[5002] == 'ColdRetain' if hasattr(child,'idx_prop') else False
isNoRetain = lambda child: child.idx_prop[5002] == '' if hasattr(child,'idx_prop') else False
isRetain = lambda child: child.idx_prop[5002] == 'Retain' if hasattr(child,'idx_prop') else False