import jitsi

# Create a virtual user
user = jitsi.JitsiUser("virtual user")

# Set the user's camera and microphone to the default integrated devices
user.set_camera(jitsi.JitsiCamera.DEFAULT)
user.set_microphone(jitsi.JitsiMicrophone.DEFAULT)

# Read text from the virtual user
text = user.read_text()

# Ask a question to the end user
question = "What is your name?"
user.ask_question(question)

# Get the end user's response
response = user.get_response()

# Print the end user's response
print(response)
