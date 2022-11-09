import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Window 2.15
import BaseModel

Window {
    title: "FAIR metadata"
    width: 1400
    minimumWidth: 1400
    height: 800
    visible: true
    id: mainWindow

    Metadata{
        anchors.fill: parent
    }
    Rectangle{
        id: message_prompt

        anchors{
            horizontalCenter: parent.horizontalCenter
            bottom: parent.bottom
            bottomMargin: 100
        }

        width: Math.max(1100, text_prompt.implicitWidth + 200)
        height: text_prompt.implicitHeight + 10
        radius: 20
        color: "cornflowerblue"
        opacity: 0

        property alias message : text_prompt.text

        Text{
            id: text_prompt
            anchors.horizontalCenter: message_prompt.horizontalCenter
            anchors.verticalCenter: message_prompt.verticalCenter
            font.family: "Helvetica"
            font.pixelSize: 18
        }
    }

    SequentialAnimation{

        id: message_prompt_anim

        NumberAnimation {
            target: message_prompt
            property: "opacity"
            from: 0.0; to: 1.0
            duration: 1000
        }
        PauseAnimation{
            duration: 2000
        }
        NumberAnimation {
            id: message_prompt_anim_disappear
            target: message_prompt
            property: "opacity"
            from: 1.0; to: 0
            duration: 600
        }
    }

    // =========
    // Functions
    // =========

    /*
     * Display the message prompt with the text given in input
     */
    function messagePrompt(prompt_text){

        message_prompt.message = prompt_text
        message_prompt_anim.running = true
    }
}
