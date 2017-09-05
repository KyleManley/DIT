import os
import imp

from circuits import Loader
from dit_flow.widget_factory import WidgetFactory

class WidgetLoader(Loader):
    def init(self, channel=Loader.channel):
        base_dir = os.getcwd() # dirname(__file__)
        flow_dir = os.path.join(base_dir, 'dit_flow')
        self._widget_dir = os.path.join(base_dir, 'dit_flow', 'dit_widget')
        common_dir = os.path.join(base_dir, 'dit_flow', 'dit_widget', 'common')
        print('directory: ', base_dir)
        print('widget directory: ', self.widget_dir)
        print('flow dir: ', flow_dir)
        self._loader = Loader(paths=[base_dir, flow_dir, self.widget_dir, common_dir])

    @property
    def loader(self):
        return self._loader

    @property
    def widget_dir(self):
        return self._widget_dir

    def find_widget(self, widget_name):
        config_file = widget_name + ".yaml"
        method_file = widget_name + ".py"
        found_config = False
        found_method = False
        widget_files = (None, None)
        for root, dirs, files in os.walk(self.widget_dir, topdown=False) :
            if config_file in files:
                config_path = os.path.join(root, config_file)
                found_config = True
            if method_file in files:
                method_path = os.path.join(root, method_file)
                found_method = True
            if found_config and found_method:
                widget_files = (config_path, method_path)
                break
        return widget_files


    def load_widget(self, widget_name):

        widget = WidgetFactory.createWidget(widget_name)
        widget.speak()

