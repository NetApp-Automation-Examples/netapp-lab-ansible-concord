from ansible.utils.display import Display


class FilterModule(object):
    def filters(self): return {'warning': self.warn_filter}

    def warn_filter(self, message, **kwargs):
        
        if message:
            Display().warning(message)
        
        return message