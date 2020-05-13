/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.11.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QLineEdit *ti_user;
    QLineEdit *ti_psw;
    QLabel *u_label;
    QLabel *psw_label;
    QPushButton *b_login;
    QPushButton *b_quit;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(400, 300);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        ti_user = new QLineEdit(centralWidget);
        ti_user->setObjectName(QStringLiteral("ti_user"));
        ti_user->setGeometry(QRect(130, 60, 113, 31));
        ti_psw = new QLineEdit(centralWidget);
        ti_psw->setObjectName(QStringLiteral("ti_psw"));
        ti_psw->setGeometry(QRect(130, 100, 113, 31));
        u_label = new QLabel(centralWidget);
        u_label->setObjectName(QStringLiteral("u_label"));
        u_label->setGeometry(QRect(20, 60, 91, 26));
        QFont font;
        font.setPointSize(12);
        font.setBold(true);
        font.setWeight(75);
        u_label->setFont(font);
        psw_label = new QLabel(centralWidget);
        psw_label->setObjectName(QStringLiteral("psw_label"));
        psw_label->setGeometry(QRect(30, 100, 81, 26));
        psw_label->setFont(font);
        b_login = new QPushButton(centralWidget);
        b_login->setObjectName(QStringLiteral("b_login"));
        b_login->setGeometry(QRect(30, 170, 115, 34));
        b_login->setFont(font);
        b_quit = new QPushButton(centralWidget);
        b_quit->setObjectName(QStringLiteral("b_quit"));
        b_quit->setGeometry(QRect(180, 170, 115, 34));
        b_quit->setFont(font);
        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 400, 32));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MainWindow->setStatusBar(statusBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", nullptr));
        u_label->setText(QApplication::translate("MainWindow", "User Name:", nullptr));
        psw_label->setText(QApplication::translate("MainWindow", "pass word:", nullptr));
        b_login->setText(QApplication::translate("MainWindow", "Log In", nullptr));
        b_quit->setText(QApplication::translate("MainWindow", "Quit", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
