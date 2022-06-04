from kivy.core.window import Window

Window.size = (350, 600)

from kivy.config import Config

Config.set('graphics', 'resizable', 0)
from kivy.lang import Builder
import kivy
import rawpy
import imageio
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.utils import platform

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDToolbar:
        title: "MDFileManager"
        left_action_items: [['menu', lambda x: None]]
        elevation: 10

    FloatLayout:

        MDRoundFlatIconButton:
            text: "Open manager"
            icon: "folder"
            pos_hint: {'center_x': .5, 'center_y': .6}
            on_release: app.file_manager_open()
'''


class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            # convert=self.convert,
            # preview=True
        )

    def build(self):
        return Builder.load_string(KV)

    def file_manager_open(self):
        PATH = "."
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            app_folder = os.path.dirname(os.path.abspath(__file__))
            PATH = "/storage/emulated/0"  # app_folder
        self.file_manager.show(PATH)  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.convert(path)
        toast(path)

    def convert(self, path):
        if (path[-3:] == 'dng'):
            import rawpy
            with rawpy.imread(path) as raw:
                rgb = raw.postprocess(output_color=rawpy.ColorSpace.Adobe, gamma=(1.48, 3.05), use_camera_wb=True,
                                      output_bps=8, four_color_rgb=False, user_wb=[1, 1, 1, 1], dcb_enhance=True,
                                      no_auto_bright=True, bright=4, exp_preserve_highlights=.6,
                                      demosaic_algorithm=None)

            imageio.imsave('/storage/emulated/0', rgb)
        # else:
        # img = (255*plt.imread(path)[:,:,:3]).astype('uint8')

        # return img

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


Example().run()
