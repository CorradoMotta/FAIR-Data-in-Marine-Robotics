/*************************************************************************
 *
 * Metadata qml view. This is the global metadata view. It loads all the
 * elements from the cpp model which in turn is generated from JSON
 * database.
 *
 *************************************************************************/

import QtQuick 2.0
import QtQuick.Layouts 1.2
import QtQuick.Controls 2.15
import QtQuick.Dialogs
import BaseModel

Rectangle {

    color: "whitesmoke"

    property bool isMainView: false
    //property date currentDate: new Date()

    Rectangle {
        id: tabRectangle
        y: 20
        height: tabTitle.height * 2
        color: "#87bfee"
        anchors.rightMargin: 0
        anchors.leftMargin: 0
        anchors.left: parent.left
        anchors.right: parent.right

        Label {
            id: tabTitle
            color: "#ffffff"
            text: qsTr("Global Metadata")
            font.family: "Helvetica"
            font.pixelSize: 16
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    Item {
        id: item2
        height: gridLayout3.implicitHeight
        anchors.rightMargin: 20
        anchors.leftMargin: 20
        anchors.bottomMargin: 20
        anchors.topMargin: 20
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: tabRectangle.bottom

        GridLayout {
            id: gridLayout3
            rowSpacing: 10
            columns: 2
            columnSpacing: 10
            anchors.fill: parent

            Repeater {
                id: rp
                model: BaseModel {}
                BasicMetadataInput{
                    Layout.fillWidth: true
                    //Layout.alignment: Qt.AlignRight
                    title_color: isMandatory ? "darkorange" : ""
                    title_text: name
                    value_text: value
                    hovering_text: description
                    onCurrentValueChanged: value = currentValue
                }
            }
        }
    }
    RowLayout {
        id: rowLayout1
        anchors.top: item2.bottom
        anchors.left: parent.left
        anchors.leftMargin: 20
        anchors.right: parent.right
        anchors.topMargin: 50
        Label {

            id: label
            Layout.minimumWidth: 100
            font.family: "Helvetica"
            font.pixelSize: 18
            font.bold: true
            text: "Path to telemetry:"
            //Layout.minimumWidth: 200
        }
        TextField {
            id: label_text
            Layout.preferredWidth: 600
            font.family: "Helvetica"
            font.pixelSize: 18
            width: 500
            //onEditingFinished: root.currentValue = label_text.text
        }
        Image {
            z: 10
            id: info
            source: "Images/system.png"
            MouseArea{
                id: info_ma
                anchors.fill: parent
                onClicked: fileDialog.open()
            }
        }
        Item{
            id: space
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }
    RowLayout {
        id: rowLayout3
        anchors.top: rowLayout1.bottom
        anchors.right: parent.right
        anchors.rightMargin: 20
        anchors.topMargin: 10

        Button {
            id: defaultButton
            Layout.preferredHeight: 30
            Layout.preferredWidth: 60
            text: qsTr("Default")
            onClicked: rp.model.default()
        }

        Button {
            id: clearButton
            Layout.preferredHeight: 30
            Layout.preferredWidth: 60
            text: qsTr("Clear")
            onClicked: rp.model.reset()
        }

        Button {
            id: goButton
            Layout.preferredHeight: 30
            Layout.preferredWidth: 100
            text: qsTr("Generate INI")
            onClicked: generateINI()
        }
        Button {
            id: ncButton

            Layout.preferredHeight: 30
            Layout.preferredWidth: 100
            text: qsTr("Generate NetCDF")
            onClicked: message_dialog_2.visible = true
        }

        Button {
            id: cancelButton
            Layout.preferredHeight: 30
            Layout.preferredWidth: 60
            text: qsTr("Quit")
            onClicked: Qt.quit()
        }
    }
    Item {
        Layout.fillHeight: true
        Layout.columnSpan: 4
    }
    Layout.fillHeight: true
    Layout.fillWidth: true

    FileDialog {
        id: fileDialog
        title: "Please choose a file"
        onAccepted: {
            label_text.text = fileDialog.currentFile
        }
    }
    MessageDialog {
        id: message_dialog_2
        title: "Note"
        text: "This operation will overwrite existing ini files with what specified here."
        informativeText: "Do you want to continue?"
        buttons: MessageDialog.Ok | MessageDialog.Cancel
        visible: false
        onAccepted: messagePrompt(rp.model.generateNC(label_text.text))
    }
    MessageDialog {
        id: message_dialog
        title: "Note"
        text: "A conf.ini file is already existing!"
        informativeText: "Do you want to overwrite it?"
        buttons: MessageDialog.Ok | MessageDialog.Cancel
        visible: false
        onAccepted: rp.model.generateINI(false)? "" : messagePrompt("ini file generated!")
    }
    function generateINI(){
        var result = rp.model.generateINI(true)
        if(result)
            message_dialog.visible = true
        else messagePrompt("ini file generated!")

    }
}
