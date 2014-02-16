import logging

class Action(object):
    def __init__(self, name, mind=None, type=None, watch=None, class_watch=None):
        self.name = name

        if watch is None:
            watch = {}

        if class_watch is None:
            class_watch = []

        self.watch = watch
        self.class_watch = class_watch

        if mind is not None:
            mind.register_action(self, type)

        self.type = type
        
    def __call__(self, function):
        def func(self_, *args, **kwargs):

            messages = []

            messages.append("Recording {action} from {player}.".format(action=self.name, player=self_))
            
            for index, name in self.watch.items():
                if name in kwargs:
                    value = kwargs[name]
                elif index < len(args):
                    value = args[index]
                else:
                    continue

                messages.append('{name} is currently {value}'.format(name=name, value=value))

            for name in self.class_watch:
                try:
                    messages.append('{name} is current {value}'.format(name=name, value=self_.__getattribute__(name)))
                except AttributeError:
                    logging.error("No such property as {name}".format(name=name))


            logging.debug('\n'.join(messages))

            try:
                self_.mind.record(self_, self.name)
            except AttributeError:
                logging.error("{name} has no mind!".format(name=self.name))

            return function(self_, *args, **kwargs)

        try:
            _ = func.func_dict
        except AttributeError as e:
            func.func_dict = {}

        func.func_dict['action'] = True
        func.func_dict['type'] = self.type
        return func
