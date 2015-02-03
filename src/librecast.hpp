#include <wx/wxprec.h>

#ifndef WX_PRECOMP
    #include <wx/wx.h>
#endif

#include "ui/mainwindow.hpp"

class LibreCast : public wxApp {
public:
    virtual bool OnInit();
    virtual int OnExit();
private:
    MainWindow *mainwindow;
};

IMPLEMENT_APP(LibreCast)