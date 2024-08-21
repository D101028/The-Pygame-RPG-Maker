import json

def generate_message_script(num, start = 1):
    dump_str = ""

    for i in range(start, num + 1):
        dump_str += """message_{}: 
  speakerName: 
  text: |-
    
""".format(str(i))

    with open("../Script/output.yaml", mode = "w") as file:
        file.write(dump_str)

def generate_choice_script(num, start = 1):
    dump_str = ""

    for i in range(start, num + 1):
        dump_str += """choice_{}:
  text: |-

""".format(str(i))
    
    with open("../Script/output.yaml", mode = "w") as file:
        file.write(dump_str)

if __name__ == "__main__":
    generate_message_script(50)

