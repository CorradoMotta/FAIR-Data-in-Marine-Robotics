/*************************************************************************
 *
 * Basic metadata information. It is a row layout composed by an info icon
 * that gives information on hovering, a label and a text field where the
 * user can digit the attribute for each value.
 *
 *************************************************************************/

import QtQuick 2.0
import QtQuick.Layouts 1.2
import QtQuick.Controls 2.15

Item {
    id: root

    property alias title_text: label.text
    property alias value_text: label_text.text
    property alias hovering_text: info_label_text.text
    property alias title_color: label.color
    property string currentValue: ""

    implicitHeight: rl.implicitHeight
    implicitWidth: rl.implicitWidth


    RowLayout{
        id: rl
        anchors.fill: parent
        spacing: 6
        Image {
            z: 10
            id: info
            source: "Images/info.png"
            Rectangle{
                id: info_label
                anchors.bottom: info.top
                anchors.bottomMargin: - (info_label_text.height/3)
                anchors.left: info.right
                width: info_label_text.implicitWidth + 6
                height: info_label_text.implicitHeight + 6
                color: "white"
                border.color: "darkorange"
                visible: false

                Text{
                    id: info_label_text
                    font.family: "Helvetica"
                    anchors.horizontalCenter: info_label.horizontalCenter
                    anchors.verticalCenter: info_label.verticalCenter
                    font.pixelSize: 15
                }
            }
            MouseArea{
                id: info_ma
                anchors.fill: parent
                hoverEnabled : true
                onEntered: info_label.visible = true
                onExited:  info_label.visible = false
            }
        }
        Label {
            id: label
            font.family: "Helvetica"
            font.pixelSize: 18
            //Layout.minimumWidth: 200
        }
        Item{
            id: space
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        TextField {
            id: label_text
            Layout.preferredWidth: 400
            font.family: "Helvetica"
            font.pixelSize: 18
            width: 500
            onEditingFinished: root.currentValue = label_text.text
        }
    }
}
