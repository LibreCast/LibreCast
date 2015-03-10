#include "mainwindow.hpp"

MainWindow::MainWindow() : wxFrame(NULL,wxID_ANY,"LibreCast",wxDefaultPosition,wxSize(800,600)) {
    // Initializing menus
    this->menubar = new wxMenuBar;

    this->file_menu = new wxMenu;
    this->file_menu->Append(5,wxT("&Add new feed\tCTRL+I"));
    this->file_menu->Append(5,wxT("&Refresh\tCTRL+R"));
    this->file_menu->Append(wxID_PREFERENCES, wxT("&Preferences"));
    this->file_menu->Append(wxID_EXIT,wxT("Exit"));
    this->menubar->Append(this->file_menu,wxT("&File"));

    this->edit_menu = new wxMenu;
    this->edit_menu->Append(wxID_SELECTALL,wxT("&Select All\tCTRL+A"));
    this->edit_menu->Append(wxID_COPY,wxT("&Copy\tCTRL+C"));
    this->edit_menu->Append(wxID_PASTE,wxT("&Paste\tCTRL+V"));
    this->menubar->Append(this->edit_menu,wxT("&Edit"));

    this->help_menu = new wxMenu;
    this->help_menu->Append(wxID_ABOUT, wxT("About LibreCast"));
    this->menubar->Append(this->help_menu,wxT("&Help"));
    
    SetMenuBar(this->menubar);

    CreateStatusBar(1,wxSTB_DEFAULT_STYLE,0,wxT("IDLE"));
    SetStatusText(wxT("IDLE"));

    wxPanel *panel = new wxPanel(this, -1);

    wxBoxSizer *columns = new wxBoxSizer(wxHORIZONTAL);

    wxBoxSizer *vbox = new wxBoxSizer(wxVERTICAL);
    wxBoxSizer *search_hbox = new wxBoxSizer(wxHORIZONTAL);
    wxTextCtrl *search_form = new wxTextCtrl(panel,-1);
    search_form->SetHint(wxT("Something to search for ..."));
    wxButton *search_button = new wxButton(panel,-1,wxT("Search"),wxDefaultPosition, wxSize(70, 30));
    search_hbox->Add(search_form,0,wxALIGN_CENTER_VERTICAL|wxEXPAND);
    search_hbox->Add(search_button,0,wxALIGN_CENTER_VERTICAL);
    vbox->Add(search_hbox,0,wxEXPAND);

    wxBoxSizer *sidebar = new wxBoxSizer(wxVERTICAL);
    wxCommandLinkButton *jeej = new wxCommandLinkButton(panel,-1,wxT("Search"),wxT("(discover new videos)"),wxDefaultPosition, wxSize(250, 50));
    sidebar->Add(jeej,0);
    wxCommandLinkButton *jouj = new wxCommandLinkButton(panel,-1,wxT("Downloads"),wxT("(download manager)"),wxDefaultPosition, wxSize(250, 50));
    sidebar->Add(jouj,0);

    columns->Add(sidebar,0,wxALL,10);
    columns->Add(vbox,0,wxEXPAND|wxALL,10);

    panel->SetSizer(columns);

    Centre();
}

void MainWindow::OnQuit(wxCommandEvent& WXUNUSED(event)) {
    Close(true);
}