# Protocol Constants
CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "get_score_msg": "MY_SCORE",
    "get_question_msg": "GET_QUESTION",
    "send_answer_msg": "SEND_ANSWER",
    "get_highscore_msg": "HIGHSCORE",
    "get_logged_msg": "LOGGED"
}  # .. Add more commands if needed

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR",
    "score_ok_msg": "YOUR_SCORE",
    "no_questions_msg": "NO_QUESTIONS",
    "ok_get_questions_msg": "YOUR_QUESTION",
    "ok_correct_answer": "CORRECT_ANSWER",
    "wrong_answer": "WRONG_ANSWER",
    "ok_get_highscore_msg": "ALL_SCORE",
    "ok_get_logged_msg": "LOGGED_ANSWER",
    "error_cmd": "ERROR"
}  # ..  Add more commands if needed


# Other constants
ERROR = None  # What is returned in case of an error


def build_message(cmd, data):
    if not (cmd in (PROTOCOL_CLIENT.values() or PROTOCOL_SERVER.values())):
        return ERROR
    if len(data) > MAX_DATA_LENGTH or len(cmd) > 16:
        return ERROR
    else:
        full_msg = join_msg([cmd, data])
        return full_msg


"""
Parses protocol message and returns command name and data field
Returns: cmd (str), data (str). If some error occurred, returns None, None
"""


def parse_message(msg):
    data = split_msg(msg)

    if len(data) != 3:
        return ERROR, ERROR
    if not (data[0] in PROTOCOL_CLIENT.values() or data[0] in PROTOCOL_SERVER.values()):
        return ERROR, ERROR
    if len(data[0]) > 16 or len(data[1]) > 4 or len(data[2]) > MAX_DATA_LENGTH:
        return ERROR, ERROR
    if not data[1].isdigit():
        return ERROR, ERROR
    # if int(data[1]) != len(data[2]):
    #     return ERROR, ERROR

    return data[0], data[2]


"""
Helper method. gets a string and Splits the string 
using protocol's delimiter (|).
Returns: list of fields.
"""


def split_msg(msg):
    fields = msg.split(DELIMITER)

    for i in range(len(fields)):
        fields[i] = str(fields[i]).replace(" ", "")

    return fields


"""
The join_msg method Gets a list that contains the Msg Command and Msg Data, and joins them to one string divided by the delimiter.
Returns: string that looks like cell1|cell2|cell3
"""


def join_msg(msg_fields):
    msg_cmd = str(msg_fields[0]) + " " * (16 - len(msg_fields[0]))
    msg_data_len = "0" * (4 - len(str(len(msg_fields[1])))) + str(len(msg_fields[1]))
    msg_data = str(msg_fields[1])
    joined_msg = msg_cmd + DELIMITER + msg_data_len + DELIMITER + msg_data
    return joined_msg
