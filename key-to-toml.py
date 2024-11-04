import json
import toml

output_file = ".streamlit/secrets.toml"
with open("firestore-key.json") as json_file:
    json_text = json_file.read()

cred = {"cred": json_text}
toml_cred = toml.dumps(cred)

options = {
    "options": json.dumps(
        {
            'databaseURL': "https://manage-reading-schedule-default-rtdb.asia-southeast1.firebasedatabase.app",
            'storageBucket': "manage-reading-schedule.appspot.com",
        }
    )
}
toml_options = toml.dumps(options)

with open(output_file, "w") as target:
    target.write(toml_cred)
    target.write(toml_options)
