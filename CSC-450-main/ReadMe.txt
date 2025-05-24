Welocme to the Employee Training Completion Enforcement System!

Description: 
    The Employee Training Completion Enforcement System is a video player that is meant to constrain the system and watch the user to verify they have watched the given
video in it's entirety. The system locks certain user inputs, checks the volume, and tracks the users face all to make sure the user finishes the video before giving
control back tothe user. Once completed the system will create a certificate holding a hash which the user sends to thier manager/employer, so the manager/employer can
verify the completion of the video by inputing the user credentials and the hash made from it using the hash verification program.

For Testing:
    Run the program through gui.py to start video player program and run the man_gui.py top start the hash verification program.

Video Player Program:
    Menu:
        Desription:
                There will be a text box for inputing an optional youtube link and a continue button to either select a local video (if the text box is empty), or go straight
            to the user selecting a local video. The user will then be required to put in their user credentials. Once the user puts in their credentials and clicks
            "submit", they will be greeted to the video player. Once the user finishes the video, the video player will close and the menu will want the user to select where
            they would like their certificate to be downloaded
    Video Player:
        Description:
                The video user will see a video player menu and a live feed of the face detection as it's own windows. The user will be able to click the "Play" button to start
            the video and "Pause/Resume" to pause, or resume the video. There will also be a volume slider that goes from 30-100.
        Face Detection:
                The face detection tracks the angle of the user's face in respect to the camera, for the program to work properly, the camera needs to be forward face of the user
            while the user is looking at the screen. The face detection screen will indicate when the user is to far away and will pause the video if the user is undetected,
            or if their face is not indicated as "striaght" by the face detection.
        Video Player Restraints:
            The video player will restrain the user from pressing the windows key, tab, shift, alt, home, prtsc, del key. It will also remove the windows task bar and make the video
            player the dominant page. Once the video is finished, it will give the user control again before closing.

    WARNING: MUST NOT HAVE OBS OPEN FOR FACE TRACKER TO WORK!!!!

Hash Verification Program:
    Description:
        The Hash Verification Program, will allow the manager/employer to put in the hash inside of the certificate given by the trainee and the trainnes credentials. It then
        generates it's own hash and verifies it is equivilant to the given hash. If they are the same it will notify that it is verified meaning the trainee watched the video. If it's
        is not equivilant, that indicates the trainee has not watched the video.

Developed by: Arthas Lee, Eric Morgan, Mason Pummill, and Anthony Funke
Stakeholder: Mohammed Belkhouche
Property of Missouri State University