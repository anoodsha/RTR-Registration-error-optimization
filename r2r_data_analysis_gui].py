import wx
from r2r_regression_model import run_regression_model
from arrange_data import txt_to_csv
from mappying_alg import map_sensors_cam_data


class RTR_Analysis(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='R2R DATA ANALYSIS')
        panel = wx.Panel(self)

        self.text_ctrl = wx.TextCtrl(panel, pos=(10, 10))
        # CREATE A BUTTON
        regression_btn = wx.Button(panel, label='Regression analysis', pos=(5, 55))
        regression_btn.Bind(wx.EVT_BUTTON, self.on_press)
        self.CreateStatusBar()
        self.SetStatusText("Welcome to RTR - DATA - ANALYSIS")
        self.Show()

    def on_press(self, event):
        folder_path = self.text_ctrl.GetValue()
        if not folder_path:
            print("You didn't enter anything!")
        else:
            print(f'You typed: "{folder_path}"')

            # convert, map, run analysis
            self.SetStatusText("CONVERT TEXT FILES TO CSV")
            txt_to_csv(folder_path)

            self.SetStatusText("MAPPING DATA")
            map_sensors_cam_data(folder_path)

            self.SetStatusText("RUNNING REGRESSION ANALYSIS")
            self.display_results()

    def display_results(self):
        results = run_regression_model(folder_path, 0, 'Error_cam_12_dx_MD')
        print('R2 for Random forest model:', results[0])
        print('OOR2 For Random forest:  ', results[1])
        print('features importance matrix: ', results[2])




if __name__ == '__main__':
    app = wx.App()
    frame = RTR_Analysis()
    app.MainLoop()
