# Two Way Indian Sign Language Translator using LSTM and NLP
INTRODUCTION  
There are approximately 70 million silent people across the world and most of them are illiterate and communicate using signs. The
nonverbal communication used by silent people is called sign language, and it is comprised of various gestures, each gesture has its
meaning. These gestures are used to express their thoughts and feelings. There is a wide range of sign languages each having their
own importance and significance. In Indian sign language both hands along with facial expressions are used to express a gesture.
These gestures are to be understood by vision. The performance of the recognition system is a significant factor that cannot be
ignored. And the performance mostly depends on the classifier as also the feature extraction method. So, a careful combination of
classifier and extraction methods is to be considered to obtain optimal solutions.
 
 
The proposed model is a two-way translator and has two modules, one each for the translation of sign to text and the translation of
text to sign. In the text to sign module, the text is taken from the user, it is processed using NLP, and the respective sign video is
returned. And in the sign to text module, the input can be either uploading a file or enacting before the webcam, the appropriate text
for the sign is displayed using LSTM, MediaPipe and OpenCV. In order to communicate signers mostly use dynamic signs. To
translate the dynamic gestures with time-series video we have chosen LSTM as it is good at processing sequences of data. This
proposed model can translate up-to word level in the sign to text module and up-to paragraph level in the text to sign module.
Our work is predominantly on Indian sign language as it is mostly used sign language in our nation and research to a great extent
is done and yet there is no proper data set or fixed stature for the Indian sign language. There are many factors that influence the
performance and accuracy of the model like hand movement, illumination, pose, occlusion, background information and noise.
These also effects in the building of a robust system that could give high accuracy in the real time. 
