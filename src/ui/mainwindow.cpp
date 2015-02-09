#include "mainwindow.hpp"

MainWindow::MainWindow() : wxFrame(NULL,wxID_ANY,"LibreCast",wxDefaultPosition,wxSize(800,600)) {
    // Initializing menus
    this->menubar = new wxMenuBar;

    this->file_menu = new wxMenu;
    this->file_menu->Append(5,wxT("&Add new feed\tCTRL+I"));
    this->file_menu->Append(5,wxT("&Refresh\tCTRL+R"));
    this->menubar->Append(this->file_menu,wxT("&File"));

    this->edit_menu = new wxMenu;
    this->edit_menu->Append(wxID_SELECTALL,wxT("&Select All\tCTRL+A"));
    this->edit_menu->Append(wxID_COPY,wxT("&Copy\tCTRL+C"));
    this->edit_menu->Append(wxID_PASTE,wxT("&Paste\tCTRL+V"));
    this->menubar->Append(this->edit_menu,wxT("&Edit"));
    
    SetMenuBar(this->menubar);

    CreateStatusBar(1,wxSTB_DEFAULT_STYLE,0,wxT("IDLE"));
    SetStatusText(wxT("IDLE"));

    wxBoxSizer *topSizer = new wxBoxSizer(wxVERTICAL);

    Centre();
}

void MainWindow::OnQuit(wxCommandEvent& WXUNUSED(event)) {
    Close(true);
}