#include "librecast.hpp"

bool LibreCast::OnInit() {
    this->mainwindow = new MainWindow();
    this->mainwindow->Show(true);
    return true;
}

int LibreCast::OnExit() {
    return 0;
}