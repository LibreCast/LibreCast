#include "mainwindow.hpp"

MainWindow::MainWindow() : wxFrame(NULL,wxID_ANY,"LibreCast",wxDefaultPosition,wxSize(800,600)) {
    // Initializing menus
    this->menubar = new wxMenuBar;
    this->file_menu = new wxMenu;
    this->file_menu->Append(wxID_EXIT,wxT("&Add new feed"));
    this->menubar->Append(this->file_menu,wxT("&File"));
    SetMenuBar(this->menubar);

    Centre();
}

void MainWindow::OnQuit(wxCommandEvent& WXUNUSED(event)) {
    Close(true);
}