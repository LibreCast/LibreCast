#include <wx/wx.h>
#include <wx/commandlinkbutton.h>

class MainWindow : public wxFrame {
public:
    MainWindow();
    void OnQuit(wxCommandEvent& WXUNUSED(event));
private:
    wxMenuBar *menubar;
    wxMenu *file_menu;
    wxMenu *edit_menu;
    wxMenu *help_menu;
};